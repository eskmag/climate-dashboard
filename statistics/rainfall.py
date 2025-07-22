import streamlit as st
import pandas as pd
from src.shared_utils import setup_sidebar
from src.plots import plot_rainfall_trends

st.title("🌧️ Rainfall Patterns")
st.markdown("Detailed analysis of precipitation patterns and trends")

# Setup sidebar and get filtered data
filtered_df, year_range = setup_sidebar()

# Main content
st.markdown("### Rainfall Patterns Over Time")
plot_rainfall_trends(filtered_df)

# Rainfall insights
col1, col2 = st.columns(2)
with col1:
    wettest_day = filtered_df.loc[filtered_df['precipitation_sum'].idxmax()]
    st.info(f"💧 **Wettest Day:** {wettest_day['time']} with {wettest_day['precipitation_sum']:.1f}mm")
with col2:
    avg_daily_rain = filtered_df['precipitation_sum'].mean()
    st.info(f"☔ **Average Daily Rainfall:** {avg_daily_rain:.1f}mm")

# Additional rainfall analysis
st.markdown("### 📊 Precipitation Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Rainfall Statistics")
    rain_stats = filtered_df['precipitation_sum'].describe().round(2)
    st.dataframe(rain_stats.to_frame('Precipitation (mm)'), use_container_width=True)

with col2:
    st.markdown("#### Monthly Precipitation Totals")
    monthly_rain = filtered_df.groupby(pd.to_datetime(filtered_df['time']).dt.to_period('M'))['precipitation_sum'].sum().round(1)
    st.dataframe(monthly_rain.to_frame('Total (mm)'), use_container_width=True, height=300)

# Rainfall categories
st.markdown("### 🌦️ Rainfall Categories")

# Categorize rainfall
rain_df = filtered_df.copy()
rain_df['rain_category'] = pd.cut(
    rain_df['precipitation_sum'], 
    bins=[0, 1, 5, 15, 50, float('inf')],
    labels=['No Rain (0-1mm)', 'Light (1-5mm)', 'Moderate (5-15mm)', 'Heavy (15-50mm)', 'Very Heavy (50+mm)'],
    include_lowest=True
)

rain_categories = rain_df['rain_category'].value_counts().sort_index()

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Days by Rainfall Category")
    st.dataframe(rain_categories.to_frame('Number of Days'), use_container_width=True)

with col2:
    st.markdown("#### Rainfall Category Percentages")
    rain_percentages = (rain_categories / len(rain_df) * 100).round(1)
    st.dataframe(rain_percentages.to_frame('Percentage (%)'), use_container_width=True)

# Seasonal rainfall
if len(filtered_df) > 0:
    st.markdown("### 🍂 Seasonal Rainfall Patterns")
    
    # Add season column
    rain_df['month'] = rain_df['time'].dt.month
    rain_df['season'] = rain_df['month'].map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
    })
    
    seasonal_rain = rain_df.groupby('season').agg({
        'precipitation_sum': ['sum', 'mean', 'max']
    }).round(1)
    
    # Flatten column names
    seasonal_rain.columns = ['Total (mm)', 'Daily Avg (mm)', 'Max Daily (mm)']
    
    # Reorder seasons
    season_order = ['Spring', 'Summer', 'Autumn', 'Winter']
    seasonal_rain = seasonal_rain.reindex(season_order)
    
    st.dataframe(seasonal_rain, use_container_width=True)

# Raw data section
with st.expander("🔍 View Raw Precipitation Data"):
    st.markdown(f"Showing data for years {year_range[0]} - {year_range[1]}")
    
    # Search functionality
    search_term = st.text_input("🔍 Search in data (optional)")
    display_df = filtered_df[['time', 'precipitation_sum']].copy()
    
    if search_term:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    
    st.dataframe(
        display_df, 
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download rainfall data as CSV",
        data=csv,
        file_name=f'bergen_rainfall_{year_range[0]}_{year_range[1]}.csv',
        mime='text/csv'
    )
