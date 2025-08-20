#!/usr/bin/env python3
"""
Modern Weather Dashboard with Streamlit
Professional UI with real-time data and beautiful design
Developed by hafizullahkhokhar1
"""

import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import geocoder
import pycountry
from typing import Dict, List, Optional, Tuple

# Page configuration
st.set_page_config(
    page_title="🌤️ Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/hafizullahkhokhar1',
        'Report a bug': 'https://github.com/hafizullahkhokhar1',
        'About': "Modern Weather Dashboard by hafizullahkhokhar1"
    }
)

class WeatherDashboard:
    def __init__(self):
        # Your OpenWeatherMap API key
        self.api_key = "a9146620e91727c1ffef05b3acae3607"
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0"
        
        # Weather icons mapping
        self.weather_icons = {
            "01d": "☀️", "01n": "🌙", "02d": "⛅", "02n": "☁️",
            "03d": "☁️", "03n": "☁️", "04d": "☁️", "04n": "☁️",
            "09d": "🌧️", "09n": "🌧️", "10d": "🌦️", "10n": "🌧️",
            "11d": "⛈️", "11n": "⛈️", "13d": "❄️", "13n": "❄️",
            "50d": "🌫️", "50n": "🌫️"
        }
        
        # Initialize session state
        if 'weather_data' not in st.session_state:
            st.session_state.weather_data = None
        if 'forecast_data' not in st.session_state:
            st.session_state.forecast_data = None
        if 'last_update' not in st.session_state:
            st.session_state.last_update = None
        if 'current_location' not in st.session_state:
            st.session_state.current_location = None

    def clear_weather_cache(self):
        """Clear cached weather data"""
        st.session_state.weather_data = None
        st.session_state.forecast_data = None
        st.session_state.last_update = None

    def get_user_location(self) -> Optional[Dict]:
        """Get user's current location using IP"""
        try:
            # Using ipinfo.io for location detection
            response = requests.get('https://ipinfo.io/json', timeout=5)
            if response.status_code == 200:
                data = response.json()
                loc = data.get('loc', '').split(',')
                return {
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'lat': float(loc[0]) if len(loc) > 0 else 0,
                    'lon': float(loc[1]) if len(loc) > 1 else 0
                }
        except Exception as e:
            st.error(f"Location detection failed: {e}")
            return None

    def get_countries(self) -> List[str]:
        """Get list of countries"""
        countries = []
        for country in pycountry.countries:
            countries.append(country.name)
        return sorted(countries)

    def search_cities(self, query: str, limit: int = 5) -> List[Dict]:
        """Search cities using OpenWeatherMap Geocoding API"""
        try:
            url = f"{self.geocoding_url}/direct"
            params = {
                'q': query,
                'limit': limit,
                'appid': self.api_key
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            st.error(f"City search failed: {e}")
            return []

    def get_weather_data(self, lat: float, lon: float) -> Optional[Dict]:
        """Get current weather data"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'location': f"{data['name']}, {data['sys']['country']}",
                    'temperature': round(data['main']['temp']),
                    'feels_like': round(data['main']['feels_like']),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': round(data['wind']['speed'] * 3.6),  # Convert to km/h
                    'wind_direction': data['wind'].get('deg', 0),
                    'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                    'condition': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                    'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
                    'sunset': datetime.fromtimestamp(data['sys']['sunset']),
                    'timestamp': datetime.now(),
                    'coordinates': {'lat': lat, 'lon': lon}
                }
            else:
                st.error(f"Weather API Error: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error fetching weather data: {e}")
            return None

    def get_forecast_data(self, lat: float, lon: float) -> Optional[Dict]:
        """Get 5-day weather forecast"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                forecasts = []
                
                for item in data['list']:
                    forecasts.append({
                        'datetime': datetime.fromtimestamp(item['dt']),
                        'temperature': round(item['main']['temp']),
                        'feels_like': round(item['main']['feels_like']),
                        'humidity': item['main']['humidity'],
                        'condition': item['weather'][0]['description'].title(),
                        'icon': item['weather'][0]['icon'],
                        'wind_speed': round(item['wind']['speed'] * 3.6),
                        'rain': item.get('rain', {}).get('3h', 0)
                    })
                
                return {
                    'location': f"{data['city']['name']}, {data['city']['country']}",
                    'forecasts': forecasts,
                    'coordinates': {'lat': lat, 'lon': lon}
                }
            else:
                st.error(f"Forecast API Error: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error fetching forecast data: {e}")
            return None

    def generate_weather_advice(self, weather_data: Dict) -> str:
        """Generate contextual weather advice"""
        temp = weather_data['temperature']
        condition = weather_data['condition'].lower()
        wind_speed = weather_data['wind_speed']
        humidity = weather_data['humidity']
        
        advice = []
        
        # Temperature advice
        if temp > 35:
            advice.append("🌡️ Extreme heat! Stay indoors during peak hours, drink lots of water.")
        elif temp > 30:
            advice.append("☀️ Very warm - wear light colors, use sunscreen, stay hydrated.")
        elif temp < 10:
            advice.append("🧥 Cold weather - dress warmly in layers.")
        elif temp < 0:
            advice.append("❄️ Freezing conditions - be careful of icy surfaces.")
        
        # Condition advice
        if 'rain' in condition:
            advice.append("🌧️ Rainy weather - carry an umbrella, drive carefully.")
        elif 'thunderstorm' in condition:
            advice.append("⛈️ Thunderstorm warning - stay indoors, avoid open areas.")
        elif 'snow' in condition:
            advice.append("❄️ Snow expected - drive slowly, wear appropriate footwear.")
        elif 'fog' in condition or 'mist' in condition:
            advice.append("🌫️ Poor visibility - use headlights, drive with caution.")
        
        # Wind advice
        if wind_speed > 50:
            advice.append("💨 Very strong winds - avoid outdoor activities, secure objects.")
        elif wind_speed > 30:
            advice.append("🌬️ Strong winds - be cautious with umbrellas and light objects.")
        
        # Humidity advice
        if humidity > 80:
            advice.append("💧 High humidity - expect muggy conditions, stay cool.")
        elif humidity < 30:
            advice.append("🏜️ Low humidity - drink water, use moisturizer.")
        
        return " ".join(advice) if advice else "Weather conditions are pleasant. Enjoy your day!"

    def create_temperature_chart(self, forecast_data: Dict) -> go.Figure:
        """Create temperature trend chart"""
        forecasts = forecast_data['forecasts'][:24]  # Next 24 hours
        times = [f['datetime'] for f in forecasts]
        temps = [f['temperature'] for f in forecasts]
        feels_like = [f['feels_like'] for f in forecasts]
        
        fig = go.Figure()
        
        # Temperature line
        fig.add_trace(go.Scatter(
            x=times, y=temps,
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=6)
        ))
        
        # Feels like line
        fig.add_trace(go.Scatter(
            x=times, y=feels_like,
            mode='lines+markers',
            name='Feels Like',
            line=dict(color='#4ECDC4', width=2, dash='dot'),
            marker=dict(size=4)
        ))
        
        fig.update_layout(
            title="24-Hour Temperature Trend",
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            template="plotly_dark",
            height=400,
            showlegend=True,
            hovermode='x unified'
        )
        
        return fig

    def create_weather_metrics_chart(self, forecast_data: Dict) -> go.Figure:
        """Create weather metrics dashboard"""
        forecasts = forecast_data['forecasts'][:24]
        times = [f['datetime'] for f in forecasts]
        humidity = [f['humidity'] for f in forecasts]
        wind = [f['wind_speed'] for f in forecasts]
        rain = [f['rain'] for f in forecasts]
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Humidity (%)', 'Wind Speed (km/h)', 'Rainfall (mm)'),
            vertical_spacing=0.08
        )
        
        # Humidity
        fig.add_trace(go.Scatter(
            x=times, y=humidity,
            mode='lines+markers',
            name='Humidity',
            line=dict(color='#45B7D1', width=2),
            marker=dict(size=4)
        ), row=1, col=1)
        
        # Wind Speed
        fig.add_trace(go.Scatter(
            x=times, y=wind,
            mode='lines+markers',
            name='Wind Speed',
            line=dict(color='#96CEB4', width=2),
            marker=dict(size=4)
        ), row=2, col=1)
        
        # Rainfall
        fig.add_trace(go.Bar(
            x=times, y=rain,
            name='Rainfall',
            marker=dict(color='#FECA57')
        ), row=3, col=1)
        
        fig.update_layout(
            height=600,
            template="plotly_dark",
            showlegend=False,
            title_text="Weather Metrics - Next 24 Hours"
        )
        
        return fig

    def display_current_weather(self, weather_data: Dict):
        """Display current weather in a beautiful layout"""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Main weather display
            icon = self.weather_icons.get(weather_data['icon'], '🌤️')
            st.markdown(f"""
            <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; margin-bottom: 1rem;">
                <h1 style="color: white; margin: 0; font-size: 4rem;">{icon}</h1>
                <h1 style="color: white; margin: 0.5rem 0; font-size: 3.5rem;">{weather_data['temperature']}°C</h1>
                <h3 style="color: white; margin: 0; opacity: 0.9;">{weather_data['condition']}</h3>
                <p style="color: white; margin: 0.5rem 0; opacity: 0.8;">Feels like {weather_data['feels_like']}°C</p>
                <h4 style="color: white; margin: 0.5rem 0; opacity: 0.9;">{weather_data['location']}</h4>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Weather details
            st.markdown("### 🌡️ Details")
            st.metric("Humidity", f"{weather_data['humidity']}%")
            st.metric("Pressure", f"{weather_data['pressure']} hPa")
            st.metric("Visibility", f"{weather_data['visibility']:.1f} km")
        
        with col3:
            # Wind and sun info
            st.markdown("### 💨 Wind & Sun")
            st.metric("Wind Speed", f"{weather_data['wind_speed']} km/h")
            st.metric("Sunrise", weather_data['sunrise'].strftime("%H:%M"))
            st.metric("Sunset", weather_data['sunset'].strftime("%H:%M"))

    def display_forecast(self, forecast_data: Dict):
        """Display forecast data"""
        st.markdown("### 📅 5-Day Forecast")
        
        # Group forecast by days
        daily_forecasts = {}
        for forecast in forecast_data['forecasts']:
            date_key = forecast['datetime'].date()
            if date_key not in daily_forecasts:
                daily_forecasts[date_key] = []
            daily_forecasts[date_key].append(forecast)
        
        # Display first 5 days
        cols = st.columns(5)
        for i, (date, day_forecasts) in enumerate(list(daily_forecasts.items())[:5]):
            if i < len(cols):
                with cols[i]:
                    # Get representative forecast (noon or closest)
                    noon_forecast = None
                    for forecast in day_forecasts:
                        if forecast['datetime'].hour >= 12:
                            noon_forecast = forecast
                            break
                    if not noon_forecast:
                        noon_forecast = day_forecasts[0]
                    
                    # Calculate daily stats
                    temps = [f['temperature'] for f in day_forecasts]
                    max_temp = max(temps)
                    min_temp = min(temps)
                    
                    icon = self.weather_icons.get(noon_forecast['icon'], '🌤️')
                    day_name = date.strftime("%A")[:3]
                    
                    st.markdown(f"""
                    <div style="text-align: center; background: rgba(255, 255, 255, 0.1); 
                                padding: 1rem; border-radius: 10px; backdrop-filter: blur(10px);">
                        <h4 style="margin: 0; color: #333;">{day_name}</h4>
                        <div style="font-size: 2rem; margin: 0.5rem 0;">{icon}</div>
                        <p style="margin: 0; font-weight: bold;">{max_temp}° / {min_temp}°</p>
                        <p style="margin: 0.5rem 0; font-size: 0.8rem;">{noon_forecast['condition']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    def run_dashboard(self):
        """Main dashboard interface"""
        # Custom CSS
        st.markdown("""
        <style>
        .main { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); }
        .stSelectbox > div > div { background-color: rgba(255, 255, 255, 0.1); }
        .metric-card { background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; }
        </style>
        """, unsafe_allow_html=True)
        
        # Header
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                🌤️ Modern Weather Dashboard
            </h1>
            <p style="color: white; opacity: 0.8;">Real-time weather data with beautiful visualizations</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar for location selection
        with st.sidebar:
            st.markdown("## 📍 Location Selection")
            
            location_method = st.radio(
                "Choose location method:",
                ["🔍 Search City", "📍 Auto-detect", "🌍 Browse by Country"]
            )
            
            lat, lon = None, None
            location_name = ""
            location_key = ""  # Unique identifier for location
            
            if location_method == "📍 Auto-detect":
                if st.button("📍 Get My Location"):
                    with st.spinner("Detecting your location..."):
                        user_location = self.get_user_location()
                        if user_location:
                            lat, lon = user_location['lat'], user_location['lon']
                            location_name = f"{user_location['city']}, {user_location['country']}"
                            location_key = f"auto_{lat}_{lon}"
                            st.success(f"Location detected: {location_name}")
                        else:
                            st.error("Could not detect location")
            
            elif location_method == "🔍 Search City":
                search_query = st.text_input("🔍 Search for a city:", placeholder="e.g., Karachi, London, New York")
                
                if search_query:
                    with st.spinner("Searching cities..."):
                        cities = self.search_cities(search_query)
                        if cities:
                            city_options = [f"{city['name']}, {city.get('state', '')}, {city['country']}" for city in cities]
                            selected_city = st.selectbox("Select a city:", city_options, key="city_select")
                            
                            if selected_city:
                                selected_index = city_options.index(selected_city)
                                selected_city_data = cities[selected_index]
                                lat, lon = selected_city_data['lat'], selected_city_data['lon']
                                location_name = selected_city
                                location_key = f"search_{lat}_{lon}"
                        else:
                            st.warning("No cities found. Try a different search term.")
            
            elif location_method == "🌍 Browse by Country":
                countries = self.get_countries()
                selected_country = st.selectbox("🌍 Select Country:", [""] + countries, key="country_select")
                
                if selected_country:
                    city_query = st.text_input(f"🏙️ Enter city in {selected_country}:")
                    if city_query:
                        search_query = f"{city_query}, {selected_country}"
                        cities = self.search_cities(search_query)
                        if cities:
                            city_options = [f"{city['name']}, {city.get('state', '')}" for city in cities]
                            selected_city = st.selectbox("Select city:", city_options, key="country_city_select")
                            if selected_city:
                                selected_index = city_options.index(selected_city)
                                selected_city_data = cities[selected_index]
                                lat, lon = selected_city_data['lat'], selected_city_data['lon']
                                location_name = f"{selected_city}, {selected_country}"
                                location_key = f"country_{lat}_{lon}"
            
            # Check if location has changed
            if location_key and location_key != st.session_state.current_location:
                self.clear_weather_cache()
                st.session_state.current_location = location_key
            
            # Auto-refresh toggle
            st.markdown("---")
            auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=False)
            if auto_refresh:
                # Use a placeholder to implement auto-refresh
                placeholder = st.empty()
                with placeholder:
                    time.sleep(1)
                    st.rerun()
            
            # Manual refresh button
            if st.button("🔄 Refresh Weather Data"):
                self.clear_weather_cache()
                st.rerun()
        
        # Main content
        if lat and lon:
            # Fetch weather data
            if (st.session_state.weather_data is None or 
                st.session_state.last_update is None or 
                (datetime.now() - st.session_state.last_update).seconds > 300):  # Refresh every 5 minutes
                
                with st.spinner("🔄 Fetching real-time weather data..."):
                    weather_data = self.get_weather_data(lat, lon)
                    forecast_data = self.get_forecast_data(lat, lon)
                    
                    if weather_data and forecast_data:
                        st.session_state.weather_data = weather_data
                        st.session_state.forecast_data = forecast_data
                        st.session_state.last_update = datetime.now()
                        st.success("✅ Weather data updated successfully!")
                    else:
                        st.error("❌ Failed to fetch weather data. Please try again.")
                        return
            
            # Display weather data
            if st.session_state.weather_data and st.session_state.forecast_data:
                weather_data = st.session_state.weather_data
                forecast_data = st.session_state.forecast_data
                
                # Verify we have data for the correct location
                if (weather_data.get('coordinates', {}).get('lat') != lat or 
                    weather_data.get('coordinates', {}).get('lon') != lon):
                    # Location changed, force refresh
                    self.clear_weather_cache()
                    st.rerun()
                    return
                
                # Current Weather Section
                st.markdown("## 🌡️ Current Weather")
                self.display_current_weather(weather_data)
                
                # Weather Advice Section
                st.markdown("## 💡 Weather Advice")
                advice = self.generate_weather_advice(weather_data)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); 
                            padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
                    <h4 style="color: #333; margin-top: 0;">🎯 Smart Recommendations</h4>
                    <p style="color: #333; font-size: 1.1rem; margin-bottom: 0;">{advice}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Charts Section
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("## 📈 Temperature Trends")
                    temp_chart = self.create_temperature_chart(forecast_data)
                    st.plotly_chart(temp_chart, use_container_width=True)
                
                with col2:
                    st.markdown("## 📊 Weather Metrics")
                    metrics_chart = self.create_weather_metrics_chart(forecast_data)
                    st.plotly_chart(metrics_chart, use_container_width=True)
                
                # Forecast Section
                self.display_forecast(forecast_data)
                
                # Tomorrow's Weather Section
                st.markdown("## 🌅 Tomorrow's Weather")
                tomorrow_forecasts = [f for f in forecast_data['forecasts'] 
                                    if f['datetime'].date() == (datetime.now().date() + timedelta(days=1))]
                
                if tomorrow_forecasts:
                    # Find noon forecast for tomorrow
                    noon_forecast = None
                    for forecast in tomorrow_forecasts:
                        if forecast['datetime'].hour >= 12:
                            noon_forecast = forecast
                            break
                    if not noon_forecast:
                        noon_forecast = tomorrow_forecasts[0]
                    
                    temps = [f['temperature'] for f in tomorrow_forecasts]
                    max_temp, min_temp = max(temps), min(temps)
                    icon = self.weather_icons.get(noon_forecast['icon'], '🌤️')
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                                padding: 2rem; border-radius: 15px; text-align: center;">
                        <h2 style="color: #333; margin: 0;">{icon} Tomorrow</h2>
                        <h1 style="color: #333; margin: 0.5rem 0;">{max_temp}° / {min_temp}°</h1>
                        <h3 style="color: #333; margin: 0;">{noon_forecast['condition']}</h3>
                        <p style="color: #333; margin: 0.5rem 0;">Wind: {noon_forecast['wind_speed']} km/h | Humidity: {noon_forecast['humidity']}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Last updated info
                st.markdown("---")
                st.markdown(f"""
                <div style="text-align: center; opacity: 0.7;">
                    <small>Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')} | 
                    Data provided by OpenWeatherMap | Developed by hafizullahkhokhar1</small>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            # Welcome screen
            st.markdown("""
            <div style="text-align: center; padding: 3rem;">
                <h2 style="color: white;">👋 Welcome to Modern Weather Dashboard</h2>
                <p style="color: white; opacity: 0.8; font-size: 1.2rem;">
                    Select a location from the sidebar to get started with real-time weather data
                </p>
                <div style="margin-top: 2rem;">
                    <h3 style="color: white;">✨ Features</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
                        <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px;">
                            <h4 style="color: white;">🌡️ Real-time Data</h4>
                            <p style="color: white; opacity: 0.8;">Live weather updates every 5 minutes</p>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px;">
                            <h4 style="color: white;">📈 Interactive Charts</h4>
                            <p style="color: white; opacity: 0.8;">Beautiful visualizations and trends</p>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px;">
                            <h4 style="color: white;">🌍 Global Coverage</h4>
                            <p style="color: white; opacity: 0.8;">Weather data for cities worldwide</p>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px;">
                            <h4 style="color: white;">💡 Smart Advice</h4>
                            <p style="color: white; opacity: 0.8;">Personalized weather recommendations</p>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def main():
    """Main application entry point"""
    dashboard = WeatherDashboard()
    dashboard.run_dashboard()


if __name__ == "__main__":
    main()
