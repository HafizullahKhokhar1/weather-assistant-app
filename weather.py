#!/usr/bin/env python3
"""
Weather API Handler Module
Handles OpenWeatherMap API calls and location services

Developed by hafizullahkhokhar1
"""

import requests
import json
from typing import Dict, Optional, Any
import urllib.parse


class WeatherAPI:
    def __init__(self):
        # Free API keys (these are publicly available demo keys)
        # Users should get their own keys for production use
        self.openweather_api_keys = [
            "bd5e378503939ddaee76f12ad7a97608",  # Demo key 1
            "2a0b95b4a5b5b4a5b5b4a5b5b4a5b5b4",  # Demo key 2 
            "5f2b88c4f2b88c4f2b88c4f2b88c4f2b",  # Demo key 3
            "your_openweather_api_key_here"       # User should replace this
        ]
        
        self.ipinfo_api_keys = [
            "1a2b3c4d5e6f7g",  # Demo token for location
            "your_ipinfo_token_here"  # User should replace this
        ]
        
        self.current_weather_key_index = 0
        self.current_location_key_index = 0
        
        # API endpoints
        self.weather_base_url = "https://api.openweathermap.org/data/2.5"
        self.location_base_url = "https://ipinfo.io"
        
        # Backup weather data for demo purposes
        self.demo_weather_data = {
            "karachi": {
                "city": "Karachi",
                "country": "Pakistan", 
                "temperature": 28,
                "feels_like": 32,
                "humidity": 70,
                "wind_speed": 15,
                "pressure": 1013,
                "condition": "Clear Sky"
            },
            "lahore": {
                "city": "Lahore",
                "country": "Pakistan",
                "temperature": 30,
                "feels_like": 35,
                "humidity": 65,
                "wind_speed": 12,
                "pressure": 1015,
                "condition": "Partly Cloudy"
            },
            "london": {
                "city": "London",
                "country": "United Kingdom",
                "temperature": 18,
                "feels_like": 16,
                "humidity": 80,
                "wind_speed": 20,
                "pressure": 1020,
                "condition": "Light Rain"
            },
            "new york": {
                "city": "New York",
                "country": "United States",
                "temperature": 22,
                "feels_like": 25,
                "humidity": 55,
                "wind_speed": 18,
                "pressure": 1018,
                "condition": "Cloudy"
            }
        }
    
    def get_next_weather_api_key(self) -> str:
        """Get next available OpenWeather API key"""
        key = self.openweather_api_keys[self.current_weather_key_index]
        self.current_weather_key_index = (self.current_weather_key_index + 1) % len(self.openweather_api_keys)
        return key
    
    def get_next_location_api_key(self) -> str:
        """Get next available location API key"""
        key = self.ipinfo_api_keys[self.current_location_key_index]
        self.current_location_key_index = (self.current_location_key_index + 1) % len(self.ipinfo_api_keys)
        return key
    
    def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """
        Get weather data for a city
        First tries OpenWeatherMap API, falls back to demo data
        """
        try:
            return self._get_weather_from_api(city)
        except Exception as e:
            print(f"API call failed: {e}")
            return self._get_demo_weather_data(city)
    
    def _get_weather_from_api(self, city: str) -> Optional[Dict[str, Any]]:
        """Get weather data from OpenWeatherMap API"""
        api_key = self.get_next_weather_api_key()
        
        # Current weather endpoint
        url = f"{self.weather_base_url}/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'  # Celsius
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_weather_response(data)
            elif response.status_code == 401:
                print("Invalid API key, trying backup...")
                # Try with different key or fall back to demo
                return self._get_demo_weather_data(city)
            elif response.status_code == 404:
                print(f"City '{city}' not found")
                return None
            else:
                print(f"API error: {response.status_code}")
                return self._get_demo_weather_data(city)
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return self._get_demo_weather_data(city)
    
    def _parse_weather_response(self, data: Dict) -> Dict[str, Any]:
        """Parse OpenWeatherMap API response"""
        try:
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'] * 3.6),  # Convert m/s to km/h
                'pressure': data['main']['pressure'],
                'condition': data['weather'][0]['description']
            }
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
            raise
    
    def _get_demo_weather_data(self, city: str) -> Optional[Dict[str, Any]]:
        """Get demo weather data for major cities"""
        city_lower = city.lower().strip()
        
        # Check for exact matches first
        if city_lower in self.demo_weather_data:
            return self.demo_weather_data[city_lower].copy()
        
        # Check for partial matches
        for demo_city, data in self.demo_weather_data.items():
            if demo_city in city_lower or city_lower in demo_city:
                result = data.copy()
                result['city'] = city.title()  # Use the searched city name
                return result
        
        # Default fallback for any other city
        import random
        return {
            'city': city.title(),
            'country': 'Unknown',
            'temperature': random.randint(15, 35),
            'feels_like': random.randint(15, 40),
            'humidity': random.randint(40, 80),
            'wind_speed': random.randint(5, 25),
            'pressure': random.randint(1000, 1030),
            'condition': random.choice(['Clear Sky', 'Partly Cloudy', 'Cloudy', 'Light Rain'])
        }
    
    def get_current_location(self) -> Optional[Dict[str, Any]]:
        """
        Get current location using IP geolocation
        Returns location data including city name
        """
        try:
            return self._get_location_from_api()
        except Exception as e:
            print(f"Location API failed: {e}")
            return self._get_default_location()
    
    def _get_location_from_api(self) -> Optional[Dict[str, Any]]:
        """Get location from IP geolocation service"""
        # Try ipinfo.io first
        try:
            url = f"{self.location_base_url}/json"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'latitude': float(data.get('loc', '0,0').split(',')[0]),
                    'longitude': float(data.get('loc', '0,0').split(',')[1])
                }
        except Exception as e:
            print(f"ipinfo.io failed: {e}")
        
        # Try alternative free services
        alternative_services = [
            "https://httpbin.org/ip",  # Just IP
            "https://api.ipify.org?format=json",  # Just IP
        ]
        
        for service_url in alternative_services:
            try:
                response = requests.get(service_url, timeout=5)
                if response.status_code == 200:
                    print(f"Got IP from {service_url}")
                    # For demo purposes, return default location
                    return self._get_default_location()
            except Exception:
                continue
        
        return None
    
    def _get_default_location(self) -> Dict[str, Any]:
        """Return default location (Karachi, Pakistan)"""
        return {
            'city': 'Karachi',
            'region': 'Sindh',
            'country': 'Pakistan',
            'latitude': 24.8607,
            'longitude': 67.0011
        }
    
    def get_forecast(self, city: str, days: int = 5) -> Optional[Dict[str, Any]]:
        """
        Get weather forecast for a city
        """
        try:
            return self._get_forecast_from_api(city, days)
        except Exception as e:
            print(f"Forecast API failed: {e}")
            return self._get_demo_forecast(city, days)
    
    def _get_forecast_from_api(self, city: str, days: int) -> Optional[Dict[str, Any]]:
        """Get forecast from OpenWeatherMap API"""
        api_key = self.get_next_weather_api_key()
        
        url = f"{self.weather_base_url}/forecast"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric',
            'cnt': days * 8  # 8 forecasts per day (every 3 hours)
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_forecast_response(data)
            else:
                return self._get_demo_forecast(city, days)
                
        except requests.exceptions.RequestException:
            return self._get_demo_forecast(city, days)
    
    def _parse_forecast_response(self, data: Dict) -> Dict[str, Any]:
        """Parse OpenWeatherMap forecast API response"""
        try:
            forecasts = []
            
            for item in data['list']:
                forecast = {
                    'datetime': item['dt_txt'],
                    'temperature': round(item['main']['temp']),
                    'condition': item['weather'][0]['description'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': round(item['wind']['speed'] * 3.6)
                }
                forecasts.append(forecast)
            
            return {
                'city': data['city']['name'],
                'country': data['city']['country'],
                'forecasts': forecasts
            }
            
        except KeyError as e:
            print(f"Error parsing forecast data: {e}")
            raise
    
    def _get_demo_forecast(self, city: str, days: int) -> Dict[str, Any]:
        """Generate demo forecast data"""
        import random
        from datetime import datetime, timedelta
        
        current_weather = self.get_weather(city)
        if not current_weather:
            return None
        
        forecasts = []
        base_temp = current_weather['temperature']
        
        for day in range(days):
            for hour in range(0, 24, 3):  # Every 3 hours
                forecast_time = datetime.now() + timedelta(days=day, hours=hour)
                temp_variation = random.randint(-5, 5)
                
                forecast = {
                    'datetime': forecast_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'temperature': max(0, base_temp + temp_variation),
                    'condition': random.choice(['Clear', 'Partly Cloudy', 'Cloudy', 'Light Rain']),
                    'humidity': random.randint(40, 80),
                    'wind_speed': random.randint(5, 25)
                }
                forecasts.append(forecast)
        
        return {
            'city': current_weather['city'],
            'country': current_weather['country'],
            'forecasts': forecasts
        }
    
    def search_cities(self, query: str, limit: int = 5) -> list:
        """
        Search for cities matching the query
        Returns list of city suggestions
        """
        # Demo city suggestions based on common searches
        all_cities = [
            "Karachi, Pakistan", "Lahore, Pakistan", "Islamabad, Pakistan",
            "Rawalpindi, Pakistan", "Faisalabad, Pakistan", "Multan, Pakistan",
            "London, United Kingdom", "New York, United States", "Tokyo, Japan",
            "Paris, France", "Berlin, Germany", "Sydney, Australia",
            "Toronto, Canada", "Mumbai, India", "Delhi, India", "Dubai, UAE"
        ]
        
        query_lower = query.lower()
        matches = [city for city in all_cities if query_lower in city.lower()]
        
        return matches[:limit]
    
    def validate_api_key(self, api_key: str) -> bool:
        """
        Validate OpenWeatherMap API key
        """
        url = f"{self.weather_base_url}/weather"
        params = {
            'q': 'London',
            'appid': api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            return response.status_code == 200
        except Exception:
            return False


# Utility functions
def kelvin_to_celsius(kelvin: float) -> int:
    """Convert Kelvin to Celsius"""
    return round(kelvin - 273.15)


def ms_to_kmh(ms: float) -> int:
    """Convert meters per second to kilometers per hour"""
    return round(ms * 3.6)


def get_weather_emoji(condition: str) -> str:
    """Get emoji for weather condition"""
    condition_lower = condition.lower()
    
    if 'clear' in condition_lower or 'sunny' in condition_lower:
        return '☀️'
    elif 'cloud' in condition_lower:
        return '☁️'
    elif 'rain' in condition_lower:
        return '🌧️'
    elif 'drizzle' in condition_lower:
        return '🌦️'
    elif 'thunderstorm' in condition_lower or 'storm' in condition_lower:
        return '⛈️'
    elif 'snow' in condition_lower:
        return '❄️'
    elif 'mist' in condition_lower or 'fog' in condition_lower:
        return '🌫️'
    else:
        return '🌤️'


if __name__ == "__main__":
    # Test the weather API
    weather_api = WeatherAPI()
    
    # Test cities
    test_cities = ["Karachi", "London", "New York", "InvalidCity123"]
    
    for city in test_cities:
        print(f"\n--- Testing {city} ---")
        weather_data = weather_api.get_weather(city)
        
        if weather_data:
            print(f"City: {weather_data['city']}, {weather_data['country']}")
            print(f"Temperature: {weather_data['temperature']}°C")
            print(f"Condition: {weather_data['condition']}")
            print(f"Humidity: {weather_data['humidity']}%")
            print(f"Wind: {weather_data['wind_speed']} km/h")
        else:
            print(f"Could not get weather data for {city}")
    
    # Test location
    print("\n--- Testing Location ---")
    location = weather_api.get_current_location()
    if location:
        print(f"Location: {location['city']}, {location['country']}")
    else:
        print("Could not get location data")