"""
Biomass Analyzer Page - Quality prediction
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import (
    generate_biomass_dataset, validate_biomass_input,
    calculate_summary_stats, get_quality_color, BIOMASS_QUALITY_CLASSES
)
from app_config.config import BIOMASS_FEATURES, BIOMASS_TARGET

st.set_page_config(page_title="Biomass Analyzer - Pancarbo", layout="wide")

st.title("🌾 Biomass Quality Analyzer")
st.markdown("Predict and analyze biomass quality using AI models")

# Load data
biomass_data = generate_biomass_dataset(500)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis", "🎯 Prediction", "📈 Statistics", "📋 Data"])

# ============================================================================
# TAB 1: Analysis
# ============================================================================
with tab1:
    st.subheader("Biomass Quality Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Quality class distribution
        quality_counts = biomass_data['quality_class'].value_counts()
        fig = px.pie(
            values=quality_counts.values,
            names=quality_counts.index,
            title="Quality Class Distribution",
            color_discrete_map=BIOMASS_QUALITY_CLASSES
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Moisture impact
        fig = px.box(
            biomass_data,
            x='quality_class',
            y='moisture_pct',
            title="Moisture Content by Quality Class",
            color='quality_class',
            color_discrete_map=BIOMASS_QUALITY_CLASSES
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Feature correlations
    st.subheader("Feature Correlation with Steam Output")
    
    correlation_data = []
    for feature in BIOMASS_FEATURES:
        corr = biomass_data[feature].corr(biomass_data[BIOMASS_TARGET])
        correlation_data.append({'Feature': feature, 'Correlation': corr})
    
    corr_df = pd.DataFrame(correlation_data).sort_values('Correlation', key=abs, ascending=False)
    
    fig = px.bar(
        corr_df,
        x='Correlation',
        y='Feature',
        orientation='h',
        title='Feature Importance (Correlation with Steam Output)',
        color='Correlation',
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # 2D Scatter plots
    st.subheader("Feature Relationships")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            biomass_data,
            x='moisture_pct',
            y='steam_output_tph',
            color='quality_class',
            title='Moisture vs Steam Output',
            color_discrete_map=BIOMASS_QUALITY_CLASSES,
            trendline='ols'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            biomass_data,
            x='color_score',
            y='steam_output_tph',
            color='quality_class',
            title='Color Score vs Steam Output',
            color_discrete_map=BIOMASS_QUALITY_CLASSES,
            trendline='ols'
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 2: Prediction
# ============================================================================
with tab2:
    st.subheader("Predict Biomass Quality")
    st.info("Enter biomass characteristics to predict quality and steam output")
    
    col1, col2 = st.columns(2)
    
    with col1:
        moisture = st.slider("Moisture (%)", 3.0, 35.0, 12.0, 0.5, key="moisture_slider")
        bale_weight = st.slider("Bale Weight (kg)", 100.0, 280.0, 180.0, 5.0, key="bale_weight_slider")
        parali = st.slider("Parali Fraction", 0.0, 1.0, 0.85, 0.05, key="parali_slider")
        color_score = st.slider("Color Score", 0.1, 1.0, 0.8, 0.05, key="color_slider")
    
    with col2:
        texture = st.slider("Texture Uniformity", 0.1, 1.0, 0.8, 0.05, key="texture_slider")
        foreign = st.slider("Foreign Matter Score", 0.0, 1.0, 0.1, 0.05, key="foreign_slider")
        season = st.selectbox("Harvest Season", [0, 1], format_func=lambda x: "Off-season" if x == 0 else "Harvest season", key="season_select")
        vendor_dist = st.slider("Vendor Distance (km)", 1.0, 20.0, 10.0, 1.0, key="vendor_slider")
    
    col1, col2 = st.columns(2)
    with col1:
        feed_rate = st.slider("Feed Rate (tph)", 3.0, 6.0, 4.5, 0.1, key="feed_slider")
    
    with col2:
        furnace_temp = st.slider("Furnace Temp (°C)", 800.0, 1000.0, 900.0, 10.0, key="temp_slider")
    
    st.divider()
    
    # Prediction
    input_data = {
        'moisture_pct': moisture,
        'bale_weight_kg': bale_weight,
        'parali_fraction': parali,
        'color_score': color_score,
        'texture_uniformity': texture,
        'foreign_matter_score': foreign,
        'harvest_season': season,
        'vendor_distance_km': vendor_dist,
        'feed_rate_tph': feed_rate,
        'furnace_temp_c': furnace_temp
    }
    
    # Validate
    is_valid, message = validate_biomass_input(input_data)
    
    if is_valid:
        st.success("✅ " + message)
        
        # Simple prediction model (linear approximation)
        predicted_steam = (
            28.0
            - 0.35 * (moisture - 10)
            + 3.5 * (parali - 0.85)
            + 0.8 * (feed_rate - 4.5)
            + 0.01 * (furnace_temp - 900)
            + 0.5 * color_score
        )
        predicted_steam = max(18, min(32, predicted_steam))
        
        # Determine quality class
        if moisture < 10:
            quality = 'Excellent'
        elif moisture < 15:
            quality = 'Good'
        elif moisture < 20:
            quality = 'Marginal'
        else:
            quality = 'Reject'
        
        # Display results
        st.markdown("### Prediction Results")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Quality Class", quality, help="Based on moisture content")
        
        with col2:
            st.metric("Predicted Steam Output", f"{predicted_steam:.2f} tph", help="Tons per hour")
        
        with col3:
            quality_score = 1.0 - (moisture / 35)
            st.metric("Quality Score", f"{quality_score:.2%}", help="Inverse of moisture ratio")
        
        with col4:
            confidence = 0.87  # Simulated confidence
            st.metric("Model Confidence", f"{confidence:.1%}", help="Model prediction confidence")
        
        st.divider()
        
        # Detailed explanation
        with st.expander("📖 Prediction Details"):
            st.markdown(f"""
            **Input Parameters:**
            - Moisture: {moisture}%
            - Feed Rate: {feed_rate} tph
            - Furnace Temperature: {furnace_temp}°C
            - Color Score: {color_score}
            
            **Quality Assessment:**
            - Classification: {quality}
            - Primary Factor: Moisture content
            - Secondary Factors: Feed rate, furnace temperature
            
            **Predicted Output:**
            - Steam Output: {predicted_steam:.2f} tph
            - Expected Efficiency: Good
            - Recommendation: {f'Reduce moisture content' if moisture > 15 else 'Maintain current conditions'}
            """)
    else:
        st.error("❌ " + message)

# ============================================================================
# TAB 3: Statistics
# ============================================================================
with tab3:
    st.subheader("Statistical Summary")
    
    # Feature statistics
    st.markdown("### Feature Statistics")
    
    stats_data = []
    for feature in BIOMASS_FEATURES:
        stats = calculate_summary_stats(biomass_data, feature)
        stats_data.append({
            'Feature': feature,
            'Mean': f"{stats['mean']:.2f}",
            'Std Dev': f"{stats['std']:.2f}",
            'Min': f"{stats['min']:.2f}",
            'Max': f"{stats['max']:.2f}",
            'Median': f"{stats['median']:.2f}"
        })
    
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Quality class statistics
    st.markdown("### Quality Class Statistics")
    quality_stats = biomass_data.groupby('quality_class')[BIOMASS_TARGET].agg([
        'count', 'mean', 'std', 'min', 'max'
    ]).round(2)
    st.dataframe(quality_stats, use_container_width=True)

# ============================================================================
# TAB 4: Data View
# ============================================================================
with tab4:
    st.subheader("Dataset Viewer")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_quality = st.multiselect(
            "Filter by Quality Class",
            options=biomass_data['quality_class'].unique(),
            default=list(biomass_data['quality_class'].unique())
        )
    
    with col2:
        n_rows = st.number_input("Show rows", 5, 100, 10)
    
    filtered_data = biomass_data[biomass_data['quality_class'].isin(search_quality)].head(n_rows)
    st.dataframe(filtered_data, use_container_width=True, hide_index=True)
    
    # Download button
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="biomass_analysis.csv",
        mime="text/csv"
    )
