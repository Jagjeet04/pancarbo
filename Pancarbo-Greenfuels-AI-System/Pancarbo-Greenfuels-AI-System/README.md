
# 🌾 Pancarbo Greenfuels — Industrial AI Optimization System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)

**Pancarbo Greenfuels** is a comprehensive Industrial AI platform designed to optimize biomass-based energy systems through advanced machine learning, real-time monitoring, and predictive analytics.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Deployment](#deployment)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Pancarbo Greenfuels is an end-to-end Industrial AI platform focused on:

- **Biomass Quality Prediction** - Predict quality and steam output from raw materials
- **Boiler Efficiency Optimization** - Real-time performance monitoring and optimization
- **Predictive Maintenance** - AI-driven maintenance scheduling and anomaly detection
- **Explainable AI** - SHAP-based model explanations for transparency
- **Real-Time Monitoring** - Live dashboard with sensor data visualization
- **Reinforcement Learning** - Self-optimizing system parameters

## ✨ Features

### Dashboard
- 📊 **Real-Time Monitoring** - Live sensor data and system metrics
- 📈 **Advanced Analytics** - Comprehensive data analysis and insights
- 🎯 **Predictive Analytics** - Machine learning-based forecasts
- 🔧 **Maintenance Scheduling** - Predictive maintenance recommendations
- 📋 **Report Generation** - Professional PDF reports

### Core Functionality
- ✅ **Biomass Quality Assessment** - Classify biomass and predict steam output
- ✅ **Boiler Performance Optimization** - Real-time efficiency analysis
- ✅ **Equipment Health Monitoring** - Degradation tracking and alerts
- ✅ **Anomaly Detection** - Identify unusual patterns
- ✅ **Explainability** - SHAP-based model interpretability
- ✅ **Data Export** - CSV and Excel export capabilities

## 🛠 Tech Stack

| Category | Technology |
|----------|-----------|
| **Frontend** | Streamlit 1.28.1 |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **ML/AI** | XGBoost, LightGBM, CatBoost, Scikit-Learn |
| **Deep Learning** | PyTorch |
| **Reinforcement Learning** | Stable-Baselines3, Gymnasium |
| **Explainability** | SHAP |
| **Data Processing** | Pandas, NumPy, SciPy |
| **Deployment** | Docker, Streamlit Cloud, Render |
| **Backend** | Gunicorn, Werkzeug |

## 📁 Project Structure

```
Pancarbo-Greenfuels-AI-System/
│
├── streamlit_app.py                 # Main application entry point
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
├── docker-compose.yml              # Docker Compose setup
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
│
├── app_config/                     # Configuration module
│   └── config.py                   # Settings and constants
│
├── src/                            # Source code
│   └── utils.py                    # Utility functions and helpers
│
├── pages/                          # Streamlit multi-page apps
│   ├── 1_📊_Dashboard.py          # Real-time monitoring
│   ├── 2_🌾_Biomass_Analyzer.py   # Quality prediction
│   ├── 3_⚙️_Boiler_Optimizer.py   # Efficiency optimization
│   ├── 4_🔧_Maintenance.py        # Predictive maintenance
│   └── 5_📈_Analytics.py          # Advanced analytics
│
├── notebooks/                      # Jupyter notebooks
│   └── pancarbo_complete_final.ipynb
│
├── data/                           # Data directory (gitignored)
│   ├── biomass/
│   ├── fermentation/
│   └── images/
│
├── models/                         # Model directory (gitignored)
│   ├── project1/
│   └── project2/
│
├── reports/                        # Reports directory (gitignored)
│
└── .github/                        # GitHub configuration
    └── workflows/
        └── deploy.yml              # CI/CD workflow
```

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip or conda
- Git (for cloning the repository)
- Docker (optional, for containerization)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Pancarbo-Greenfuels-AI-System.git
cd Pancarbo-Greenfuels-AI-System
```

### 2. Create Virtual Environment

**Using venv:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Using conda:**
```bash
conda create -n pancarbo python=3.11
conda activate pancarbo
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

## 📖 Quick Start

### Run Locally

```bash
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501`

### Run with Docker

**Option 1: Docker Compose (Recommended)**
```bash
docker-compose up --build
```

**Option 2: Docker**
```bash
docker build -t pancarbo-app .
docker run -p 8501:8501 pancarbo-app
```

## 📚 Usage

### Navigating the Dashboard

1. **Home Page** (`streamlit_app.py`)
   - Overview of system status
   - Quick metrics and alerts
   - Navigation guide

2. **Dashboard** (`pages/1_📊_Dashboard.py`)
   - Real-time sensor monitoring
   - Temperature and pressure trends
   - System health overview

3. **Biomass Analyzer** (`pages/2_🌾_Biomass_Analyzer.py`)
   - Predict quality class (Excellent, Good, Marginal, Reject)
   - Forecast steam output
   - Analyze biomass characteristics

4. **Boiler Optimizer** (`pages/3_⚙️_Boiler_Optimizer.py`)
   - Optimize boiler efficiency
   - Parameter recommendations
   - Historical performance analysis

5. **Maintenance** (`pages/4_🔧_Maintenance.py`)
   - Equipment health monitoring
   - Maintenance recommendations
   - Service history and scheduling

6. **Analytics** (`pages/5_📈_Analytics.py`)
   - Advanced statistical analysis
   - Feature importance analysis
   - Trend analysis and insights

### Example: Making a Prediction

1. Navigate to **Biomass Analyzer**
2. Adjust the sliders for biomass characteristics:
   - Moisture percentage
   - Bale weight
   - Color score
   - Furnace temperature
3. Click to see predictions
4. Review quality classification and steam output forecast

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Connect your GitHub repository
5. Select the branch and main file (`streamlit_app.py`)
6. Deploy!

**Environment Variables:**
```
DEPLOYMENT_PLATFORM=STREAMLIT_CLOUD
```

### Deploy to Render

1. Create account on [render.com](https://render.com)
2. Connect your GitHub repository
3. Create new Web Service
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run streamlit_app.py --server.port=10000`
6. Add environment variables from `.env.example`
7. Deploy

**Important:** Set Streamlit port to 10000 for Render compatibility.

### Deploy to Heroku

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create `Procfile`:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableXsrfProtection = false" > ~/.streamlit/config.toml
   ```
4. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

### Docker Deployment

Push Docker image to registry:
```bash
docker build -t pancarbo-app:latest .
docker tag pancarbo-app:latest your-registry/pancarbo-app:latest
docker push your-registry/pancarbo-app:latest
```

## 📖 API Reference

### Configuration Module (`app_config/config.py`)

```python
from app_config.config import (
    BIOMASS_FEATURES,
    BIOMASS_TARGET,
    SENSOR_CONFIG,
    THRESHOLDS,
    MODEL_CONFIG
)
```

### Utility Functions (`src/utils.py`)

**Data Generation:**
```python
from src.utils import (
    generate_biomass_dataset,
    generate_sensor_data,
    generate_maintenance_data
)
```

**Validation:**
```python
from src.utils import (
    validate_biomass_input,
    validate_sensor_data
)
```

**Caching:**
```python
from src.utils import (
    load_biomass_data,
    load_maintenance_data
)
```

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

```
DEBUG=False
LOG_LEVEL=INFO
DEPLOYMENT_PLATFORM=LOCAL
SECURE_MODE=False
CACHE_TTL=3600
```

### Customization

Edit `app_config/config.py` to customize:
- Sensor ranges and thresholds
- Model configurations
- Quality class definitions
- Visualization settings
- Cache behavior

## 🧪 Testing

Run tests:
```bash
pytest
```

Run specific test:
```bash
pytest tests/test_utils.py -v
```

## 📊 Data

The application includes synthetic data generators for demonstration:
- **Biomass Dataset**: 2000 synthetic samples
- **Sensor Data**: Real-time simulated readings
- **Maintenance Data**: Equipment degradation simulation

Replace with real data by:
1. Add CSV files to `data/` directory
2. Update data loading in `src/utils.py`
3. Adjust feature mappings in `app_config/config.py`

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙋 Support

- 📧 Email: support@pancarbo.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 📖 Documentation: [Wiki](https://github.com/yourusername/Pancarbo-Greenfuels-AI-System/wiki)

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)

## 🔄 Version History

- **v1.0.0** (2024) - Initial release
  - Multi-page dashboard
  - Biomass quality prediction
  - Boiler optimization
  - Predictive maintenance
  - Advanced analytics

## ⭐ Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Machine learning powered by [Scikit-Learn](https://scikit-learn.org/), [XGBoost](https://xgboost.readthedocs.io/)
- Explainability with [SHAP](https://shap.readthedocs.io/)
- Visualization with [Plotly](https://plotly.com/)

---

**Made with ❤️ by the Pancarbo AI Team**
