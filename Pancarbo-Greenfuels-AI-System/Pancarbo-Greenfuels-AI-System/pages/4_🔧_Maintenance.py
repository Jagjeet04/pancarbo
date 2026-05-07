"""
Maintenance Page - Predictive maintenance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import generate_maintenance_data
from app_config.config import THRESHOLDS

st.set_page_config(page_title="Maintenance - Pancarbo", layout="wide")

st.title("🔧 Predictive Maintenance")
st.markdown("Get AI-powered maintenance recommendations and track equipment health")

# Load maintenance data
maintenance_data = generate_maintenance_data(100)

# Tabs
tab1, tab2, tab3 = st.tabs(["🚨 Alerts & Recommendations", "📊 Equipment Health", "📋 Maintenance History"])

# ============================================================================
# TAB 1: Alerts & Recommendations
# ============================================================================
with tab1:
    st.subheader("Active Alerts & Recommendations")
    
    # Get latest equipment status
    latest_status = maintenance_data.iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Degradation Score",
            f"{latest_status['Degradation_Score']:.2%}",
            delta=f"{latest_status['Degradation_Score'] - maintenance_data.iloc[-2]['Degradation_Score']:.2%}"
        )
    
    with col2:
        st.metric(
            "Risk Level",
            f"{latest_status['Risk_Level']:.2%}",
            delta_color="inverse" if latest_status['Risk_Level'] > 0.7 else "normal"
        )
    
    with col3:
        remaining_life = max(0, (60 - latest_status['Equipment_Age_Months']) * (1 - latest_status['Degradation_Score']))
        st.metric(
            "Estimated Life Remaining",
            f"{remaining_life:.0f} days",
            help="Estimated days until maintenance is required"
        )
    
    st.divider()
    
    # Alert system
    alerts = []
    
    if latest_status['Degradation_Score'] > THRESHOLDS['maintenance_risk']:
        alerts.append({
            'Severity': '🔴 CRITICAL',
            'Component': 'Main Furnace',
            'Issue': 'High degradation detected',
            'Action': 'Schedule maintenance within 7 days',
            'Estimated_Cost': '$2,500 - $3,500'
        })
    
    if latest_status['Vibration_Level'] > 85:
        alerts.append({
            'Severity': '🟠 HIGH',
            'Component': 'Pump Assembly',
            'Issue': 'Elevated vibration levels',
            'Action': 'Inspect bearings and alignment',
            'Estimated_Cost': '$500 - $1,200'
        })
    
    if latest_status['Temperature_Deviation'] > 40:
        alerts.append({
            'Severity': '🟡 MEDIUM',
            'Component': 'Heat Exchanger',
            'Issue': 'Temperature deviation detected',
            'Action': 'Clean heat exchanger surfaces',
            'Estimated_Cost': '$300 - $600'
        })
    
    if latest_status['Noise_Level'] > 85:
        alerts.append({
            'Severity': '🔵 INFO',
            'Component': 'Fan System',
            'Issue': 'Unusual noise detected',
            'Action': 'Monitor and inspect at next maintenance',
            'Estimated_Cost': 'Included in routine maintenance'
        })
    
    if alerts:
        alerts_df = pd.DataFrame(alerts)
        st.dataframe(alerts_df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No critical alerts. System operating normally.")
    
    st.divider()
    
    # Maintenance recommendations
    st.markdown("### Recommended Maintenance Actions")
    
    recommendations = [
        {
            'Task': 'Oil Change',
            'Interval': 'Every 500 hours',
            'Last Performed': '45 hours ago',
            'Next Due': 'In 455 hours',
            'Priority': 'Medium'
        },
        {
            'Task': 'Filter Replacement',
            'Interval': 'Every 1000 hours',
            'Last Performed': '120 hours ago',
            'Next Due': 'In 880 hours',
            'Priority': 'Low'
        },
        {
            'Task': 'Bearing Inspection',
            'Interval': 'Every 2000 hours',
            'Last Performed': '450 hours ago',
            'Next Due': 'In 1550 hours',
            'Priority': 'Medium'
        },
        {
            'Task': 'Seal Replacement',
            'Interval': 'Every 5000 hours',
            'Last Performed': '3200 hours ago',
            'Next Due': 'In 1800 hours',
            'Priority': 'High'
        },
    ]
    
    rec_df = pd.DataFrame(recommendations)
    st.dataframe(rec_df, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 2: Equipment Health
# ============================================================================
with tab2:
    st.subheader("Equipment Health Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Degradation Trend")
        fig = px.line(
            maintenance_data,
            x='Equipment_Age_Months',
            y='Degradation_Score',
            title='Equipment Degradation Over Time',
            markers=True,
            color_discrete_sequence=['#e74c3c']
        )
        fig.add_hline(
            y=THRESHOLDS['maintenance_risk'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Maintenance Threshold ({THRESHOLDS['maintenance_risk']:.0%})"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Risk Level Distribution")
        fig = px.area(
            maintenance_data,
            x='Equipment_Age_Months',
            y='Risk_Level',
            title='Overall Risk Level Progression',
            color_discrete_sequence=['#f39c12']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Component analysis
    st.markdown("### Component Health Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Vibration Levels")
        fig = px.line(
            maintenance_data,
            x='Equipment_Age_Months',
            y='Vibration_Level',
            title='Vibration Monitoring',
            color_discrete_sequence=['#3498db']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Temperature Deviation")
        fig = px.line(
            maintenance_data,
            x='Equipment_Age_Months',
            y='Temperature_Deviation',
            title='Temperature Monitoring',
            color_discrete_sequence=['#2ecc71']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown("#### Noise Level")
        fig = px.line(
            maintenance_data,
            x='Equipment_Age_Months',
            y='Noise_Level',
            title='Noise Level Monitoring',
            color_discrete_sequence=['#9b59b6']
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 3: Maintenance History
# ============================================================================
with tab3:
    st.subheader("Maintenance History & Schedule")
    
    # Historical maintenance log
    maintenance_log = pd.DataFrame([
        {
            'Date': '2024-04-15',
            'Component': 'Main Furnace',
            'Service': 'Annual Inspection',
            'Duration': '8 hours',
            'Cost': '$3,200',
            'Technician': 'John Smith',
            'Status': '✅ Completed'
        },
        {
            'Date': '2024-03-22',
            'Component': 'Pump Assembly',
            'Service': 'Bearing Replacement',
            'Duration': '4 hours',
            'Cost': '$1,800',
            'Technician': 'Maria Garcia',
            'Status': '✅ Completed'
        },
        {
            'Date': '2024-02-10',
            'Component': 'Heat Exchanger',
            'Service': 'Cleaning & Inspection',
            'Duration': '3 hours',
            'Cost': '$500',
            'Technician': 'Ahmed Hassan',
            'Status': '✅ Completed'
        },
        {
            'Date': '2024-01-28',
            'Component': 'Filter System',
            'Service': 'Filter Replacement',
            'Duration': '1.5 hours',
            'Cost': '$300',
            'Technician': 'Sarah Chen',
            'Status': '✅ Completed'
        },
    ])
    
    st.markdown("#### Past Maintenance")
    st.dataframe(maintenance_log, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Upcoming schedule
    st.markdown("#### Upcoming Schedule")
    
    upcoming = pd.DataFrame([
        {
            'Scheduled_Date': '2024-06-15',
            'Component': 'Main Furnace',
            'Service': 'Annual Inspection',
            'Estimated_Duration': '8 hours',
            'Estimated_Cost': '$3,200',
            'Status': '📅 Scheduled'
        },
        {
            'Scheduled_Date': '2024-07-01',
            'Component': 'Pump Assembly',
            'Service': 'Seal Replacement',
            'Estimated_Duration': '6 hours',
            'Estimated_Cost': '$2,500',
            'Status': '📅 Scheduled'
        },
        {
            'Scheduled_Date': '2024-08-10',
            'Component': 'Heat Exchanger',
            'Service': 'Cleaning & Inspection',
            'Estimated_Duration': '3 hours',
            'Estimated_Cost': '$500',
            'Status': '📋 Pending Approval'
        },
    ])
    
    st.dataframe(upcoming, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Cost analysis
    st.markdown("#### Maintenance Cost Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Annual Maintenance Cost", "$8,400")
    
    with col2:
        st.metric("Cost per Operating Hour", "$2.80")
    
    with col3:
        st.metric("Maintenance Efficiency", "94%", help="Ratio of planned vs emergency maintenance")
    
    with col4:
        st.metric("Equipment Uptime", "99.2%", help="Percentage of operational time")
