import streamlit as st
import pandas as pd
from src.process_data import process_data

@st.cache_data
def load_data():
    """Load and process climate data"""
    df = pd.read_csv("data/bergen_climate_data.csv")
    return process_data(df)

def setup_sidebar():
    """Setup sidebar with filters and key statistics"""
    df = load_data()
    
    # Sidebar for filters and controls
    st.sidebar.header("Dashboard Controls")
    
    # Year filter
    year_range = st.sidebar.slider(
        "Select Year Range", 
        min_value=int(df['year'].min()), 
        max_value=int(df['year'].max()), 
        value=(int(df['year'].min()), int(df['year'].max())),
        help="Filter data by year range"
    )
    
    # Filter data based on selection
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    # Key metrics in the sidebar
    st.sidebar.markdown("#### 📈 Key Stats")
    
    # Compact metrics with smaller text
    avg_temp = filtered_df['temperature_avg'].mean()
    total_rain = filtered_df['precipitation_sum'].sum()
    max_temp = filtered_df['temperature_2m_max'].max()
    min_temp = filtered_df['temperature_2m_min'].min()
    
    cols = st.sidebar.columns(2)
    cols[0].metric("Avg Temp (°C)", f"{avg_temp:.1f}")
    cols[1].metric("Total Rain (mm)", f"{total_rain:.0f}")
    cols[0].metric("Max Temp (°C)", f"{max_temp:.1f}")
    cols[1].metric("Min Temp (°C)", f"{min_temp:.1f}")

    
    return filtered_df, year_range
