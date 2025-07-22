import streamlit as st

# Streamlit config
st.set_page_config(
    page_title="Bergen Climate Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌍"
)

# Define pages
home_page = st.Page("home.py", title="Home", icon="🏠", default=True)
temperature_page = st.Page("statistics/temperature.py", title="Temperature Trends", icon="🌡️")
rainfall_page = st.Page("statistics/rainfall.py", title="Rainfall Patterns", icon="🌧️")
analysis_page = st.Page("analysis/annual_summary.py", title="Annual Summary", icon="📊")
trends_page = st.Page("analysis/trend_analysis.py", title="Trend Analysis", icon="📈")

# Navigation
pg = st.navigation(
    {
        "Home": [home_page],
        "Statistics": [temperature_page, rainfall_page],
        "Analysis": [analysis_page, trends_page],
    }
)

# Run the navigation
pg.run()
