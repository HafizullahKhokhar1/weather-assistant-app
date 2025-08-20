# 🚀 Deployment Guide - Modern Weather Dashboard

Complete guide for deploying your weather dashboard locally and to the cloud.

**Developed by hafizullahkhokhar1**

## 📋 Quick Start (Local Development)

### Option 1: Automatic Setup
```bash
# Clone or create project directory
mkdir weather-dashboard
cd weather-dashboard

# Copy all files from artifacts, then:
python run.py
```

### Option 2: Manual Setup  
```bash
# Install dependencies
pip install streamlit plotly pandas requests geocoder pycountry

# Run the dashboard
streamlit run app.py
```

### Option 3: Using UV (Faster)
```bash
# Install UV
pip install uv

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Linux/Mac
# OR: .venv\Scripts\activate  # Windows

uv pip install -r requirements.txt

# Launch dashboard
streamlit run app.py
```

---

## 🌐 Cloud Deployment Options

### 1. 📱 Streamlit Community Cloud (FREE & RECOMMENDED)

**Steps:**
1. **Upload to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Modern weather dashboard"
   git remote add origin https://github.com/yourusername/weather-dashboard.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy!"

3. **Your app will be live at:**
   `https://yourusername-weather-dashboard-app-xxx.streamlit.app`

**Advantages:**
- ✅ Completely FREE
- ✅ Automatic HTTPS
- ✅ Auto-updates from GitHub
- ✅ Built-in CI/CD
- ✅ No server management

---

### 2. 🐳 Docker Deployment

**Create Dockerfile:** (already included)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Deploy with Docker:**
```bash
# Build image
docker build -t weather-dashboard .

# Run container
docker run -p 8501:8501 weather-dashboard

# Or use docker-compose
docker-compose up -d
```

**Deploy to Cloud:**
- **DigitalOcean:** App Platform
- **AWS:** ECS/Fargate
- **Google Cloud:** Cloud Run
- **Azure:** Container Instances

---

### 3. ☁️ Heroku Deployment

**Create required files:**

`Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

`runtime.txt`:
```
python-3.9.18
```

**Deploy:**
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-weather-dashboard

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open app
heroku open
```

---

### 4. 🚀 Railway Deployment

1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Deploy automatically
4. Get live URL

**Advantages:**
- ✅ Simple deployment
- ✅ Automatic builds
- ✅ Free tier available
- ✅ Custom domains

---

### 5. ⚡ Vercel Deployment

**Create `vercel.json`:**
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

**Deploy:**
```bash
npm i -g vercel
vercel --prod
```

---

## 🔧 Environment Configuration

### Environment Variables
Create `.env` file:
```env
OPENWEATHER_API_KEY=a9146620e91727c1ffef05b3acae3607
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Streamlit Secrets (for Cloud)
Create `.streamlit/secrets.toml`:
```toml
OPENWEATHER_API_KEY = "a9146620e91727c1ffef05b3acae3607"

[database]
# Add database credentials if needed

[api_keys]
openweather = "a9146620e91727c1ffef05b3acae3607"
mapbox = "your_mapbox_token_here"
```

**Access in code:**
```python
import streamlit as st
api_key = st.secrets["OPENWEATHER_API_KEY"]
```

---

## 📊 Production Optimization

### 1. Performance Settings

**Update `.streamlit/config.toml`:**
```toml
[server]
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 50
enableWebsocketCompression = true

[client]
caching = true
displayEnabled = true

[runner]
magicEnabled = true
installTracer = false
fixMatplotlib = true
```

### 2. Caching Implementation

**Add to app.py:**
```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_weather_data(lat: float, lon: float):
    # Your weather fetching code
    pass

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_forecast_data(lat: float, lon: float):
    # Your forecast fetching code
    pass
```

### 3. Error Handling & Monitoring

**Add logging:**
```python
import logging
logging.basicConfig(level=logging.INFO)

# Add to your functions
try:
    # API call
    pass
except Exception as e:
    logging.error(f"API Error: {e}")
    st.error("Weather service temporarily unavailable")
```

---

## 🔐 Security Best Practices

### 1. API Key Security
- ✅ Use environment variables
- ✅ Never commit keys to Git
- ✅ Use Streamlit secrets for cloud
- ✅ Rotate keys regularly

### 2. Input Validation
```python
def validate_coordinates(lat, lon):
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError("Invalid coordinates")
    return True
```

### 3. Rate Limiting
```python
import time
from functools import wraps

def rate_limit(max_calls=60, time_window=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Implement rate limiting logic
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## 📱 Mobile Optimization

### Responsive Design
```python
# Detect mobile
def is_mobile():
    return st.session_state.get('mobile', False)

# Adjust layout
if is_mobile():
    cols = st.columns(1)
else:
    cols = st.columns([2, 1, 1])
```

### Mobile-First CSS
```css
/* Add to st.markdown with unsafe_allow_html=True */
@media (max-width: 768px) {
    .metric-card {
        margin: 0.5rem 0;
        padding: 1rem;
    }
    
    .temperature-display {
        font-size: 2rem !important;
    }
}
```

---

## 🚀 Advanced Deployment (Production)

### 1. Load Balancer Setup (Nginx)

**nginx.conf:**
```nginx
upstream weather_app {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;  # Multiple instances
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://weather_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 2. SSL/TLS Certificate (Let's Encrypt)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Process Management (systemd)

**Create `/etc/systemd/system/weather-dashboard.service`:**
```ini
[Unit]
Description=Weather Dashboard
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/weather-dashboard
Environment=PATH=/var/www/weather-dashboard/venv/bin
ExecStart=/var/www/weather-dashboard/venv/bin/streamlit run app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable weather-dashboard
sudo systemctl start weather-dashboard
```

---

## 📊 Monitoring & Analytics

### 1. Application Monitoring
```python
import psutil
import time

# Add to sidebar
if st.sidebar.checkbox("Show System Info"):
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        st.metric("CPU", f"{psutil.cpu_percent()}%")
        st.metric("Memory", f"{psutil.virtual_memory().percent}%")
    
    with col2:
        st.metric("Requests", st.session_state.get('request_count', 0))
        st.metric("Uptime", f"{time.time() - st.session_state.get('start_time', time.time()):.0f}s")
```

### 2. Error Tracking (Sentry)
```python
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[LoggingIntegration()],
    traces_sample_rate=0.1
)
```

### 3. Usage Analytics
```python
# Track page views
if 'page_views' not in st.session_state:
    st.session_state.page_views = 0
st.session_state.page_views += 1

# Track user interactions
def track_search(city):
    # Log to analytics service
    pass
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

**1. Port already in use:**
```bash
# Kill process on port 8501
sudo lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app.py --server.port=8502
```

**2. Memory issues:**
```python
# Clear cache periodically
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.experimental_rerun()
```

**3. API rate limits:**
```python
# Implement exponential backoff
import random
import time

def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + random.random()
            time.sleep(wait_time)
```

**4. HTTPS mixed content:**
```python
# Force HTTPS in production
if st.secrets.get("environment") == "production":
    st.markdown("""
    <script>
    if (location.protocol !== 'https:') {
        location.replace('https:' + window.location.href.substring(window.location.protocol.length));
    }
    </script>
    """, unsafe_allow_html=True)
```

---

## 📈 Scaling & Performance

### Horizontal Scaling
- Deploy multiple instances
- Use load balancer (nginx/HAProxy)
- Database for shared state
- Redis for caching

### Vertical Scaling
- Increase server resources
- Optimize Python code
- Use async operations
- Implement caching strategies

### CDN Integration
- Serve static assets from CDN
- Cache API responses
- Optimize images
- Compress responses

---

## 🎯 Success Metrics

### Deployment Checklist
- [ ] App loads without errors
- [ ] Weather data fetches correctly
- [ ] Charts render properly
- [ ] Mobile responsive
- [ ] HTTPS enabled (production)
- [ ] Error handling works
- [ ] Performance optimized
- [ ] Monitoring enabled

### Testing
```bash
# Load testing with Apache Bench
ab -n 100 -c 10 http://localhost:8501/

# Python testing
python -m pytest tests/

# Security scan
bandit -r app.py
```

---

**🎉 Your Modern Weather Dashboard is ready for the world!**

**📧 Need help? Contact hafizullahkhokhar1@gmail.com**

---

*Last updated: August 2025*
