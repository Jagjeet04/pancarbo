# Quick Start Guide - Pancarbo Greenfuels AI System

Get up and running with Pancarbo Greenfuels in minutes!

## 🚀 5-Minute Setup

### Option 1: Local (Fastest)

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/Pancarbo-Greenfuels-AI-System.git
cd Pancarbo-Greenfuels-AI-System

# 2. Create environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install and run
pip install -r requirements.txt
streamlit run streamlit_app.py
```

**Result:** App opens at `http://localhost:8501`

### Option 2: Docker

```bash
# One command!
docker-compose up
```

**Result:** App opens at `http://localhost:8501`

### Option 3: Cloud (Streamlit Cloud)

1. Push code to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "Deploy" and select your repo
4. **Done!** App is live

---

## 📊 First Steps

1. **Explore Dashboard**
   - See real-time sensor data
   - Check system health metrics

2. **Test Biomass Prediction**
   - Go to "Biomass Analyzer"
   - Adjust sliders (e.g., moisture: 12%)
   - View quality prediction

3. **Check System Health**
   - View "Boiler Optimizer" page
   - Review efficiency metrics
   - Check maintenance alerts

4. **View Analytics**
   - Analyze historical trends
   - Review feature importance
   - Export insights

---

## 🎯 Common Tasks

### Change Dashboard Appearance

Edit `app_config/config.py`:
```python
BIOMASS_QUALITY_CLASSES = {
    'Excellent': '#2ecc71',  # Change colors here
    'Good': '#3498db',
    'Marginal': '#f39c12',
    'Reject': '#e74c3c'
}
```

### Add Custom Data

Place CSV files in `data/` folder:
```
data/
├── biomass.csv
├── sensors.csv
└── maintenance.csv
```

Update `src/utils.py`:
```python
def load_custom_data():
    return pd.read_csv('data/your_file.csv')
```

### Modify Thresholds

Edit `app_config/config.py`:
```python
THRESHOLDS = {
    "moisture_critical": 20,      # Change here
    "efficiency_warning": 0.80,
    "maintenance_risk": 0.75,
}
```

### Deploy to Production

1. **Streamlit Cloud**
   ```
   Push to GitHub → Cloud auto-deploys
   ```

2. **Docker**
   ```bash
   docker build -t myapp .
   docker run -p 8501:8501 myapp
   ```

3. **Heroku**
   ```bash
   heroku create myapp
   git push heroku main
   ```

---

## 📁 Project Layout

```
Pancarbo-Greenfuels-AI-System/
├── streamlit_app.py          ← Main app
├── pages/                    ← Dashboard pages
│   ├── 1_📊_Dashboard.py
│   ├── 2_🌾_Biomass_Analyzer.py
│   ├── 3_⚙️_Boiler_Optimizer.py
│   ├── 4_🔧_Maintenance.py
│   └── 5_📈_Analytics.py
├── app_config/config.py      ← Settings
├── src/utils.py              ← Functions
├── data/                     ← Your data
├── models/                   ← Saved models
├── requirements.txt          ← Dependencies
└── docker-compose.yml        ← Docker setup
```

---

## 🔧 Customization

### Add New Page

1. Create `pages/6_🆕_NewPage.py`
2. Use existing pages as template:
   ```python
   import streamlit as st
   st.set_page_config(page_title="New Page")
   st.title("🆕 New Feature")
   # Your code here
   ```
3. Page auto-appears in sidebar!

### Modify Prediction Model

Edit `src/utils.py`, `validate_biomass_input()` function:
```python
def validate_biomass_input(data):
    # Add your validation logic
    if not condition_met:
        return False, "Error message"
    return True, "Valid"
```

### Change Colors & Theme

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"           # Your color
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

---

## 🐛 Troubleshooting

### "Port 8501 already in use"
```bash
streamlit run streamlit_app.py --server.port 8502
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Docker won't start"
```bash
docker-compose down
docker-compose up --build
```

### Cache issues
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/

# Restart app
streamlit run streamlit_app.py --logger.level=debug
```

---

## 📚 Learn More

- Full docs: [README.md](README.md)
- Deployment: [DEPLOYMENT.md](DEPLOYMENT.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- GitHub: [Repository](https://github.com/yourusername/repo)

---

## 💡 Tips & Tricks

### Speed Up Loading

Set in `app_config/config.py`:
```python
CACHE_TTL = 3600  # Cache for 1 hour
ENABLE_CACHE = True
```

### Better Visuals

Customize theme in `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
font = "sans serif"
```

### Debug Mode

Enable in `.env`:
```
DEBUG=True
LOG_LEVEL=DEBUG
```

---

## 🎓 Example Workflow

### Scenario: Predict Biomass Quality

1. Open app: `streamlit run streamlit_app.py`
2. Go to **Biomass Analyzer** page
3. Adjust features:
   - Moisture: 12%
   - Feed rate: 4.5 tph
   - Temperature: 900°C
4. View prediction: "Good Quality"
5. Download results: "Export CSV"

### Scenario: Deploy to Web

1. Push to GitHub: `git push origin main`
2. Create Streamlit Cloud account
3. Select repo and deploy
4. Share URL with team
5. Monitor in Streamlit Cloud dashboard

---

## 🆘 Getting Help

- 📧 Email: support@pancarbo.com
- 💬 Discussions: GitHub Discussions
- 🐛 Issues: Report bugs on GitHub
- 📖 Wiki: Full documentation

---

**Start exploring Pancarbo Greenfuels now! 🌾**

For detailed setup: See [README.md](README.md)  
For deployment: See [DEPLOYMENT.md](DEPLOYMENT.md)
