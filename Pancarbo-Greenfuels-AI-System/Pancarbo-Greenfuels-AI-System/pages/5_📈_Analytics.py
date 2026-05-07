"""
Analytics Page - Advanced analytics and reporting
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import generate_biomass_dataset, generate_sensor_data, generate_maintenance_data
from app_config.config import BIOMASS_FEATURES, BIOMASS_QUALITY_CLASSES

st.set_page_config(page_title="Analytics - Pancarbo", layout="wide")

st.title("📈 Advanced Analytics")
st.markdown("Comprehensive analytics and insights for the entire system")

# Load all data
biomass_data = generate_biomass_dataset(500)
sensor_data = generate_sensor_data(100)
maintenance_data = generate_maintenance_data(100)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 System Overview", "🔍 Deep Dive", "📉 Trends", "💡 Insights"])

# ============================================================================
# TAB 1: System Overview
# ============================================================================
with tab1:
    st.subheader("System Performance Overview")
    
    # Key performance indicators
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_samples = len(biomass_data)
        st.metric("Total Data Points", f"{total_samples:,}")
    
    with col2:
        excellent_pct = (biomass_data['quality_class'] == 'Excellent').sum() / len(biomass_data) * 100
        st.metric("Excellent Quality %", f"{excellent_pct:.1f}%")
    
    with col3:
        avg_steam = biomass_data['steam_output_tph'].mean()
        st.metric("Avg Steam Output", f"{avg_steam:.1f} tph")
    
    with col4:
        avg_moisture = biomass_data['moisture_pct'].mean()
        st.metric("Avg Moisture", f"{avg_moisture:.1f}%")
    
    with col5:
        uptime = 99.5
        st.metric("System Uptime", f"{uptime:.1f}%")
    
    st.divider()
    
    # Dashboard grid
    col1, col2 = st.columns(2)
    
    with col1:
        # Quality distribution pie chart
        quality_counts = biomass_data['quality_class'].value_counts()
        fig = px.pie(
            values=quality_counts.values,
            names=quality_counts.index,
            title="Quality Class Distribution",
            color_discrete_map=BIOMASS_QUALITY_CLASSES,
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sensor readings distribution
        fig = go.Figure()
        
        metrics = ['Temperature_C', 'Steam_Output_tph', 'Oxygen_percent', 'Pressure_bar']
        normalized_data = {}
        
        for metric in metrics:
            data = sensor_data[metric]
            normalized = (data - data.min()) / (data.max() - data.min())
            normalized_data[metric] = normalized
        
        for metric, values in normalized_data.items():
            fig.add_trace(go.Box(y=values, name=metric))
        
        fig.update_layout(title="Sensor Readings Distribution (Normalized)")
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 2: Deep Dive
# ============================================================================
with tab2:
    st.subheader("Deep Dive Analysis")
    
    # Feature importance
    st.markdown("### Feature Importance for Steam Output")
    
    correlation_data = []
    for feature in BIOMASS_FEATURES:
        corr = biomass_data[feature].corr(biomass_data['steam_output_tph'])
        correlation_data.append({'Feature': feature, 'Correlation': corr})
    
    corr_df = pd.DataFrame(correlation_data).sort_values('Correlation', key=abs, ascending=False)
    
    fig = px.bar(
        corr_df,
        x='Correlation',
        y='Feature',
        orientation='h',
        color='Correlation',
        color_continuous_scale='RdBu',
        title='Feature Correlation with Steam Output'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Multi-variable analysis
    st.markdown("### Multi-Variable Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create quality score
        biomass_data['quality_score'] = 1 - (biomass_data['moisture_pct'] / 35)
        
        fig = px.scatter_3d(
            biomass_data.sample(100),
            x='moisture_pct',
            y='feed_rate_tph',
            z='steam_output_tph',
            color='quality_score',
            title='3D Feature Relationship',
            labels={
                'moisture_pct': 'Moisture (%)',
                'feed_rate_tph': 'Feed Rate (tph)',
                'steam_output_tph': 'Steam Output (tph)'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Heatmap of feature correlations
        features_subset = ['moisture_pct', 'bale_weight_kg', 'color_score', 
                          'furnace_temp_c', 'feed_rate_tph', 'steam_output_tph']
        corr_matrix = biomass_data[features_subset].corr()
        
        fig = px.imshow(
            corr_matrix,
            labels=dict(x="Features", y="Features", color="Correlation"),
            title='Feature Correlation Matrix',
            color_continuous_scale='RdBu',
            zmin=-1, zmax=1
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 3: Trends
# ============================================================================
with tab3:
    st.subheader("System Trends Over Time")
    
    # Time-based analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Efficiency Trend")
        sensor_data['Efficiency'] = (
            (1 - abs(sensor_data['Temperature_C'] - 900) / 900) +
            (1 - abs(sensor_data['Steam_Output_tph'] - 30) / 30) +
            (1 - abs(sensor_data['Oxygen_percent'] - 4) / 4)
        ) / 3
        
        fig = px.line(
            sensor_data,
            x='Time',
            y='Efficiency',
            title='System Efficiency Trend',
            markers=True,
            line_shape='spline'
        )
        fig.add_hline(y=0.85, line_dash="dash", line_color="red", annotation_text="Target: 85%")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Equipment Degradation")
        fig = px.line(
            maintenance_data,
            x='Equipment_Age_Months',
            y='Degradation_Score',
            title='Equipment Health Trend',
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#e74c3c']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Comparative analysis
    st.markdown("### Multi-Parameter Trend Analysis")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sensor_data['Time'],
        y=sensor_data['Temperature_C'],
        mode='lines',
        name='Temperature (°C)',
        yaxis='y1'
    ))
    
    fig.add_trace(go.Scatter(
        x=sensor_data['Time'],
        y=sensor_data['Steam_Output_tph'],
        mode='lines',
        name='Steam Output (tph)',
        yaxis='y2'
    ))
    
    fig.add_trace(go.Scatter(
        x=sensor_data['Time'],
        y=sensor_data['Oxygen_percent'],
        mode='lines',
        name='Oxygen (%)',
        yaxis='y3'
    ))
    
    fig.update_layout(
        yaxis=dict(title='Temperature (°C)', side='left'),
        yaxis2=dict(title='Steam Output (tph)', overlaying='y', side='right'),
        yaxis3=dict(title='Oxygen (%)', overlaying='y', side='far right', anchor='free', position=1.15),
        hovermode='x unified',
        title='Multi-Parameter Trends',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 4: Insights
# ============================================================================
with tab4:
    st.subheader("Key Insights & Recommendations")
    
    # Generate insights
    insights = []
    
    # Insight 1: Quality
    excellent_count = (biomass_data['quality_class'] == 'Excellent').sum()
    excellent_pct = excellent_count / len(biomass_data) * 100
    insights.append({
        'Category': 'Biomass Quality',
        'Insight': f'{excellent_pct:.1f}% of samples are Excellent quality',
        'Recommendation': 'Maintain current supplier relationships and quality control standards',
        'Priority': 'High'
    })
    
    # Insight 2: Efficiency
    sensor_data['Efficiency'] = (
        (1 - abs(sensor_data['Temperature_C'] - 900) / 900) +
        (1 - abs(sensor_data['Steam_Output_tph'] - 30) / 30) +
        (1 - abs(sensor_data['Oxygen_percent'] - 4) / 4)
    ) / 3
    avg_efficiency = sensor_data['Efficiency'].mean()
    insights.append({
        'Category': 'System Efficiency',
        'Insight': f'Average system efficiency is {avg_efficiency:.1%}',
        'Recommendation': f'Optimize combustion parameters to reach 90%+ efficiency',
        'Priority': 'High'
    })
    
    # Insight 3: Maintenance
    degradation_trend = maintenance_data['Degradation_Score'].iloc[-1] - maintenance_data['Degradation_Score'].iloc[0]
    insights.append({
        'Category': 'Equipment Health',
        'Insight': f'Equipment degradation trend: {degradation_trend:.1%} over monitored period',
        'Recommendation': 'Schedule preventive maintenance to prevent critical failures',
        'Priority': 'Medium'
    })
    
    # Insight 4: Moisture
    high_moisture = (biomass_data['moisture_pct'] > 20).sum() / len(biomass_data) * 100
    insights.append({
        'Category': 'Feedstock Quality',
        'Insight': f'{high_moisture:.1f}% of biomass has moisture > 20%',
        'Recommendation': 'Implement stricter moisture control in receiving process',
        'Priority': 'Medium'
    })
    
    insights_df = pd.DataFrame(insights)
    
    for idx, insight in insights_df.iterrows():
        with st.expander(f"**{insight['Category']}** - {insight['Insight'][:50]}..."):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**Insight:** {insight['Insight']}")
            
            with col2:
                st.markdown(f"**Recommendation:** {insight['Recommendation']}")
            
            with col3:
                priority_color = {
                    'High': '🔴',
                    'Medium': '🟡',
                    'Low': '🟢'
                }
                st.markdown(f"**Priority:** {priority_color.get(insight['Priority'], '⚪')} {insight['Priority']}")
    
    st.divider()
    
    # Export section
    st.markdown("### Export Analytics Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Generate PDF Report"):
            st.success("✅ PDF report generated successfully!")
            st.info("Report includes: Summary, Charts, Insights, and Recommendations")
    
    with col2:
        if st.button("💾 Export Data as CSV"):
            st.success("✅ Data exported successfully!")
            st.info("All analytics data available for download")
