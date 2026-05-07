"""
Configuration module for Pancarbo Greenfuels AI System
Manages all configuration settings and environment variables
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# Ensure directories exist
for directory in [DATA_DIR, MODELS_DIR, REPORTS_DIR, NOTEBOOKS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Application settings
APP_NAME = "Pancarbo Greenfuels Industrial AI System"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "End-to-end Industrial AI platform for biomass quality prediction and boiler optimization"
AUTHOR = "Pancarbo AI Team"

# Streamlit configuration
STREAMLIT_CONFIG = {
    "page_title": "Pancarbo AI Dashboard",
    "page_icon": "🌾",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Model configuration
MODEL_CONFIG = {
    "biomass_prediction": {
        "name": "Biomass Quality Predictor",
        "type": "XGBoost",
        "version": "1.0"
    },
    "boiler_efficiency": {
        "name": "Boiler Efficiency Optimizer",
        "type": "RandomForest",
        "version": "1.0"
    },
    "predictive_maintenance": {
        "name": "Predictive Maintenance",
        "type": "LightGBM",
        "version": "1.0"
    },
}

# Feature configuration for biomass prediction
BIOMASS_FEATURES = [
    'moisture_pct',
    'bale_weight_kg',
    'parali_fraction',
    'color_score',
    'texture_uniformity',
    'foreign_matter_score',
    'harvest_season',
    'vendor_distance_km',
    'feed_rate_tph',
    'furnace_temp_c'
]

BIOMASS_TARGET = 'steam_output_tph'

BIOMASS_QUALITY_CLASSES = {
    'Excellent': '#2ecc71',
    'Good': '#3498db',
    'Marginal': '#f39c12',
    'Reject': '#e74c3c'
}

# Sensor configuration
SENSOR_CONFIG = {
    "temperature": {
        "unit": "°C",
        "min": 800,
        "max": 1000,
        "optimal_range": (880, 920)
    },
    "steam_output": {
        "unit": "tph",
        "min": 10,
        "max": 100,
        "optimal_range": (28, 35)
    },
    "oxygen": {
        "unit": "%",
        "min": 1,
        "max": 10,
        "optimal_range": (3, 5)
    },
    "pressure": {
        "unit": "bar",
        "min": 20,
        "max": 40,
        "optimal_range": (30, 35)
    },
    "moisture": {
        "unit": "%",
        "min": 3,
        "max": 35,
        "optimal_range": (8, 12)
    }
}

# Threshold settings
THRESHOLDS = {
    "moisture_critical": 20,
    "efficiency_warning": 0.80,
    "maintenance_risk": 0.75,
    "anomaly_sensitivity": 0.95
}

# Visualization settings
VISUALIZATION = {
    "colorscale": "Viridis",
    "theme": "plotly_dark",
    "height": 500,
    "width": 800,
}

# Cache settings
CACHE_TTL = 3600  # seconds
ENABLE_CACHE = True

# Debug and logging
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Deployment settings
DEPLOYMENT_PLATFORM = os.getenv("DEPLOYMENT_PLATFORM", "LOCAL")  # LOCAL, STREAMLIT_CLOUD, RENDER, HEROKU
SECURE_MODE = os.getenv("SECURE_MODE", "False").lower() == "true"

# Database settings (if needed)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///pancarbo.db")
