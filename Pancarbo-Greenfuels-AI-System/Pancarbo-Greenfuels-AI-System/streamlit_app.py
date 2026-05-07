"""
Main Streamlit Application
Pancarbo Greenfuels Industrial AI System
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app_config.config import STREAMLIT_CONFIG, APP_NAME, APP_VERSION, APP_DESCRIPTION
from src.utils import generate_biomass_dataset, generate_sensor_data

# Configure page
st.set_page_config(**STREAMLIT_CONFIG)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    .status-good { color: #2ecc71; font-weight: bold; }
    .status-warning { color: #f39c12; font-weight: bold; }
    .status-critical { color: #e74c3c; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Main header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="main-header">
        <h1>🌾 Pancarbo Greenfuels</h1>
        <h3>Industrial AI Optimization System</h3>
        <p>v{}</p>
    </div>
    """.format(APP_VERSION), unsafe_allow_html=True)

st.markdown(f"**{APP_DESCRIPTION}**")
st.divider()

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x150?text=Pancarbo+Logo", use_column_width=True)
    st.markdown("### About")
    st.info("""
    **Pancarbo Greenfuels** is an advanced AI platform designed to optimize 
    biomass-based industrial processes through predictive analytics, machine learning, 
    and real-time monitoring.
    """)
    
    st.markdown("### Features")
    features = [
        "✅ Biomass Quality Prediction",
        "✅ Boiler Efficiency Optimization",
        "✅ Predictive Maintenance",
        "✅ Real-Time Monitoring",
        "✅ SHAP Explainability",
        "✅ Anomaly Detection",
    ]
    for feature in features:
        st.markdown(feature)
    
    st.divider()
    st.markdown("### Navigation")
    st.markdown("""
    Use the pages in the sidebar to navigate through different modules:
    - **Dashboard**: Real-time monitoring and overview
    - **Biomass Analyzer**: Quality prediction and analysis
    - **Boiler Optimizer**: Efficiency optimization
    - **Maintenance**: Predictive maintenance insights
    - **Analytics**: Advanced analytics and reporting
    """)

# Main content
st.markdown("## Welcome to Pancarbo AI Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("System Status", "✅ Operational", "+5%")

with col2:
    st.metric("Processing Capacity", "92%", "-2%")

with col3:
    st.metric("Biomass Quality", "Good", "+3%")

with col4:
    st.metric("Efficiency Score", "87%", "+4%")

st.divider()

# Key sections
st.markdown("### Quick Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Current System Metrics")
    sensor_data = generate_sensor_data(10)
    latest = sensor_data.iloc[-1]
    
    st.markdown(f"""
    - **Temperature**: {latest['Temperature_C']:.1f}°C
    - **Steam Output**: {latest['Steam_Output_tph']:.1f} tph
    - **Oxygen Level**: {latest['Oxygen_percent']:.1f}%
    - **Pressure**: {latest['Pressure_bar']:.1f} bar
    - **Moisture**: {latest['Moisture_percent']:.1f}%
    """)
    
    st.success("✅ All sensors within normal range")

with col2:
    st.markdown("#### Recent Predictions")
    biomass_data = generate_biomass_dataset(5)
    
    for idx, row in biomass_data.iterrows():
        quality = row['quality_class']
        color_map = {
            'Excellent': '🟢',
            'Good': '🔵',
            'Marginal': '🟡',
            'Reject': '🔴'
        }
        st.markdown(f"{color_map.get(quality, '⚪')} **{quality}** - Moisture: {row['moisture_pct']:.1f}%")

st.divider()

# Navigation info
st.markdown("### Next Steps")
st.info("""
👈 **Select a page from the sidebar** to explore:
- **Dashboard** - Real-time system monitoring
- **Biomass Analyzer** - Predict and analyze biomass quality
- **Boiler Optimizer** - Optimize boiler efficiency
- **Maintenance** - Get predictive maintenance recommendations
- **Analytics** - In-depth analysis and insights
""")

# Footer
st.divider()
st.markdown("""
---
<div style='text-align: center; color: #888; font-size: 0.9em;'>
    <p>Pancarbo Greenfuels AI System | v{} | © 2024 Pancarbo AI</p>
    <p><a href='#' style='color: #667eea; text-decoration: none;'>Documentation</a> | 
       <a href='#' style='color: #667eea; text-decoration: none;'>GitHub</a> | 
       <a href='#' style='color: #667eea; text-decoration: none;'>Support</a></p>
</div>
""".format(APP_VERSION), unsafe_allow_html=True)
