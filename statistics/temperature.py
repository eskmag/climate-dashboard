import streamlit as st
import pandas as pd
from src.shared_utils import setup_sidebar
from src.plots import plot_temperature_trends

st.title("🌡️ Temperature Trends")
st.markdown("Detailed analysis of temperature patterns over time")

# Setup sidebar and get filtered data
filtered_df, year_range = setup_sidebar()

# Main content
st.markdown("### Temperature Trends Over Time")
plot_temperature_trends(filtered_df)

# Temperature insights
col1, col2, col3 = st.columns(3)

max_temp = filtered_df['temperature_2m_max'].max()
min_temp = filtered_df['temperature_2m_min'].min()
avg_temp = filtered_df['temperature_avg'].mean()

with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Highest Temperature", f"{max_temp:.1f}°C")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Lowest Temperature", f"{min_temp:.1f}°C")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Average Temperature", f"{avg_temp:.1f}°C")
    st.markdown('</div>', unsafe_allow_html=True)

# Additional analysis
st.markdown("### 📊 Temperature Analysis")

# Monthly averages - convert datetime to string for grouping
monthly_temps = filtered_df.groupby(pd.to_datetime(filtered_df['time']).dt.to_period('M')).agg({
    'temperature_2m_max': 'mean',
    'temperature_2m_min': 'mean',
    'temperature_avg': 'mean'
}).round(1)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Monthly Temperature Averages")
    st.dataframe(monthly_temps, use_container_width=True)

with col2:
    st.markdown("#### Temperature Statistics")
    temp_stats = filtered_df[['temperature_2m_max', 'temperature_2m_min', 'temperature_avg']].describe().round(1)
    st.dataframe(temp_stats, use_container_width=True)

# Seasonal analysis
if len(filtered_df) > 0:
    st.markdown("### 🍂 Seasonal Temperature Patterns")
    
    # Add season column
    temp_df = filtered_df.copy()
    temp_df['month'] = temp_df['time'].dt.month
    temp_df['season'] = temp_df['month'].map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
    })
    
    seasonal_temps = temp_df.groupby('season').agg({
        'temperature_avg': 'mean',
        'temperature_2m_max': 'max',
        'temperature_2m_min': 'min'
    }).round(1)
    
    # Reorder seasons
    season_order = ['Spring', 'Summer', 'Autumn', 'Winter']
    seasonal_temps = seasonal_temps.reindex(season_order)
    
    st.dataframe(seasonal_temps, use_container_width=True)
