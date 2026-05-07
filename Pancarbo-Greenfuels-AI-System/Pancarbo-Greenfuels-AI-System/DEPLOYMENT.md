# Deployment Guide - Pancarbo Greenfuels AI System

This guide provides step-by-step instructions for deploying Pancarbo Greenfuels to various platforms.

## Table of Contents

- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [Streamlit Cloud](#streamlit-cloud)
- [Heroku](#heroku)
- [Render](#render)
- [AWS](#aws)
- [Troubleshooting](#troubleshooting)

---

## Local Deployment

### Prerequisites

- Python 3.9 or higher
- pip or conda

### Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/Pancarbo-Greenfuels-AI-System.git
   cd Pancarbo-Greenfuels-AI-System
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run Application**
   ```bash
   streamlit run streamlit_app.py
   ```

6. **Access Application**
   - Open browser to `http://localhost:8501`

---

## Docker Deployment

### Prerequisites

- Docker
- Docker Compose (optional)

### Using Docker Compose (Recommended)

1. **Build and Run**
   ```bash
   docker-compose up --build
   ```

2. **Access Application**
   - `http://localhost:8501`

3. **View Logs**
   ```bash
   docker-compose logs -f pancarbo-app
   ```

4. **Stop Application**
   ```bash
   docker-compose down
   ```

### Using Docker Directly

1. **Build Image**
   ```bash
   docker build -t pancarbo-app:latest .
   ```

2. **Run Container**
   ```bash
   docker run -p 8501:8501 \
     -e DEBUG=False \
     -e LOG_LEVEL=INFO \
     --name pancarbo \
     pancarbo-app:latest
   ```

3. **Access Application**
   - `http://localhost:8501`

4. **Stop Container**
   ```bash
   docker stop pancarbo
   docker rm pancarbo
   ```

---

## Streamlit Cloud

### Prerequisites

- GitHub account with repository
- Streamlit Cloud account

### Steps

1. **Push Code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Connect to Streamlit Cloud**
   - Visit [streamlit.io/cloud](https://streamlit.io/cloud)
   - Click "New app"
   - Select your GitHub repository
   - Choose branch: `main`
   - Set main file path: `streamlit_app.py`

3. **Configure Secrets**
   - In Streamlit Cloud dashboard
   - Click on app settings
   - Add environment variables from `.env.example`

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app URL will be provided

### Custom Domain (Optional)

1. Configure DNS settings
2. Add custom domain in Streamlit Cloud settings
3. Wait for SSL certificate generation

---

## Heroku

### Prerequisites

- Heroku account
- Heroku CLI installed
- GitHub repository

### Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create App**
   ```bash
   heroku create pancarbo-app-name
   ```

3. **Add Buildpack**
   ```bash
   heroku buildpacks:add heroku/python
   ```

4. **Deploy Code**
   ```bash
   git push heroku main
   ```

5. **Configure Environment Variables**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set LOG_LEVEL=INFO
   heroku config:set DEPLOYMENT_PLATFORM=HEROKU
   ```

6. **View Logs**
   ```bash
   heroku logs --tail
   ```

7. **Access Application**
   - `https://pancarbo-app-name.herokuapp.com`

### Cost Optimization

- Free tier: Limited to 550 dyno hours/month
- Upgrade if needed: `heroku dyno:upgrade web`
- Consider scheduled downtime for cost savings

---

## Render

### Prerequisites

- Render account
- GitHub repository

### Steps

1. **Create Web Service**
   - Visit [render.com](https://render.com)
   - Click "New +"
   - Select "Web Service"
   - Connect GitHub

2. **Configure Service**
   - Name: `pancarbo-greenfuels`
   - Environment: `Python 3`
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run streamlit_app.py --server.port=10000`

3. **Environment Variables**
   - Add from `.env.example`
   - Important: Set `DEPLOYMENT_PLATFORM=RENDER`

4. **Deploy**
   - Click "Create Web Service"
   - Monitor deployment logs

5. **Access Application**
   - `https://pancarbo-greenfuels.onrender.com`

### Important Notes

- Render requires port 10000 for web services
- Free tier has limitations on uptime
- Set auto-deploy on push in settings

---

## AWS

### Using EC2

1. **Launch Instance**
   - Ubuntu 20.04 LTS
   - t2.micro or larger
   - Security group: Allow ports 80, 443, 8501

2. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv
   ```

4. **Setup Application**
   ```bash
   git clone your-repo-url
   cd Pancarbo-Greenfuels-AI-System
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Run with Supervisor**
   ```bash
   sudo apt install supervisor
   # Create config file for streamlit app
   ```

### Using ECS with Docker

1. **Create ECR Repository**
   ```bash
   aws ecr create-repository --repository-name pancarbo-app
   ```

2. **Push Image**
   ```bash
   docker build -t pancarbo-app .
   docker tag pancarbo-app:latest your-account-id.dkr.ecr.region.amazonaws.com/pancarbo-app:latest
   docker push your-account-id.dkr.ecr.region.amazonaws.com/pancarbo-app:latest
   ```

3. **Create ECS Service**
   - Task definition
   - Service configuration
   - Load balancer setup

---

## Troubleshooting

### Port Issues

```bash
# Check if port is in use
lsof -i :8501  # On Mac/Linux
netstat -ano | findstr :8501  # On Windows

# Use different port
streamlit run streamlit_app.py --server.port 8502
```

### Memory Issues

```bash
# Increase Docker memory
docker run -m 2g pancarbo-app:latest

# Or in docker-compose.yml
services:
  pancarbo-app:
    deploy:
      resources:
        limits:
          memory: 2G
```

### Dependency Issues

```bash
# Update requirements with latest compatible versions
pip list --outdated
pip install --upgrade -r requirements.txt

# Rebuild requirements.txt
pip freeze > requirements.txt
```

### Cache Issues

```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/

# Clear Docker cache
docker system prune -a

# Clear pip cache
pip cache purge
```

### Debugging

Enable debug mode in `.env`:
```
DEBUG=True
LOG_LEVEL=DEBUG
```

View logs:
```bash
# Docker
docker logs pancarbo-app

# Heroku
heroku logs --tail

# Local
tail -f logs/pancarbo.log
```

---

## Performance Optimization

### 1. Caching
- Enable caching in config
- Use `@st.cache_data` decorator
- Adjust `CACHE_TTL` in `.env`

### 2. Image Optimization
- Use smaller base images
- Minimize Docker layers
- Compress data files

### 3. Code Optimization
- Lazy load heavy libraries
- Use efficient algorithms
- Profile code regularly

### 4. Database
- Use connection pooling
- Add indexes
- Archive old data

---

## Monitoring & Maintenance

### Uptime Monitoring

- Use tools like UptimeRobot
- Set up health checks
- Configure alerts

### Logging

- Centralize logs with ELK stack
- Use structured logging
- Set appropriate log levels

### Updates

- Keep dependencies updated
- Review security advisories
- Test in staging before production

### Backups

- Regular database backups
- Store models in version control
- Archive reports

---

## Security Considerations

### Before Deployment

- [ ] Use strong API keys
- [ ] Set `SECURE_MODE=True` in production
- [ ] Use HTTPS only
- [ ] Configure firewall rules
- [ ] Enable authentication if needed

### Secrets Management

Use environment variables for:
- API keys
- Database credentials
- Authentication tokens
- Configuration values

Example `.env`:
```
API_KEY=your_secure_key
DB_PASSWORD=your_secure_password
SECRET_KEY=your_secret_key
```

---

## Cost Estimation

| Platform | Free Tier | Pricing |
|----------|-----------|---------|
| Streamlit Cloud | Yes | $10-300/mo |
| Heroku | 550 hrs/mo | $7-50/mo |
| Render | Yes | $4.50+/mo |
| AWS EC2 | 750 hrs/mo | $5-50+/mo |

---

## Support

- Documentation: [README.md](../README.md)
- Issues: GitHub Issues
- Discussions: GitHub Discussions

---

**Last Updated:** 2024
**Version:** 1.0.0
