import streamlit as st
import pandas as pd
from src.shared_utils import setup_sidebar
from src.plots import plot_annual_averages

st.title("📊 Annual Climate Summary")
st.markdown("Comprehensive annual analysis of temperature and precipitation trends")

# Setup sidebar and get filtered data
filtered_df, year_range = setup_sidebar()

# Main content
st.markdown("### Annual Climate Trends")
plot_annual_averages(filtered_df)

# Annual statistics
st.markdown("### 📈 Year-over-Year Analysis")

# Calculate annual statistics
annual_stats = filtered_df.groupby("year").agg({
    "temperature_avg": ["mean", "std"],
    "temperature_2m_max": "max",
    "temperature_2m_min": "min",
    "precipitation_sum": ["sum", "mean", "max"]
}).round(2)

# Flatten column names
annual_stats.columns = [
    'Avg Temp (°C)', 'Temp Std Dev', 'Max Temp (°C)', 
    'Min Temp (°C)', 'Total Rain (mm)', 'Daily Rain Avg (mm)', 'Max Daily Rain (mm)'
]

st.dataframe(annual_stats, use_container_width=True)

# Climate trends analysis
if len(annual_stats) >= 2:
    st.markdown("### 🔍 Climate Trends Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Temperature Trends")
        
        # Temperature trend
        first_year_temp = annual_stats['Avg Temp (°C)'].iloc[0]
        last_year_temp = annual_stats['Avg Temp (°C)'].iloc[-1]
        temp_change = last_year_temp - first_year_temp
        
        if temp_change > 0:
            st.success(f"🌡️ **Temperature Trend:** +{temp_change:.1f}°C increase over the period")
        elif temp_change < 0:
            st.info(f"🌡️ **Temperature Trend:** {temp_change:.1f}°C decrease over the period")
        else:
            st.info(f"🌡️ **Temperature Trend:** No significant change")
        
        # Warmest and coldest years
        warmest_year = annual_stats['Avg Temp (°C)'].idxmax()
        coldest_year = annual_stats['Avg Temp (°C)'].idxmin()
        
        st.write(f"🔥 **Warmest Year:** {warmest_year} ({annual_stats.loc[warmest_year, 'Avg Temp (°C)']}°C)")
        st.write(f"❄️ **Coldest Year:** {coldest_year} ({annual_stats.loc[coldest_year, 'Avg Temp (°C)']}°C)")
    
    with col2:
        st.markdown("#### Precipitation Trends")
        
        # Precipitation trend
        first_year_rain = annual_stats['Total Rain (mm)'].iloc[0]
        last_year_rain = annual_stats['Total Rain (mm)'].iloc[-1]
        rain_change = last_year_rain - first_year_rain
        
        if rain_change > 0:
            st.success(f"🌧️ **Precipitation Trend:** +{rain_change:.0f}mm increase over the period")
        elif rain_change < 0:
            st.warning(f"🌧️ **Precipitation Trend:** {rain_change:.0f}mm decrease over the period")
        else:
            st.info(f"🌧️ **Precipitation Trend:** No significant change")
        
        # Wettest and driest years
        wettest_year = annual_stats['Total Rain (mm)'].idxmax()
        driest_year = annual_stats['Total Rain (mm)'].idxmin()
        
        st.write(f"💧 **Wettest Year:** {wettest_year} ({annual_stats.loc[wettest_year, 'Total Rain (mm)']}mm)")
        st.write(f"🏜️ **Driest Year:** {driest_year} ({annual_stats.loc[driest_year, 'Total Rain (mm)']}mm)")

# Extreme events analysis
st.markdown("### 🌪️ Extreme Weather Events")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Temperature Extremes")
    
    # Hottest day
    hottest_day = filtered_df.loc[filtered_df['temperature_2m_max'].idxmax()]
    st.metric(
        "Hottest Day", 
        f"{hottest_day['temperature_2m_max']:.1f}°C",
        delta=f"{hottest_day['time']}"
    )
    
    # Coldest day
    coldest_day = filtered_df.loc[filtered_df['temperature_2m_min'].idxmin()]
    st.metric(
        "Coldest Day", 
        f"{coldest_day['temperature_2m_min']:.1f}°C",
        delta=f"{coldest_day['time']}"
    )

with col2:
    st.markdown("#### Precipitation Extremes")
    
    # Wettest day
    wettest_day = filtered_df.loc[filtered_df['precipitation_sum'].idxmax()]
    st.metric(
        "Wettest Day", 
        f"{wettest_day['precipitation_sum']:.1f}mm",
        delta=f"{wettest_day['time']}"
    )
    
    # Count of heavy rain days (>15mm)
    heavy_rain_days = len(filtered_df[filtered_df['precipitation_sum'] > 15])
    st.metric(
        "Heavy Rain Days", 
        f"{heavy_rain_days}",
        delta="(>15mm/day)"
    )

with col3:
    st.markdown("#### Climate Averages")
    
    # Average temperature
    avg_temp_overall = filtered_df['temperature_avg'].mean()
    st.metric(
        "Overall Avg Temp", 
        f"{avg_temp_overall:.1f}°C"
    )
    
    # Total precipitation
    total_precip = filtered_df['precipitation_sum'].sum()
    st.metric(
        "Total Precipitation", 
        f"{total_precip:.0f}mm"
    )

# Download section
st.markdown("### 📥 Data Export")

col1, col2 = st.columns(2)

with col1:
    # Download annual summary
    annual_csv = annual_stats.to_csv()
    st.download_button(
        label="📊 Download Annual Summary",
        data=annual_csv,
        file_name=f'bergen_annual_summary_{year_range[0]}_{year_range[1]}.csv',
        mime='text/csv'
    )

with col2:
    # Download complete filtered data
    complete_csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📋 Download Complete Data",
        data=complete_csv,
        file_name=f'bergen_complete_data_{year_range[0]}_{year_range[1]}.csv',
        mime='text/csv'
    )
