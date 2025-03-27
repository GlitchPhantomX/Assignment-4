import requests
import sys

def get_weather_data(location, api_key):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    try:
        complete_url = f"{base_url}?q={location}&appid={api_key}&units=metric"
        response = requests.get(complete_url)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def display_weather(data):
    if not data:
        return
    
    if data.get('cod') != 200:
        print(f"Error: {data.get('message', 'Unknown error')}")
        return
    
    try:
        main = data['main']
        weather = data['weather'][0]
        sys = data.get('sys', {})
        
        print("\n" + "="*40)
        print(f"Weather in {data['name']}, {sys.get('country', 'N/A')}")
        print("="*40)
        print(f"🌡 Temperature: {main['temp']}°C (Feels like: {main.get('feels_like', 'N/A')}°C)")
        print(f"📊 Pressure: {main['pressure']} hPa")
        print(f"💧 Humidity: {main['humidity']}%")
        print(f"☁ Weather: {weather['description'].capitalize()}")
        print(f"🌬 Wind: {data.get('wind', {}).get('speed', 'N/A')} m/s")
        print(f"👀 Visibility: {data.get('visibility', 'N/A')} meters")
        print("="*40 + "\n")
    except KeyError as e:
        print(f"Error parsing weather data: Missing key {e}")

def main():
    print("🌦 Weather App 🌦")
    print("----------------")
    
    try:
        with open('api_key.txt', 'r') as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        api_key = input("Enter your OpenWeatherMap API key (or create one at openweathermap.org): ")
        with open('725445a93053bb679c6f64a1402bd0ce', 'w') as f:
            f.write(api_key)
    
    while True:
        location = input("\nEnter city name (or 'quit' to exit): ").strip()
        if location.lower() in ('quit', 'exit', 'q'):
            break
            
        weather_data = get_weather_data(location, api_key)
        display_weather(weather_data)

if __name__ == "__main__":
    main()