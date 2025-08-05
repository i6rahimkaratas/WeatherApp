from config import API_KEY
import requests

print(f"API Key uzunluğu: {len(API_KEY)}")
print(f"API Key ilk 8 karakter: {API_KEY[:8]}")

# Basit test
url = "http://api.openweathermap.org/data/2.5/weather"
params = {
    'q': 'London',
    'appid': API_KEY,
    'units': 'metric'
}

response = requests.get(url, params=params)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text[:200]}")