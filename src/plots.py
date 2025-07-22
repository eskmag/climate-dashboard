import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_temperature_trends(df):
    """Create an interactive temperature trends plot"""
    
    # Create subplot for better visualization
    fig = go.Figure()
    
    # Add temperature lines
    fig.add_trace(go.Scatter(
        x=df['time'], 
        y=df['temperature_2m_max'],
        mode='lines',
        name='Max Temperature',
        line=dict(color='#ff6b6b', width=2),
        hovertemplate='<b>Max Temp</b><br>Date: %{x}<br>Temperature: %{y:.1f}°C<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['time'], 
        y=df['temperature_2m_min'],
        mode='lines',
        name='Min Temperature',
        line=dict(color='#4ecdc4', width=2),
        hovertemplate='<b>Min Temp</b><br>Date: %{x}<br>Temperature: %{y:.1f}°C<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['time'], 
        y=df['temperature_avg'],
        mode='lines',
        name='Average Temperature',
        line=dict(color='#45b7d1', width=3),
        hovertemplate='<b>Avg Temp</b><br>Date: %{x}<br>Temperature: %{y:.1f}°C<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title="Temperature Trends Over Time",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        hovermode='x unified',
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_rainfall_trends(df):
    """Create an interactive rainfall plot"""
    
    # Create monthly aggregation for better visualization
    df_monthly = df.copy()
    df_monthly['year_month'] = pd.to_datetime(df_monthly['time']).dt.to_period('M')
    monthly_rain = df_monthly.groupby('year_month')['precipitation_sum'].sum().reset_index()
    monthly_rain['year_month'] = monthly_rain['year_month'].dt.to_timestamp()
    
    # Create the plot
    fig = px.bar(
        monthly_rain, 
        x='year_month', 
        y='precipitation_sum',
        title="Monthly Rainfall Totals",
        labels={
            'year_month': 'Date',
            'precipitation_sum': 'Precipitation (mm)'
        },
        color='precipitation_sum',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        hovermode='x'
    )
    
    fig.update_traces(
        hovertemplate='<b>Monthly Rainfall</b><br>Date: %{x}<br>Precipitation: %{y:.1f}mm<extra></extra>'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add daily rainfall as well in an expander
    with st.expander("View Daily Rainfall Data"):
        daily_fig = px.line(
            df, 
            x='time', 
            y='precipitation_sum',
            title="Daily Rainfall",
            labels={
                'time': 'Date',
                'precipitation_sum': 'Daily Precipitation (mm)'
            },
            color_discrete_sequence=['#1f77b4']
        )
        daily_fig.update_layout(height=400)
        st.plotly_chart(daily_fig, use_container_width=True)

def plot_annual_averages(df):
    """Create annual summary visualizations"""
    
    # Calculate annual statistics
    annual = df.groupby("year").agg({
        "temperature_avg": "mean",
        "temperature_2m_max": "max",
        "temperature_2m_min": "min",
        "precipitation_sum": "sum"
    }).round(2)
    
    annual.reset_index(inplace=True)
    
    # Create subplots
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature trends
        temp_fig = go.Figure()
        
        temp_fig.add_trace(go.Scatter(
            x=annual['year'],
            y=annual['temperature_avg'],
            mode='lines+markers',
            name='Average Temperature',
            line=dict(color='#ff6b6b', width=3),
            marker=dict(size=8)
        ))
        
        temp_fig.update_layout(
            title="Annual Average Temperature",
            xaxis_title="Year",
            yaxis_title="Temperature (°C)",
            height=400
        )
        
        st.plotly_chart(temp_fig, use_container_width=True)
    
    with col2:
        # Precipitation trends
        precip_fig = go.Figure()
        
        precip_fig.add_trace(go.Bar(
            x=annual['year'],
            y=annual['precipitation_sum'],
            name='Annual Precipitation',
            marker_color='#4ecdc4'
        ))
        
        precip_fig.update_layout(
            title="Annual Total Precipitation",
            xaxis_title="Year",
            yaxis_title="Precipitation (mm)",
            height=400
        )
        
        st.plotly_chart(precip_fig, use_container_width=True)
    
    # Summary table
    st.markdown("### 📋 Annual Climate Summary Table")
    
    # Rename columns for better display
    display_annual = annual.rename(columns={
        'year': 'Year',
        'temperature_avg': 'Avg Temp (°C)',
        'temperature_2m_max': 'Max Temp (°C)',
        'temperature_2m_min': 'Min Temp (°C)',
        'precipitation_sum': 'Total Rain (mm)'
    })
    
    st.dataframe(
        display_annual, 
        use_container_width=True,
        hide_index=True
    )
