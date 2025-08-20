#!/usr/bin/env python3
"""
Configuration file for Weather Assistant App
Developed by hafizullahkhokhar1

Contains all app settings, API keys, and customizable parameters.
"""

import os
from typing import Dict, List

class WeatherAppConfig:
    """Configuration class for Weather Assistant App"""
    
    # App Information
    APP_NAME = "Weather Assistant"
    APP_VERSION = "1.0.0"
    DEVELOPER = "hafizullahkhokhar1"
    DEVELOPER_EMAIL = "hafizullahkhokhar1@gmail.com"
    
    # Window Settings
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    MIN_WIDTH = 800
    MIN_HEIGHT = 600
    
    # Color Scheme
    COLORS = {
        'primary_bg': '#1a1a2e',      # Main background
        'secondary_bg': '#16213e',     # Cards background  
        'accent_bg': '#0f3460',        # Advice section
        'forecast_bg': '#533483',      # Forecast section
        'text_primary': '#ffffff',     # Main text
        'text_secondary': '#00d4ff',   # Temperature text
        'text_accent': '#888888',      # Status text
        'button_bg': '#0066cc',        # Button background
        'entry_bg': '#ffffff',         # Entry field background
        'border': '#333333'            # Border colors
    }
    
    # Font Settings
    FONTS = {
        'title': ('Helvetica', 24, 'bold'),
        'weather': ('Helvetica', 14),
        'temperature': ('Helvetica', 48, 'bold'),
        'condition': ('Helvetica', 16),
        'details': ('Helvetica', 12),
        'advice': ('Helvetica', 14, 'bold'),
        'search': ('Helvetica', 12),
        'button': ('Helvetica', 10, 'bold'),
        'status': ('Helvetica', 9),
        'icon': ('Helvetica', 60),
        'small_icon': ('Arial', 40),
        'animation': ('Arial', 16)
    }
    
    # API Configuration
    OPENWEATHER_API_KEYS = [
        "bd5e378503939ddaee76f12ad7a97608",  # Demo key 1
        "2a0b95b4a5b5b4a5b5b4a5b5b4a5b5b4",  # Demo key 2
        "5f2b88c4f2b88c4f2b88c4f2b88c4f2b",  # Demo key 3
        "a9146620e91727c1ffef05b3acae3607"       # User replacement
    ]
    
    IPINFO_API_KEYS = [
        "1a2b3c4d5e6f7g",  # Demo token
        "your_ipinfo_token_here"  # User replacement
    ]
    
    # API Endpoints
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
    IPINFO_BASE_URL = "https://ipinfo.io"
    
    # Request Settings
    API_TIMEOUT = 10  # seconds
    LOCATION_TIMEOUT = 5  # seconds
    MAX_RETRIES = 3
    
    # Animation Settings
    ANIMATION_SPEED = {
        'rain': 100,      # milliseconds between frames
        'snow': 200,      # slower than rain
        'clouds': 150,    # cloud movement speed
        'sun': 100,       # sun ray rotation speed
        'lightning': 100  # lightning flash duration
    }
    
    ANIMATION_OBJECTS = {
        'max_raindrops': 50,
        'max_snowflakes': 30,
        'max_clouds': 3,
        'sun_rays': 8,
        'raindrop_length': 20,
        'cloud_speed': 2,
        'lightning_chance': 20  # 1 in 20 chance per frame
    }
    
    # Weather Icons
    WEATHER_ICONS = {
        'clear': '☀️',
        'sunny': '☀️',
        'partly_cloudy': '🌤️',
        'cloudy': '☁️',
        'overcast': '☁️',
        'rain': '🌧️',
        'light_rain': '🌦️',
        'drizzle': '🌦️',
        'heavy_rain': '🌧️',
        'thunderstorm': '⛈️',
        'storm': '⛈️',
        'snow': '❄️',
        'light_snow': '🌨️',
        'heavy_snow': '❄️',
        'sleet': '🌨️',
        'mist': '🌫️',
        'fog': '🌫️',
        'haze': '🌫️',
        'dust': '🌫️',
        'sand': '🌫️',
        'tornado': '🌪️',
        'hurricane': '🌀',
        'hot': '🌡️',
        'cold': '🥶',
        'windy': '💨'
    }
    
    # Default Cities for Demo
    DEMO_CITIES = {
        "karachi": {
            "city": "Karachi", "country": "Pakistan", 
            "temperature": 28, "feels_like": 32, "humidity": 70,
            "wind_speed": 15, "pressure": 1013, "condition": "Clear Sky"
        },
        "lahore": {
            "city": "Lahore", "country": "Pakistan",
            "temperature": 30, "feels_like": 35, "humidity": 65,
            "wind_speed": 12, "pressure": 1015, "condition": "Partly Cloudy"
        },
        "islamabad": {
            "city": "Islamabad", "country": "Pakistan",
            "temperature": 25, "feels_like": 28, "humidity": 60,
            "wind_speed": 10, "pressure": 1018, "condition": "Clear Sky"
        },
        "london": {
            "city": "London", "country": "United Kingdom",
            "temperature": 18, "feels_like": 16, "humidity": 80,
            "wind_speed": 20, "pressure": 1020, "condition": "Light Rain"
        },
        "new york": {
            "city": "New York", "country": "United States",
            "temperature": 22, "feels_like": 25, "humidity": 55,
            "wind_speed": 18, "pressure": 1018, "condition": "Cloudy"
        },
        "tokyo": {
            "city": "Tokyo", "country": "Japan",
            "temperature": 24, "feels_like": 27, "humidity": 70,
            "wind_speed": 8, "pressure": 1016, "condition": "Partly Cloudy"
        },
        "dubai": {
            "city": "Dubai", "country": "United Arab Emirates",
            "temperature": 35, "feels_like": 42, "humidity": 45,
            "wind_speed": 12, "pressure": 1012, "condition": "Clear Sky"
        }
    }
    
    # Weather Advice Templates
    WEATHER_ADVICE = {
        'temperature': {
            'very_hot': "🌡️ Very hot! Stay hydrated and avoid direct sunlight.",
            'hot': "☀️ Hot weather - wear light clothes and drink plenty of water.",
            'warm': "🌤️ Pleasant warm weather - great for outdoor activities!",
            'mild': "😊 Mild temperature - perfect weather conditions!",
            'cool': "🧥 Cool weather - consider a light jacket.",
            'cold': "🧥 Cold weather - dress warmly and layer up!",
            'very_cold': "❄️ Very cold - wear heavy winter clothing."
        },
        'conditions': {
            'rain': "🌧️ It's raining - carry an umbrella and drive carefully!",
            'drizzle': "🌦️ Light drizzle - a light jacket might be helpful.",
            'thunderstorm': "⛈️ Thunderstorm alert - stay indoors and avoid high places!",
            'snow': "❄️ Snowy conditions - drive slowly and wear non-slip shoes.",
            'clear': "🌞 Perfect weather for outdoor activities!",
            'cloudy': "☁️ Cloudy but pleasant - good day for any activities.",
            'fog': "🌫️ Foggy conditions - drive with headlights and reduce speed.",
            'windy': "💨 Windy conditions - be careful with umbrellas!"
        },
        'wind': {
            'very_strong': "💨 Very windy - secure loose objects and avoid highways!",
            'strong': "🌬️ Strong winds - be cautious outdoors.",
            'moderate': "🍃 Moderate breeze - pleasant conditions.",
            'light': "🌿 Light breeze - perfect weather!"
        },
        'humidity': {
            'very_high': "💧 Very high humidity - stay in air-conditioned areas if possible.",
            'high': "💧 High humidity - stay hydrated and cool.",
            'comfortable': "😊 Comfortable humidity levels.",
            'low': "🏜️ Low humidity - use moisturizer and stay hydrated.",
            'very_low': "🏜️ Very dry air - drink extra water and use humidifier."
        },
        'pakistan_specific': {
            'extreme_heat': "🇵🇰 Pakistan weather alert: Extreme heat - avoid outdoor work 12-4 PM.",
            'monsoon': "🇵🇰 Pakistan monsoon - watch for street flooding in urban areas.",
            'dust_storm': "🇵🇰 Dust storm warning - stay indoors and close windows.",
            'karachi_wind': "🚗 Avoid main highways in Karachi during strong winds."
        }
    }
    
    # City Suggestions
    POPULAR_CITIES = [
        "Karachi, Pakistan", "Lahore, Pakistan", "Islamabad, Pakistan",
        "Rawalpindi, Pakistan", "Faisalabad, Pakistan", "Multan, Pakistan",
        "Peshawar, Pakistan", "Quetta, Pakistan", "Hyderabad, Pakistan",
        "London, United Kingdom", "New York, United States", "Tokyo, Japan",
        "Paris, France", "Berlin, Germany", "Sydney, Australia",
        "Toronto, Canada", "Mumbai, India", "Delhi, India", "Dubai, UAE",
        "Singapore", "Bangkok, Thailand", "Istanbul, Turkey",
        "Cairo, Egypt", "Moscow, Russia", "Beijing, China"
    ]
    
    # Temperature Thresholds (Celsius)
    TEMP_THRESHOLDS = {
        'very_hot': 40,
        'hot': 30,
        'warm': 25,
        'mild': 20,
        'cool': 15,
        'cold': 10,
        'very_cold': 0
    }
    
    # Wind Speed Thresholds (km/h)
    WIND_THRESHOLDS = {
        'very_strong': 40,
        'strong': 25,
        'moderate': 15,
        'light': 8
    }
    
    # Humidity Thresholds (%)
    HUMIDITY_THRESHOLDS = {
        'very_high': 85,
        'high': 70,
        'comfortable': 60,
        'low': 40,
        'very_low': 25
    }
    
    # UI Texts
    UI_TEXTS = {
        'title': f"🌤️ Weather Assistant",
        'search_placeholder': "Enter city name (e.g., Karachi, London)",
        'search_button': "🔍 Search",
        'location_button': "📍 My Location",
        'loading': "🔄 Loading weather data...",
        'error_city_not_found': "Could not find weather data for '{}'",
        'error_network': "Network error. Please check your internet connection.",
        'error_api': "Weather service temporarily unavailable.",
        'advice_title': "💡 Weather Advice",
        'forecast_title': "🌅 Tomorrow's Forecast",
        'status_ready': f"Ready - Developed by {DEVELOPER}",
        'status_loading': "Loading weather data...",
        'status_location': "📍 Getting your location...",
        'status_searching': "🔍 Getting weather for {}...",
        'status_updated': "Weather updated for {} - Last updated: {}"
    }
    
    # File Paths
    ASSETS_DIR = "assets"
    ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
    ANIMATIONS_DIR = os.path.join(ASSETS_DIR, "animations")
    CONFIG_DIR = "config"
    
    # Error Messages
    ERROR_MESSAGES = {
        'no_city': "Please enter a city name",
        'invalid_city': "City '{}' not found. Please check the spelling.",
        'network_error': "Network error: {}",
        'api_error': "Weather service error: {}",
        'location_error': "Could not detect your location: {}",
        'general_error': "An unexpected error occurred: {}"
    }
    
    # Animation Colors
    ANIMATION_COLORS = {
        'rain': '#4da6ff',
        'snow': '#ffffff',
        'sun': '#ffdd44',
        'sun_outline': '#ffaa00',
        'lightning': '#ffffff',
        'cloud': '#f0f0f0'
    }
    
    @classmethod
    def get_temperature_category(cls, temp: float) -> str:
        """Get temperature category based on thresholds"""
        if temp >= cls.TEMP_THRESHOLDS['very_hot']:
            return 'very_hot'
        elif temp >= cls.TEMP_THRESHOLDS['hot']:
            return 'hot'
        elif temp >= cls.TEMP_THRESHOLDS['warm']:
            return 'warm'
        elif temp >= cls.TEMP_THRESHOLDS['mild']:
            return 'mild'
        elif temp >= cls.TEMP_THRESHOLDS['cool']:
            return 'cool'
        elif temp >= cls.TEMP_THRESHOLDS['cold']:
            return 'cold'
        else:
            return 'very_cold'
    
    @classmethod
    def get_wind_category(cls, wind_speed: float) -> str:
        """Get wind category based on thresholds"""
        if wind_speed >= cls.WIND_THRESHOLDS['very_strong']:
            return 'very_strong'
        elif wind_speed >= cls.WIND_THRESHOLDS['strong']:
            return 'strong'
        elif wind_speed >= cls.WIND_THRESHOLDS['moderate']:
            return 'moderate'
        else:
            return 'light'
    
    @classmethod
    def get_humidity_category(cls, humidity: float) -> str:
        """Get humidity category based on thresholds"""
        if humidity >= cls.HUMIDITY_THRESHOLDS['very_high']:
            return 'very_high'
        elif humidity >= cls.HUMIDITY_THRESHOLDS['high']:
            return 'high'
        elif humidity >= cls.HUMIDITY_THRESHOLDS['comfortable']:
            return 'comfortable'
        elif humidity >= cls.HUMIDITY_THRESHOLDS['low']:
            return 'low'
        else:
            return 'very_low'
    
    @classmethod
    def get_weather_icon(cls, condition: str) -> str:
        """Get weather icon based on condition"""
        condition_lower = condition.lower()
        
        # Check for exact matches first
        if condition_lower in cls.WEATHER_ICONS:
            return cls.WEATHER_ICONS[condition_lower]
        
        # Check for partial matches
        for key, icon in cls.WEATHER_ICONS.items():
            if key in condition_lower:
                return icon
        
        # Default icon
        return '🌤️'
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [cls.ASSETS_DIR, cls.ICONS_DIR, cls.ANIMATIONS_DIR, cls.CONFIG_DIR]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")


# Create singleton instance
config = WeatherAppConfig()


if __name__ == "__main__":
    # Test configuration
    print(f"App: {config.APP_NAME} v{config.APP_VERSION}")
    print(f"Developer: {config.DEVELOPER}")
    print(f"Colors: {len(config.COLORS)} defined")
    print(f"Fonts: {len(config.FONTS)} defined")
    print(f"Weather Icons: {len(config.WEATHER_ICONS)} defined")
    print(f"Demo Cities: {len(config.DEMO_CITIES)} defined")
    
    # Test temperature categorization
    test_temps = [45, 32, 25, 18, 12, 5, -5]
    print("\nTemperature Categories:")
    for temp in test_temps:
        category = config.get_temperature_category(temp)
        print(f"  {temp}°C -> {category}")
    
    # Test weather icon selection
    test_conditions = ["Clear Sky", "Light Rain", "Thunderstorm", "Snow", "Unknown Weather"]
    print("\nWeather Icons:")
    for condition in test_conditions:
        icon = config.get_weather_icon(condition)
        print(f"  {condition} -> {icon}")