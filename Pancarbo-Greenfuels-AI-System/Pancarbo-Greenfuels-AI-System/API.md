# API Documentation - Pancarbo Greenfuels

## Overview

This document provides a complete API reference for the Pancarbo Greenfuels AI System modules.

## Table of Contents

- [app_config.config](#app_configconfig)
- [src.utils](#srcutils)
- [Streamlit Components](#streamlit-components)

---

## app_config.config

Configuration and constants module.

### Imports

```python
from app_config.config import (
    # Paths
    BASE_DIR,
    DATA_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    
    # Application
    APP_NAME,
    APP_VERSION,
    
    # Features
    BIOMASS_FEATURES,
    BIOMASS_TARGET,
    BIOMASS_QUALITY_CLASSES,
    
    # Configuration
    SENSOR_CONFIG,
    THRESHOLDS,
    MODEL_CONFIG,
    VISUALIZATION,
)
```

### Key Constants

#### Application Settings
```python
APP_NAME = "Pancarbo Greenfuels Industrial AI System"
APP_VERSION = "1.0.0"
DEPLOYMENT_PLATFORM = "LOCAL"  # or STREAMLIT_CLOUD, RENDER, HEROKU
```

#### Biomass Configuration
```python
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
```

#### Sensor Configuration
```python
SENSOR_CONFIG = {
    "temperature": {
        "unit": "°C",
        "min": 800,
        "max": 1000,
        "optimal_range": (880, 920)
    },
    # ... more sensors
}
```

#### Thresholds
```python
THRESHOLDS = {
    "moisture_critical": 20,
    "efficiency_warning": 0.80,
    "maintenance_risk": 0.75,
    "anomaly_sensitivity": 0.95
}
```

---

## src.utils

Utility functions for data generation, validation, and processing.

### Data Generation Functions

#### generate_biomass_dataset

Generate synthetic biomass quality dataset.

```python
from src.utils import generate_biomass_dataset

# Generate 2000 samples
df = generate_biomass_dataset(n_samples=2000, seed=42)

# Returns DataFrame with columns:
# - moisture_pct
# - bale_weight_kg
# - parali_fraction
# - color_score
# - texture_uniformity
# - foreign_matter_score
# - harvest_season
# - vendor_distance_km
# - feed_rate_tph
# - furnace_temp_c
# - quality_class
# - steam_output_tph
```

**Parameters:**
- `n_samples` (int): Number of samples to generate. Default: 2000
- `seed` (int): Random seed for reproducibility. Default: 42

**Returns:**
- `pd.DataFrame`: Generated dataset

#### generate_sensor_data

Generate synthetic real-time sensor data.

```python
from src.utils import generate_sensor_data

# Generate 50 time steps
df = generate_sensor_data(n_samples=50)

# Returns DataFrame with columns:
# - Time
# - Temperature_C
# - Steam_Output_tph
# - Oxygen_percent
# - Pressure_bar
# - Moisture_percent
```

#### generate_maintenance_data

Generate synthetic predictive maintenance data.

```python
from src.utils import generate_maintenance_data

df = generate_maintenance_data(n_samples=100)

# Returns DataFrame with columns:
# - Equipment_Age_Months
# - Vibration_Level
# - Temperature_Deviation
# - Noise_Level
# - Degradation_Score
# - Risk_Level
# - Maintenance_Recommended
```

### Validation Functions

#### validate_biomass_input

Validate biomass input data.

```python
from src.utils import validate_biomass_input

data = {
    'moisture_pct': 12.0,
    'furnace_temp_c': 900,
    'feed_rate_tph': 4.5,
    # ... other fields
}

is_valid, message = validate_biomass_input(data)

if is_valid:
    print(f"✓ {message}")  # Input data is valid
else:
    print(f"✗ {message}")  # Error message
```

**Returns:**
- `Tuple[bool, str]`: (is_valid, message)

#### validate_sensor_data

Validate sensor readings against normal ranges.

```python
from src.utils import validate_sensor_data

sensor_readings = {
    'temperature': 905,
    'oxygen': 4.2,
    'pressure': 32,
}

is_valid, warnings = validate_sensor_data(sensor_readings)

for warning in warnings:
    print(f"⚠️ {warning}")
```

**Returns:**
- `Tuple[bool, List[str]]`: (is_valid, list_of_warnings)

### Statistical Functions

#### calculate_summary_stats

Calculate summary statistics for a column.

```python
from src.utils import calculate_summary_stats

stats = calculate_summary_stats(df, 'moisture_pct')

print(stats['mean'])     # 12.5
print(stats['std'])      # 3.2
print(stats['median'])   # 12.0
```

**Returns:**
- `Dict[str, float]`: Dictionary with keys: mean, std, min, max, median, q25, q75

#### identify_outliers

Identify outliers in a column.

```python
from src.utils import identify_outliers

outliers = identify_outliers(df, 'steam_output_tph', method='iqr')
outlier_rows = df[outliers]
```

**Parameters:**
- `data` (pd.DataFrame): Input data
- `column` (str): Column to analyze
- `method` (str): 'iqr' (default) or 'zscore'

**Returns:**
- `pd.Series`: Boolean series indicating outliers

### Caching Functions

#### load_biomass_data

Load or generate biomass dataset with caching.

```python
import streamlit as st
from src.utils import load_biomass_data

# Automatically cached
df = load_biomass_data(filepath='data/biomass.csv')
# Or generates synthetic data if file not found
```

#### load_maintenance_data

Load or generate maintenance data with caching.

```python
from src.utils import load_maintenance_data

# Automatically cached
df = load_maintenance_data()
```

### Formatting Functions

#### format_metric

Format a metric value with unit.

```python
from src.utils import format_metric

result = format_metric(25.456, unit="°C", decimals=1)
print(result)  # "25.5 °C"
```

#### get_quality_color

Get color for quality class.

```python
from src.utils import get_quality_color

color = get_quality_color('Excellent')
print(color)  # "#2ecc71"
```

#### get_status_icon

Get emoji icon for status.

```python
from src.utils import get_status_icon

icon = get_status_icon('good')
print(icon)  # "✅"
```

---

## Streamlit Components

### Layout

All dashboard pages follow a common structure:

```python
import streamlit as st
from app_config.config import STREAMLIT_CONFIG

st.set_page_config(**STREAMLIT_CONFIG)

st.title("📊 Page Title")
st.markdown("Subtitle or description")

# Your content here
```

### Common Patterns

#### Metrics Display

```python
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Label", value="123", delta="+5%")

with col2:
    st.metric("Label", value="456", delta="-2%", delta_color="inverse")

with col3:
    st.metric("Label", value="789")
```

#### Tabs

```python
tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🎯 Prediction", "📈 Statistics"])

with tab1:
    st.write("Analysis content")

with tab2:
    st.write("Prediction content")

with tab3:
    st.write("Statistics content")
```

#### Data Display

```python
# DataFrame with custom options
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        'Status': st.column_config.TextColumn("Status", width="small")
    }
)

# Download button
csv = df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv"
)
```

#### Charts

```python
import plotly.express as px
import plotly.graph_objects as go

# Simple chart
fig = px.line(df, x='Time', y='Value', title='Trend')
st.plotly_chart(fig, use_container_width=True)

# Advanced gauge
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=85,
    title="Efficiency %",
    domain={'x': [0, 1], 'y': [0, 1]},
    gauge={'axis': {'range': [0, 100]}}
))
st.plotly_chart(fig, use_container_width=True)
```

---

## Example: Complete Integration

```python
import streamlit as st
import pandas as pd
from app_config.config import BIOMASS_FEATURES, THRESHOLDS
from src.utils import (
    generate_biomass_dataset,
    validate_biomass_input,
    calculate_summary_stats,
    format_metric,
)

# Page config
st.set_page_config(page_title="My Page", layout="wide")

# Load data
df = generate_biomass_dataset(500)

# Display metrics
col1, col2, col3 = st.columns(3)
with col1:
    avg_moisture = df['moisture_pct'].mean()
    st.metric("Avg Moisture", format_metric(avg_moisture, "%"))

# Validation example
user_input = {
    'moisture_pct': st.slider("Moisture %", 3, 35, 12),
    'furnace_temp_c': st.slider("Temperature °C", 800, 1000, 900),
}

is_valid, message = validate_biomass_input(user_input)
if is_valid:
    st.success(message)
else:
    st.error(message)

# Statistics
stats = calculate_summary_stats(df, 'steam_output_tph')
st.write(f"Mean: {stats['mean']:.2f}")
```

---

## Best Practices

1. **Always cache data loading**
   ```python
   @st.cache_data
   def load_data():
       return pd.read_csv('file.csv')
   ```

2. **Use configuration for constants**
   ```python
   from app_config.config import THRESHOLDS
   # Instead of hardcoding values
   ```

3. **Validate user input**
   ```python
   is_valid, msg = validate_biomass_input(data)
   if not is_valid:
       st.error(msg)
       return
   ```

4. **Format numbers for display**
   ```python
   st.write(f"Value: {format_metric(123.456, '°C', 1)}")
   ```

---

## Support

For more help:
- Check examples in `pages/` directory
- See full docs in `README.md`
- Review deployment guide in `DEPLOYMENT.md`

**Version:** 1.0.0  
**Last Updated:** 2024
