import requests

API_KEY = "46273699e3eeb2daf4fc23d0a4132048"

def fetch_weather(latitude, longitude):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        weather_data = {
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed']
        }
        return weather_data
    else:
        print("Error fetching weather data:", response.status_code, response.text)
        return None

# Test Example:
if __name__ == "__main__":
    latitude = 28.6139    # Example: Delhi coordinates
    longitude = 77.2090

    weather = fetch_weather(latitude, longitude)
    print("Real-time Weather Data:", weather)