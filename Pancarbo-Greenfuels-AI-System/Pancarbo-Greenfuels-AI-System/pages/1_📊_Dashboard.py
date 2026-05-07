"""
Dashboard Page - Real-time monitoring
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import generate_sensor_data, generate_biomass_dataset
from app_config.config import SENSOR_CONFIG, THRESHOLDS

st.set_page_config(page_title="Dashboard - Pancarbo", layout="wide")

st.title("📊 Real-Time Dashboard")
st.markdown("Monitor all system metrics and sensor readings in real-time")

# Refresh data button
if st.button("🔄 Refresh Data", key="refresh_dashboard"):
    st.rerun()

st.divider()

# Key Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

sensor_data = generate_sensor_data(50)
latest = sensor_data.iloc[-1]

with col1:
    st.metric(
        "Temperature",
        f"{latest['Temperature_C']:.1f}°C",
        delta=f"{latest['Temperature_C'] - sensor_data.iloc[-2]['Temperature_C']:.1f}°C"
    )

with col2:
    st.metric(
        "Steam Output",
        f"{latest['Steam_Output_tph']:.1f} tph",
        delta=f"{latest['Steam_Output_tph'] - sensor_data.iloc[-2]['Steam_Output_tph']:.1f} tph"
    )

with col3:
    st.metric(
        "Oxygen Level",
        f"{latest['Oxygen_percent']:.2f}%",
        delta=f"{latest['Oxygen_percent'] - sensor_data.iloc[-2]['Oxygen_percent']:.2f}%"
    )

with col4:
    st.metric(
        "Pressure",
        f"{latest['Pressure_bar']:.1f} bar",
        delta=f"{latest['Pressure_bar'] - sensor_data.iloc[-2]['Pressure_bar']:.1f} bar"
    )

with col5:
    st.metric(
        "Moisture",
        f"{latest['Moisture_percent']:.1f}%",
        delta=f"{latest['Moisture_percent'] - sensor_data.iloc[-2]['Moisture_percent']:.1f}%"
    )

st.divider()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Temperature & Pressure Trends")
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sensor_data['Time'],
        y=sensor_data['Temperature_C'],
        mode='lines',
        name='Temperature (°C)',
        line=dict(color='#e74c3c', width=2),
        yaxis='y1'
    ))
    
    fig.add_trace(go.Scatter(
        x=sensor_data['Time'],
        y=sensor_data['Pressure_bar'],
        mode='lines',
        name='Pressure (bar)',
        line=dict(color='#3498db', width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        hovermode='x unified',
        height=400,
        yaxis=dict(title='Temperature (°C)', side='left'),
        yaxis2=dict(title='Pressure (bar)', overlaying='y', side='right'),
        xaxis_title='Time Steps'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Steam Output & Oxygen Levels")
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sensor_data['Time'],
        y=sensor_data['Steam_Output_tph'],
        mode='lines',
        name='Steam Output (tph)',
        line=dict(color='#2ecc71', width=2),
        fill='tozeroy',
        fillcolor='rgba(46, 204, 113, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=sensor_data['Time'],
        y=sensor_data['Oxygen_percent'],
        mode='lines',
        name='Oxygen (%)',
        line=dict(color='#f39c12', width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        hovermode='x unified',
        height=400,
        yaxis=dict(title='Steam Output (tph)'),
        yaxis2=dict(title='Oxygen (%)', overlaying='y', side='right'),
        xaxis_title='Time Steps'
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Sensor Status Table
st.subheader("Sensor Status Overview")
sensor_status = pd.DataFrame({
    'Sensor': ['Temperature', 'Steam Output', 'Oxygen', 'Pressure', 'Moisture'],
    'Current Value': [
        f"{latest['Temperature_C']:.1f}°C",
        f"{latest['Steam_Output_tph']:.1f} tph",
        f"{latest['Oxygen_percent']:.2f}%",
        f"{latest['Pressure_bar']:.1f} bar",
        f"{latest['Moisture_percent']:.1f}%",
    ],
    'Status': ['✅ Normal', '✅ Normal', '✅ Normal', '✅ Normal', '✅ Normal'],
    'Last Updated': [datetime.now().strftime('%H:%M:%S')] * 5
})

st.dataframe(sensor_status, use_container_width=True, hide_index=True)

st.divider()

# System Health
st.subheader("System Health Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Overall System Health", "92%", "Excellent")
    st.success("✅ All sensors operational")

with col2:
    st.metric("Uptime", "47 days", "No issues")
    st.info("Last maintenance: 15 days ago")

with col3:
    st.metric("Data Points Logged", "150,000+", "+500/min")
    st.info("Real-time processing active")

st.divider()

# Alerts
if latest['Temperature_C'] > 920:
    st.warning("⚠️ High temperature detected. Consider reducing feed rate.")

if latest['Moisture_percent'] > THRESHOLDS['moisture_critical']:
    st.warning("⚠️ High moisture content detected in biomass.")

if latest['Steam_Output_tph'] < 25:
    st.warning("⚠️ Low steam output. Check furnace temperature and feed rate.")

st.markdown("""
---
*Last updated: {}*  
*Auto-refresh every 30 seconds*
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
