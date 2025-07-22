import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from src.shared_utils import setup_sidebar

st.title("📈 Climate Trend Analysis & Forecasting")
st.markdown("Explore historical trends and projected climate changes for Bergen, Norway")

# Load filtered data
df, year_range = setup_sidebar()

# Convert time to datetime if not already
df['time'] = pd.to_datetime(df['time'])

# Check if we have enough data for meaningful analysis
if len(df) < 365:  # Less than a year of data
    st.warning("⚠️ Limited data available. For more accurate trend analysis, consider expanding the year range.")

# Group by year for trend analysis
yearly = df.groupby(df['time'].dt.year).agg({
    'temperature_avg': 'mean',
    'temperature_2m_max': 'max',
    'temperature_2m_min': 'min', 
    'precipitation_sum': 'sum'
}).reset_index().rename(columns={'time': 'year'})

# Check if we have multiple years for trend analysis
if len(yearly) < 2:
    st.error("❌ Need at least 2 years of data for trend analysis. Please adjust the year range filter.")
    st.stop()

# Historical Trends Section
st.markdown("## 📊 Historical Climate Trends")

col1, col2 = st.columns(2)

with col1:
    # Temperature trend analysis
    temp_slope = np.polyfit(yearly['year'], yearly['temperature_avg'], 1)[0]
    temp_r2 = r2_score(yearly['temperature_avg'], np.polyval(np.polyfit(yearly['year'], yearly['temperature_avg'], 1), yearly['year']))
    
    if temp_slope > 0.05:
        temp_trend = "🔺 Warming"
        temp_color = "red"
    elif temp_slope < -0.05:
        temp_trend = "🔻 Cooling" 
        temp_color = "blue"
    else:
        temp_trend = "➡️ Stable"
        temp_color = "gray"
    
    st.metric(
        "Temperature Trend", 
        temp_trend,
        delta=f"{temp_slope:.3f}°C/year",
        help=f"R² = {temp_r2:.3f} (higher = more reliable trend)"
    )

with col2:
    # Precipitation trend analysis
    rain_slope = np.polyfit(yearly['year'], yearly['precipitation_sum'], 1)[0]
    rain_r2 = r2_score(yearly['precipitation_sum'], np.polyval(np.polyfit(yearly['year'], yearly['precipitation_sum'], 1), yearly['year']))
    
    if rain_slope > 10:
        rain_trend = "🔺 Increasing"
        rain_color = "blue"
    elif rain_slope < -10:
        rain_trend = "🔻 Decreasing"
        rain_color = "orange"
    else:
        rain_trend = "➡️ Stable"
        rain_color = "gray"
    
    st.metric(
        "Precipitation Trend",
        rain_trend, 
        delta=f"{rain_slope:.1f}mm/year",
        help=f"R² = {rain_r2:.3f} (higher = more reliable trend)"
    )

# Forecasting Section
st.markdown("## 🔮 Future Climate Projections")

col1, col2 = st.columns([2, 1])

with col1:
    forecast_years = st.slider("Forecast horizon (years)", 1, 50, 20, help="Number of years to project into the future")

with col2:
    confidence_level = st.selectbox("Confidence Level", [90, 95, 99], index=1, help="Statistical confidence for prediction intervals")

# Prepare data for forecasting
X = yearly[['year']]
X_future = pd.DataFrame({'year': range(yearly['year'].max() + 1, yearly['year'].max() + forecast_years + 1)})
X_combined = pd.concat([X, X_future])

# Temperature forecasting with confidence intervals
temp_model = LinearRegression().fit(X, yearly['temperature_avg'])
temp_pred_historical = temp_model.predict(X)
temp_pred_future = temp_model.predict(X_future)
temp_pred_all = temp_model.predict(X_combined)

# Calculate prediction intervals (simplified approach)
temp_residuals = yearly['temperature_avg'] - temp_pred_historical
temp_std = np.std(temp_residuals)
z_score = {90: 1.645, 95: 1.96, 99: 2.576}[confidence_level]
temp_margin = z_score * temp_std

# Precipitation forecasting
rain_model = LinearRegression().fit(X, yearly['precipitation_sum']) 
rain_pred_historical = rain_model.predict(X)
rain_pred_future = rain_model.predict(X_future)
rain_pred_all = rain_model.predict(X_combined)

rain_residuals = yearly['precipitation_sum'] - rain_pred_historical
rain_std = np.std(rain_residuals)
rain_margin = z_score * rain_std

# Create interactive forecast plots
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=('🌡️ Temperature Forecast', '🌧️ Precipitation Forecast'),
    vertical_spacing=0.1
)

# Temperature plot
fig.add_trace(
    go.Scatter(x=yearly['year'], y=yearly['temperature_avg'], 
               mode='markers+lines', name='Historical Temperature',
               line=dict(color='#ff6b6b', width=2),
               marker=dict(size=6)), row=1, col=1
)

fig.add_trace(
    go.Scatter(x=X_future['year'], y=temp_pred_future,
               mode='lines', name='Temperature Forecast', 
               line=dict(color='#ff6b6b', width=2, dash='dash')), row=1, col=1
)

# Add confidence intervals for temperature
fig.add_trace(
    go.Scatter(x=X_combined['year'], y=temp_pred_all + temp_margin,
               mode='lines', line=dict(width=0), showlegend=False), row=1, col=1
)
fig.add_trace(
    go.Scatter(x=X_combined['year'], y=temp_pred_all - temp_margin,
               mode='lines', line=dict(width=0), 
               fill='tonexty', fillcolor='rgba(255,107,107,0.2)',
               name=f'{confidence_level}% Confidence'), row=1, col=1
)

# Precipitation plot
fig.add_trace(
    go.Scatter(x=yearly['year'], y=yearly['precipitation_sum'],
               mode='markers+lines', name='Historical Precipitation',
               line=dict(color='#4ecdc4', width=2),
               marker=dict(size=6)), row=2, col=1
)

fig.add_trace(
    go.Scatter(x=X_future['year'], y=rain_pred_future,
               mode='lines', name='Precipitation Forecast',
               line=dict(color='#4ecdc4', width=2, dash='dash')), row=2, col=1
)

# Add confidence intervals for precipitation
fig.add_trace(
    go.Scatter(x=X_combined['year'], y=rain_pred_all + rain_margin,
               mode='lines', line=dict(width=0), showlegend=False), row=2, col=1
)
fig.add_trace(
    go.Scatter(x=X_combined['year'], y=rain_pred_all - rain_margin,
               mode='lines', line=dict(width=0),
               fill='tonexty', fillcolor='rgba(78,205,196,0.2)',
               name=f'{confidence_level}% Confidence'), row=2, col=1
)

fig.update_layout(height=700, hovermode='x unified', showlegend=True)
fig.update_yaxes(title_text="Temperature (°C)", row=1, col=1)
fig.update_yaxes(title_text="Precipitation (mm)", row=2, col=1)

st.plotly_chart(fig, use_container_width=True)

# Key Projections Summary
st.markdown("## � Key Projections Summary")

col1, col2, col3 = st.columns(3)

with col1:
    future_temp_change = temp_pred_future[-1] - yearly['temperature_avg'].iloc[-1]
    st.metric(
        f"Temp Change by {yearly['year'].max() + forecast_years}",
        f"{future_temp_change:+.1f}°C",
        help="Projected temperature change from current levels"
    )

with col2:
    future_rain_change = rain_pred_future[-1] - yearly['precipitation_sum'].iloc[-1]
    st.metric(
        f"Precipitation Change by {yearly['year'].max() + forecast_years}",
        f"{future_rain_change:+.0f}mm",
        help="Projected annual precipitation change from current levels"
    )

with col3:
    avg_temp_2020s = yearly[yearly['year'] >= 2020]['temperature_avg'].mean() if len(yearly[yearly['year'] >= 2020]) > 0 else yearly['temperature_avg'].mean()
    future_temp_avg = np.mean(temp_pred_future[-10:])  # Last 10 years of forecast
    decadal_change = future_temp_avg - avg_temp_2020s
    st.metric(
        "Decadal Temperature Change", 
        f"{decadal_change:+.1f}°C",
        help="Average temperature change per decade"
    )

# Model Performance & Reliability
with st.expander("📊 Model Performance & Reliability"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Temperature Model")
        st.write(f"**R² Score:** {temp_r2:.3f}")
        st.write(f"**Trend:** {temp_slope:.3f}°C/year")
        st.write(f"**Standard Error:** ±{temp_std:.2f}°C")
        
    with col2:
        st.markdown("#### Precipitation Model")
        st.write(f"**R² Score:** {rain_r2:.3f}")
        st.write(f"**Trend:** {rain_slope:.1f}mm/year")
        st.write(f"**Standard Error:** ±{rain_std:.0f}mm")
    
    st.info("💡 **Note:** These are simple linear projections based on historical trends. Actual climate change involves complex, non-linear processes. Use these projections as indicative trends rather than precise predictions.")

# Forecast data table
with st.expander("View Detailed Forecast Data"):
    forecast_df = pd.DataFrame({
        'Year': X_future['year'],
        'Temperature Forecast (°C)': temp_pred_future.round(1),
        'Temperature Range (°C)': [f"{(t-temp_margin):.1f} - {(t+temp_margin):.1f}" for t in temp_pred_future],
        'Precipitation Forecast (mm)': rain_pred_future.round(0),
        'Precipitation Range (mm)': [f"{int(r-rain_margin)} - {int(r+rain_margin)}" for r in rain_pred_future]
    })
    
    st.dataframe(forecast_df, use_container_width=True)
    
    # Download forecast data
    csv = forecast_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Forecast Data",
        data=csv,
        file_name=f'bergen_climate_forecast_{yearly["year"].max() + 1}_{yearly["year"].max() + forecast_years}.csv',
        mime='text/csv'
    )