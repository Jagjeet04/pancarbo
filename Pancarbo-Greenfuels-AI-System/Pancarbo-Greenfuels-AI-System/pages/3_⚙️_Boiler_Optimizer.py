"""
Boiler Optimizer Page - Efficiency optimization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import generate_sensor_data, calculate_summary_stats
from app_config.config import SENSOR_CONFIG

st.set_page_config(page_title="Boiler Optimizer - Pancarbo", layout="wide")

st.title("⚙️ Boiler Efficiency Optimizer")
st.markdown("Optimize boiler performance and energy efficiency")

# Load sensor data
sensor_data = generate_sensor_data(100)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Current Status", "🎯 Optimization", "📈 Historical Trends"])

# ============================================================================
# TAB 1: Current Status
# ============================================================================
with tab1:
    st.subheader("Current Boiler Performance")
    
    latest = sensor_data.iloc[-1]
    
    # Calculate efficiency
    optimal_temp = 900
    optimal_steam = 30
    optimal_oxygen = 4
    
    temp_efficiency = 1 - abs(latest['Temperature_C'] - optimal_temp) / optimal_temp
    steam_efficiency = 1 - abs(latest['Steam_Output_tph'] - optimal_steam) / optimal_steam
    oxygen_efficiency = 1 - abs(latest['Oxygen_percent'] - optimal_oxygen) / optimal_oxygen
    
    overall_efficiency = (temp_efficiency + steam_efficiency + oxygen_efficiency) / 3
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Efficiency",
            f"{overall_efficiency:.1%}",
            delta="+2.5%",
            delta_color="inverse" if overall_efficiency > 0.85 else "normal"
        )
    
    with col2:
        st.metric("Temperature Efficiency", f"{temp_efficiency:.1%}")
    
    with col3:
        st.metric("Steam Output Efficiency", f"{steam_efficiency:.1%}")
    
    with col4:
        st.metric("Oxygen Efficiency", f"{oxygen_efficiency:.1%}")
    
    st.divider()
    
    # Real-time performance gauge
    st.markdown("### Real-Time Performance Gauge")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=overall_efficiency * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Boiler Efficiency (%)"},
        delta={'reference': 85},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "#e74c3c"},
                {'range': [50, 75], 'color': "#f39c12"},
                {'range': [75, 100], 'color': "#2ecc71"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Operating conditions
    st.markdown("### Operating Conditions vs Optimal")
    
    col1, col2, col3 = st.columns(3)
    
    conditions = [
        ("Temperature", latest['Temperature_C'], 900, "°C"),
        ("Steam Output", latest['Steam_Output_tph'], 30, "tph"),
        ("Oxygen Level", latest['Oxygen_percent'], 4, "%"),
    ]
    
    for idx, (name, current, optimal, unit) in enumerate(conditions):
        with st.columns(3)[idx]:
            fig = go.Figure(go.Indicator(
                mode="number+delta",
                value=current,
                title=name,
                delta={'reference': optimal},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            fig.update_layout(height=150)
            st.plotly_chart(fig, use_container_width=True, use_container_height=True)

# ============================================================================
# TAB 2: Optimization
# ============================================================================
with tab2:
    st.subheader("Optimization Recommendations")
    st.info("Get AI-driven recommendations to improve boiler efficiency")
    
    # Analysis
    latest = sensor_data.iloc[-1]
    recommendations = []
    
    # Temperature analysis
    if latest['Temperature_C'] < 880:
        recommendations.append({
            'Parameter': 'Temperature',
            'Current': f"{latest['Temperature_C']:.1f}°C",
            'Recommendation': 'Increase fuel feed rate',
            'Potential Gain': '2-3% efficiency',
            'Priority': 'High'
        })
    elif latest['Temperature_C'] > 920:
        recommendations.append({
            'Parameter': 'Temperature',
            'Current': f"{latest['Temperature_C']:.1f}°C",
            'Recommendation': 'Reduce fuel feed rate',
            'Potential Gain': '1-2% efficiency',
            'Priority': 'Medium'
        })
    
    # Oxygen analysis
    if latest['Oxygen_percent'] < 3:
        recommendations.append({
            'Parameter': 'Oxygen Level',
            'Current': f"{latest['Oxygen_percent']:.2f}%",
            'Recommendation': 'Increase air intake',
            'Potential Gain': '1% efficiency',
            'Priority': 'Medium'
        })
    elif latest['Oxygen_percent'] > 5:
        recommendations.append({
            'Parameter': 'Oxygen Level',
            'Current': f"{latest['Oxygen_percent']:.2f}%",
            'Recommendation': 'Optimize combustion air',
            'Potential Gain': '1-2% efficiency',
            'Priority': 'High'
        })
    
    # Steam output analysis
    if latest['Steam_Output_tph'] < 28:
        recommendations.append({
            'Parameter': 'Steam Output',
            'Current': f"{latest['Steam_Output_tph']:.1f} tph",
            'Recommendation': 'Increase input biomass quality',
            'Potential Gain': '3-5% efficiency',
            'Priority': 'High'
        })
    
    if recommendations:
        recommendations_df = pd.DataFrame(recommendations)
        
        # Display with color coding
        def color_priority(val):
            if val == 'High':
                return 'background-color: #e74c3c; color: white'
            elif val == 'Medium':
                return 'background-color: #f39c12; color: white'
            else:
                return 'background-color: #2ecc71; color: white'
        
        st.dataframe(
            recommendations_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Priority': st.column_config.TextColumn(
                    "Priority",
                    width="small",
                )
            }
        )
    else:
        st.success("✅ All parameters are within optimal ranges!")
    
    st.divider()
    
    # Optimization controls
    st.markdown("### Manual Optimization Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Temperature Control")
        temp_adjustment = st.slider(
            "Adjust fuel feed rate",
            -10, 10, 0,
            help="Negative values reduce, positive values increase feed rate"
        )
        if temp_adjustment != 0:
            st.info(f"Fuel feed adjustment: {temp_adjustment:+d}%")
    
    with col2:
        st.markdown("#### Air Control")
        air_adjustment = st.slider(
            "Adjust air intake",
            -10, 10, 0,
            help="Negative values reduce, positive values increase oxygen"
        )
        if air_adjustment != 0:
            st.info(f"Air intake adjustment: {air_adjustment:+d}%")
    
    with col3:
        st.markdown("#### Pressure Control")
        pressure_target = st.slider(
            "Set target pressure",
            20, 40, 32,
            help="Target operating pressure in bar"
        )
        st.info(f"Target pressure: {pressure_target} bar")

# ============================================================================
# TAB 3: Historical Trends
# ============================================================================
with tab3:
    st.subheader("Historical Performance Analysis")
    
    # Efficiency over time
    sensor_data['Efficiency'] = (
        (1 - abs(sensor_data['Temperature_C'] - 900) / 900) +
        (1 - abs(sensor_data['Steam_Output_tph'] - 30) / 30) +
        (1 - abs(sensor_data['Oxygen_percent'] - 4) / 4)
    ) / 3
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Efficiency Trend")
        fig = px.line(
            sensor_data,
            x='Time',
            y='Efficiency',
            title='Boiler Efficiency Over Time',
            markers=True
        )
        fig.add_hline(y=0.85, line_dash="dash", line_color="red", annotation_text="Target: 85%")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Parameter Stability")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sensor_data['Time'],
            y=sensor_data['Temperature_C'],
            name='Temperature (°C)',
            line=dict(color='#e74c3c')
        ))
        fig.add_hline(y=900, line_dash="dash", line_color="gray", annotation_text="Optimal: 900°C")
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Performance statistics
    st.markdown("### Performance Statistics")
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        avg_efficiency = sensor_data['Efficiency'].mean()
        st.metric("Average Efficiency", f"{avg_efficiency:.1%}")
    
    with stats_col2:
        max_efficiency = sensor_data['Efficiency'].max()
        st.metric("Peak Efficiency", f"{max_efficiency:.1%}")
    
    with stats_col3:
        min_efficiency = sensor_data['Efficiency'].min()
        st.metric("Minimum Efficiency", f"{min_efficiency:.1%}")
    
    with stats_col4:
        std_efficiency = sensor_data['Efficiency'].std()
        st.metric("Stability (Std Dev)", f"{std_efficiency:.1%}")
