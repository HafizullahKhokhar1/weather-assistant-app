#!/usr/bin/env python3
"""
Streamlit Weather Dashboard Launcher
Developed by hafizullahkhokhar1

This script handles installation and launching of the modern weather dashboard.
"""

import sys
import subprocess
import importlib.util
import os
from pathlib import Path
import time


def print_header():
    """Print beautiful header"""
    print("🌤️" + "="*60 + "🌤️")
    print("        Modern Weather Dashboard Launcher")
    print("           Developed by hafizullahkhokhar1")
    print("🌤️" + "="*60 + "🌤️")


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3.7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again.")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    return True


def check_package_installed(package_name):
    """Check if a Python package is installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None


def install_package(package_name):
    """Install a Python package using pip"""
    try:
        print(f"📦 Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--quiet"])
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package_name}")
        return False


def check_and_install_dependencies():
    """Check and install required dependencies"""
    required_packages = {
        'streamlit': 'streamlit>=1.28.0',
        'requests': 'requests>=2.31.0',
        'pandas': 'pandas>=2.0.0',
        'plotly': 'plotly>=5.15.0',
        'geocoder': 'geocoder>=1.38.1',
        'pycountry': 'pycountry>=22.3.0'
    }
    
    missing_packages = []
    
    print("🔍 Checking dependencies...")
    
    for import_name, package_spec in required_packages.items():
        if not check_package_installed(import_name):
            print(f"❌ {import_name} is not installed")
            missing_packages.append(package_spec)
        else:
            print(f"✅ {import_name} is installed")
    
    # Install missing packages
    if missing_packages:
        print(f"\n📥 Installing {len(missing_packages)} missing packages...")
        print("⏳ This may take a few minutes...")
        
        for package in missing_packages:
            if not install_package(package):
                return False
        print("✅ All dependencies installed successfully!")
    else:
        print("✅ All dependencies are already installed!")
    
    return True


def create_streamlit_config():
    """Create Streamlit configuration directory and file"""
    config_dir = ".streamlit"
    config_file = os.path.join(config_dir, "config.toml")
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(f"📁 Created {config_dir} directory")
    
    if not os.path.exists(config_file):
        config_content = """[global]
developmentMode = false
showWarningOnDirectExecution = false

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 50
maxMessageSize = 50
enableWebsocketCompression = true
address = "0.0.0.0"
headless = false

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[theme]
primaryColor = "#4A90E2"
backgroundColor = "#1e3c72"
secondaryBackgroundColor = "#2a5298"
textColor = "#FFFFFF"
font = "sans serif"

[ui]
hideTopBar = false
hideFooterDetails = false
sidebarState = "expanded"
wideMode = true
initialSidebarState = "expanded"
"""
        with open(config_file, 'w') as f:
            f.write(config_content)
        print(f"⚙️ Created {config_file}")


def check_app_files():
    """Check if required app files exist"""
    required_files = ['app.py']
    missing_files = []
    
    print("\n🔍 Checking app files...")
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name} found")
        else:
            print(f"❌ {file_name} is missing")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        print("   Please make sure app.py is in the current directory.")
        return False
    
    return True


def launch_streamlit():
    """Launch the Streamlit weather dashboard"""
    try:
        print("\n🚀 Launching Modern Weather Dashboard...")
        print("   📱 The app will open in your default web browser")
        print("   🌐 Access URL: http://localhost:8501")
        print("   🛑 Press Ctrl+C to stop the server")
        print("-" * 60)
        
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 Weather Dashboard stopped by user")
    except FileNotFoundError:
        print("\n❌ Streamlit not found. Installing...")
        if install_package("streamlit"):
            launch_streamlit()
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")


def open_browser():
    """Open browser to the dashboard URL"""
    import webbrowser
    time.sleep(3)  # Wait for server to start
    try:
        webbrowser.open('http://localhost:8501')
        print("🌐 Opening browser...")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")
        print("   Please manually open: http://localhost:8501")


def show_help():
    """Show help information"""
    print("""
🌤️ Modern Weather Dashboard - Streamlit Launcher

Usage:
    python run.py          - Check dependencies and launch dashboard
    python run.py --help   - Show this help message
    python run.py --check  - Only check dependencies, don't launch
    python run.py --install - Only install dependencies, don't launch
    python run.py --config - Create Streamlit configuration files

Features:
    ✅ Modern web-based interface with Streamlit
    ✅ Real-time weather data with your OpenWeatherMap API
    ✅ Interactive charts and visualizations with Plotly
    ✅ Beautiful responsive design with custom themes
    ✅ Auto-location detection and city search
    ✅ 5-day forecast with hourly breakdowns
    ✅ Smart weather advice and recommendations

Requirements:
    - Python 3.7 or higher
    - Internet connection
    - Modern web browser (Chrome, Firefox, Safari, Edge)

Access:
    - Local: http://localhost:8501
    - Network: http://YOUR_IP:8501

If you encounter issues:
    1. Make sure you have Python 3.7+
    2. Check your internet connection
    3. Ensure port 8501 is not in use
    4. Try: pip install streamlit plotly pandas requests
    5. Contact: hafizullahkhokhar1@gmail.com

Deployment:
    - Local: python run.py
    - Cloud: Deploy to Streamlit Cloud, Heroku, or AWS
    - Docker: Use provided Dockerfile for containerization
""")


def create_dockerfile():
    """Create Dockerfile for containerized deployment"""
    dockerfile_content = """# Modern Weather Dashboard Dockerfile
# Developed by hafizullahkhokhar1

FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create .streamlit directory and config
RUN mkdir -p .streamlit
COPY .streamlit/config.toml .streamlit/

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    print("🐳 Created Dockerfile for containerized deployment")


def create_docker_compose():
    """Create docker-compose.yml for easy deployment"""
    docker_compose_content = """version: '3.8'

services:
  weather-dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

# Optional: Add nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - weather-dashboard
    restart: unless-stopped
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content)
    print("🐳 Created docker-compose.yml")


def main():
    """Main launcher function"""
    print_header()
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h', 'help']:
            show_help()
            return
        
        elif arg in ['--check', '-c', 'check']:
            print("🔍 Checking system requirements only...")
            check_python_version()
            check_and_install_dependencies()
            check_app_files()
            print("\n✅ System check complete!")
            return
        
        elif arg in ['--install', '-i', 'install']:
            print("📦 Installing dependencies only...")
            check_python_version()
            check_and_install_dependencies()
            create_streamlit_config()
            print("\n✅ Installation complete!")
            return
        
        elif arg in ['--config', '-cfg', 'config']:
            print("⚙️ Creating configuration files...")
            create_streamlit_config()
            create_dockerfile()
            create_docker_compose()
            print("\n✅ Configuration files created!")
            return
    
    # Full setup and launch
    print("🚀 Starting full setup and launch...\n")
    
    # Step 1: Check Python version
    if not check_python_version():
        return
    
    # Step 2: Check and install dependencies
    print("\n" + "="*50)
    if not check_and_install_dependencies():
        print("\n❌ Dependency installation failed")
        print("   Try running: pip install -r requirements.txt")
        return
    
    # Step 3: Check app files
    print("\n" + "="*50)
    if not check_app_files():
        return
    
    # Step 4: Create Streamlit configuration
    print("\n" + "="*50)
    print("⚙️ Setting up Streamlit configuration...")
    create_streamlit_config()
    
    # Step 5: Launch the dashboard
    print("\n" + "="*50)
    print("🎉 Everything is ready! Launching dashboard...")
    print("\n💡 Tips:")
    print("   - The app will open automatically in your browser")
    print("   - Use the sidebar to search for cities")
    print("   - Try the auto-location feature")
    print("   - All data is real-time from OpenWeatherMap")
    print("   - Charts are interactive - hover and zoom!")
    
    # Small delay for user to read
    time.sleep(3)
    launch_streamlit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher interrupted by user")
    except Exception as e:
        print(f"\n❌ Launcher error: {e}")
        print("   Please try running: streamlit run app.py")