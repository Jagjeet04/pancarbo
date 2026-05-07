"""
Utility functions for Pancarbo Greenfuels AI System
Includes data generation, model utilities, and helper functions
"""

import numpy as np
import pandas as pd
import streamlit as st
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')

from app_config.config import (
    BIOMASS_FEATURES, BIOMASS_TARGET, BIOMASS_QUALITY_CLASSES,
    SENSOR_CONFIG, THRESHOLDS, BASE_DIR
)


# ============================================================================
# Data Generation Functions
# ============================================================================

def generate_biomass_dataset(n_samples: int = 2000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic biomass quality dataset
    
    Args:
        n_samples: Number of samples to generate
        seed: Random seed for reproducibility
        
    Returns:
        DataFrame with biomass features and target
    """
    np.random.seed(seed)
    n = n_samples

    # Moisture percentage (key quality indicator)
    moisture_pct = np.concatenate([
        np.random.normal(10, 2.5, int(n * 0.6)),
        np.random.normal(18, 3.0, int(n * 0.3)),
        np.random.normal(25, 2.0, int(n * 0.1))
    ])[:n]
    moisture_pct = np.clip(moisture_pct, 3, 35)

    # Other features
    bale_weight_kg = np.clip(np.random.normal(180, 25, n), 100, 280)
    parali_fraction = np.random.beta(18, 2, n)
    color_score = np.clip(1.0 - (moisture_pct/35) + np.random.normal(0, 0.08, n), 0.1, 1.0)
    texture_uniformity = np.clip(0.85 - 0.015*(moisture_pct - 10) + np.random.normal(0, 0.07, n), 0.1, 1.0)
    foreign_matter = np.clip(np.random.beta(1.5, 8, n), 0, 1)
    month = np.random.choice(range(1, 13), n)
    harvest_season = ((month >= 10) | (month <= 1)).astype(float)
    vendor_distance = np.random.uniform(1, 20, n)
    feed_rate_tph = np.random.uniform(3.5, 5.5, n)
    furnace_temp_c = np.clip(np.random.normal(900, 25, n), 820, 970)

    # Target: steam output (depends on biomass quality)
    steam_output_tph = (
        28.0
        - 0.35 * (moisture_pct - 10)
        + 3.5 * (parali_fraction - 0.85)
        + 0.8 * (feed_rate_tph - 4.5)
        + 0.01 * (furnace_temp_c - 900)
        + 0.5 * color_score
        + np.random.normal(0, 0.6, n)
    )
    steam_output_tph = np.clip(steam_output_tph, 18, 32)

    # Quality class based on moisture
    quality_class = pd.cut(
        moisture_pct, 
        bins=[0, 10, 15, 20, 100],
        labels=['Excellent', 'Good', 'Marginal', 'Reject']
    )

    return pd.DataFrame({
        'moisture_pct': moisture_pct,
        'bale_weight_kg': bale_weight_kg,
        'parali_fraction': parali_fraction,
        'color_score': color_score,
        'texture_uniformity': texture_uniformity,
        'foreign_matter_score': foreign_matter,
        'harvest_season': harvest_season,
        'vendor_distance_km': vendor_distance,
        'feed_rate_tph': feed_rate_tph,
        'furnace_temp_c': furnace_temp_c,
        'quality_class': quality_class,
        'steam_output_tph': steam_output_tph
    })


def generate_sensor_data(n_samples: int = 50) -> pd.DataFrame:
    """
    Generate synthetic real-time sensor data
    
    Args:
        n_samples: Number of time steps
        
    Returns:
        DataFrame with sensor readings
    """
    np.random.seed(None)  # Use current time for randomness
    
    time_steps = np.arange(n_samples)
    
    data = {
        "Time": time_steps,
        "Temperature_C": np.clip(
            900 + 20 * np.sin(time_steps/10) + np.random.normal(0, 5, n_samples),
            800, 1000
        ),
        "Steam_Output_tph": np.clip(
            28 + 5 * np.sin(time_steps/15) + np.random.normal(0, 0.5, n_samples),
            18, 35
        ),
        "Oxygen_percent": np.clip(
            4 + 1.5 * np.cos(time_steps/12) + np.random.normal(0, 0.2, n_samples),
            1, 10
        ),
        "Pressure_bar": np.clip(
            32 + 2 * np.sin(time_steps/20) + np.random.normal(0, 0.3, n_samples),
            20, 40
        ),
        "Moisture_percent": np.clip(
            12 + 3 * np.sin((time_steps + 5)/18) + np.random.normal(0, 0.5, n_samples),
            3, 35
        ),
    }
    
    return pd.DataFrame(data)


def generate_maintenance_data(n_samples: int = 100) -> pd.DataFrame:
    """
    Generate synthetic predictive maintenance data
    
    Args:
        n_samples: Number of samples
        
    Returns:
        DataFrame with maintenance indicators
    """
    np.random.seed(42)
    
    # Generate degradation curves
    equipment_age = np.linspace(0, 60, n_samples)  # months
    
    # Degradation follows a curve
    degradation_pattern = 0.3 + 0.008 * equipment_age + 0.00005 * equipment_age**2
    degradation_pattern = np.clip(degradation_pattern + np.random.normal(0, 0.05, n_samples), 0.1, 1.0)
    
    # Risk level based on degradation
    risk_level = degradation_pattern
    maintenance_needed = risk_level > THRESHOLDS["maintenance_risk"]
    
    return pd.DataFrame({
        'Equipment_Age_Months': equipment_age,
        'Vibration_Level': degradation_pattern * 100,  # mm/s
        'Temperature_Deviation': degradation_pattern * 50,  # °C
        'Noise_Level': 70 + degradation_pattern * 20,  # dB
        'Degradation_Score': degradation_pattern,
        'Risk_Level': risk_level,
        'Maintenance_Recommended': maintenance_needed.astype(int)
    })


# ============================================================================
# Formatting and Display Functions
# ============================================================================

def format_metric(value: float, unit: str = "", decimals: int = 2) -> str:
    """Format a metric value with unit"""
    return f"{value:.{decimals}f} {unit}".strip()


def get_quality_color(quality_class: str) -> str:
    """Get color for quality class"""
    return BIOMASS_QUALITY_CLASSES.get(quality_class, "#95a5a6")


def get_status_icon(status: str) -> str:
    """Get emoji icon for status"""
    icons = {
        "good": "✅",
        "warning": "⚠️",
        "critical": "❌",
        "info": "ℹ️",
    }
    return icons.get(status.lower(), "•")


# ============================================================================
# Validation Functions
# ============================================================================

def validate_biomass_input(data: Dict[str, float]) -> Tuple[bool, str]:
    """
    Validate biomass input data
    
    Args:
        data: Dictionary of feature values
        
    Returns:
        Tuple of (is_valid, message)
    """
    # Check moisture
    if not (3 <= data.get('moisture_pct', 0) <= 35):
        return False, "Moisture must be between 3% and 35%"
    
    # Check temperature
    if not (800 <= data.get('furnace_temp_c', 0) <= 1000):
        return False, "Furnace temperature must be between 800°C and 1000°C"
    
    # Check feed rate
    if not (3 <= data.get('feed_rate_tph', 0) <= 6):
        return False, "Feed rate must be between 3 and 6 tph"
    
    return True, "Input data is valid"


def validate_sensor_data(sensor_readings: Dict[str, float]) -> Tuple[bool, List[str]]:
    """
    Validate sensor readings against normal ranges
    
    Args:
        sensor_readings: Dictionary of sensor values
        
    Returns:
        Tuple of (is_valid, list_of_warnings)
    """
    warnings_list = []
    
    for sensor_name, config in SENSOR_CONFIG.items():
        if sensor_name in sensor_readings:
            value = sensor_readings[sensor_name]
            if not (config["min"] <= value <= config["max"]):
                warnings_list.append(f"{sensor_name}: {value}{config['unit']} is out of range [{config['min']}, {config['max']}]")
    
    return len(warnings_list) == 0, warnings_list


# ============================================================================
# Caching and Performance Functions
# ============================================================================

@st.cache_data
def load_biomass_data(filepath: str = None) -> pd.DataFrame:
    """Load or generate biomass dataset with caching"""
    if filepath:
        try:
            return pd.read_csv(filepath)
        except FileNotFoundError:
            return generate_biomass_dataset()
    return generate_biomass_dataset()


@st.cache_data
def load_maintenance_data() -> pd.DataFrame:
    """Load or generate maintenance data with caching"""
    return generate_maintenance_data()


# ============================================================================
# Statistical Functions
# ============================================================================

def calculate_summary_stats(data: pd.DataFrame, column: str) -> Dict[str, float]:
    """Calculate summary statistics for a column"""
    return {
        "mean": data[column].mean(),
        "std": data[column].std(),
        "min": data[column].min(),
        "max": data[column].max(),
        "median": data[column].median(),
        "q25": data[column].quantile(0.25),
        "q75": data[column].quantile(0.75),
    }


def identify_outliers(data: pd.DataFrame, column: str, method: str = "iqr") -> pd.Series:
    """Identify outliers in a column"""
    if method == "iqr":
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        return (data[column] < Q1 - 1.5*IQR) | (data[column] > Q3 + 1.5*IQR)
    else:
        mean = data[column].mean()
        std = data[column].std()
        return np.abs((data[column] - mean) / std) > 3
