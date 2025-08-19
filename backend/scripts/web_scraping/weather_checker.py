import requests
import json
import sys
from datetime import datetime

class WeatherChecker:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.backup_apis = [
            "http://api.weatherapi.com/v1",
            "https://api.weatherbit.io/v2.0"
        ]
    
    def get_weather_by_city(self, city, units="metric"):
        if not self.api_key:
            return self.get_weather_free(city)
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self.format_weather_data(data, units)
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return self.get_weather_free(city)
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_weather_by_coordinates(self, lat, lon, units="metric"):
        if not self.api_key:
            print("Coordinates require API key")
            return None
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self.format_weather_data(data, units)
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_weather_forecast(self, city, days=5, units="metric"):
        if not self.api_key:
            print("Forecast requires API key")
            return None
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units,
                "cnt": days * 8
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self.format_forecast_data(data, units)
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_weather_free(self, city):
        try:
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self.format_wttr_data(data)
            
        except Exception as e:
            print(f"Free weather service failed: {e}")
            return None
    
    def format_weather_data(self, data, units):
        temp_unit = "°C" if units == "metric" else "°F"
        speed_unit = "m/s" if units == "metric" else "mph"
        
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": f"{data['main']['temp']:.1f}{temp_unit}",
            "feels_like": f"{data['main']['feels_like']:.1f}{temp_unit}",
            "description": data["weather"][0]["description"].title(),
            "humidity": f"{data['main']['humidity']}%",
            "pressure": f"{data['main']['pressure']} hPa",
            "wind_speed": f"{data['wind']['speed']} {speed_unit}",
            "visibility": f"{data.get('visibility', 'N/A')} m",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return weather_info
    
    def format_forecast_data(self, data, units):
        temp_unit = "°C" if units == "metric" else "°F"
        forecast_list = []
        
        for item in data["list"][:40:8]:
            forecast_info = {
                "date": datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d"),
                "temperature": f"{item['main']['temp']:.1f}{temp_unit}",
                "description": item["weather"][0]["description"].title(),
                "humidity": f"{item['main']['humidity']}%"
            }
            forecast_list.append(forecast_info)
        
        return {
            "city": data["city"]["name"],
            "forecast": forecast_list
        }
    
    def format_wttr_data(self, data):
        current = data["current_condition"][0]
        weather_info = {
            "city": "Location",
            "country": "",
            "temperature": f"{current['temp_C']}°C",
            "feels_like": f"{current['FeelsLikeC']}°C",
            "description": current["weatherDesc"][0]["value"],
            "humidity": f"{current['humidity']}%",
            "pressure": f"{current['pressure']} hPa",
            "wind_speed": f"{current['windspeedKmph']} km/h",
            "visibility": f"{current['visibility']} km",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return weather_info
    
    def display_weather(self, weather_data):
        if not weather_data:
            print("No weather data available")
            return
        
        print("\n" + "="*50)
        print("🌤️  WEATHER INFORMATION")
        print("="*50)
        print(f"📍 Location: {weather_data['city']}, {weather_data['country']}")
        print(f"🌡️  Temperature: {weather_data['temperature']}")
        print(f"🤔 Feels like: {weather_data['feels_like']}")
        print(f"☁️  Conditions: {weather_data['description']}")
        print(f"💧 Humidity: {weather_data['humidity']}")
        print(f"📊 Pressure: {weather_data['pressure']}")
        print(f"💨 Wind Speed: {weather_data['wind_speed']}")
        print(f"👁️  Visibility: {weather_data['visibility']}")
        print(f"⏰ Updated: {weather_data['timestamp']}")
        print("="*50)
    
    def display_forecast(self, forecast_data):
        if not forecast_data:
            print("No forecast data available")
            return
        
        print(f"\n5-Day Forecast for {forecast_data['city']}")
        print("="*40)
        
        for day in forecast_data['forecast']:
            print(f"📅 {day['date']}")
            print(f"   🌡️  {day['temperature']}")
            print(f"   ☁️  {day['description']}")
            print(f"   💧 {day['humidity']}")
            print("-" * 30)
    
    def save_weather_data(self, weather_data, filename="weather_log.json"):
        if not weather_data:
            return
        
        try:
            with open(filename, 'r') as f:
                log_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            log_data = []
        
        log_data.append(weather_data)
        
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"Weather data saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python weather_checker.py <city> [api_key] [units]")
        print("       python weather_checker.py forecast <city> [api_key] [days]")
        print("       python weather_checker.py coords <lat> <lon> [api_key]")
        print("Units: metric (default), imperial")
        sys.exit(1)
    
    if sys.argv[1] == "forecast":
        if len(sys.argv) < 3:
            print("Usage: forecast <city> [api_key] [days]")
            sys.exit(1)
        
        city = sys.argv[2]
        api_key = sys.argv[3] if len(sys.argv) > 3 else None
        days = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        
        checker = WeatherChecker(api_key)
        forecast = checker.get_weather_forecast(city, days)
        checker.display_forecast(forecast)
    
    elif sys.argv[1] == "coords":
        if len(sys.argv) < 4:
            print("Usage: coords <lat> <lon> [api_key]")
            sys.exit(1)
        
        lat = float(sys.argv[2])
        lon = float(sys.argv[3])
        api_key = sys.argv[4] if len(sys.argv) > 4 else None
        
        checker = WeatherChecker(api_key)
        weather = checker.get_weather_by_coordinates(lat, lon)
        checker.display_weather(weather)
    
    else:
        city = sys.argv[1]
        api_key = sys.argv[2] if len(sys.argv) > 2 else None
        units = sys.argv[3] if len(sys.argv) > 3 else "metric"
        
        checker = WeatherChecker(api_key)
        weather = checker.get_weather_by_city(city, units)
        checker.display_weather(weather)
        
        if weather:
            save = input("\nSave weather data? (y/n): ").lower()
            if save == 'y':
                checker.save_weather_data(weather)
