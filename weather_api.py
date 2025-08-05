import requests
import geocoder
from config import API_KEY, BASE_URL

class WeatherAPI:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL
        self.use_mock = True 
    
    def get_current_location(self):
        """Kullanıcının mevcut konumunu al"""
        try:
            g = geocoder.ip('me')
            if g.ok:
                return g.latlng[0], g.latlng[1], g.city
            return 36.9081, 30.6956, "Antalya" 
        except Exception as e:
            return 36.9081, 30.6956, "Antalya"
    
    def toggle_mock_mode(self, use_mock=True):
        """Mock mode'u aç/kapat"""
        self.use_mock = use_mock
    
    def search_city(self, city_name):
        """Şehir arama"""
        if self.use_mock:
            mock_cities = [
                {"name": "İstanbul", "lat": 41.0082, "lon": 28.9784, "country": "TR"},
                {"name": "Ankara", "lat": 39.9334, "lon": 32.8597, "country": "TR"},
                {"name": "İzmir", "lat": 38.4237, "lon": 27.1428, "country": "TR"},
                {"name": "Antalya", "lat": 36.9081, "lon": 30.6956, "country": "TR"},
                {"name": "Bursa", "lat": 40.1926, "lon": 29.0611, "country": "TR"},
                {"name": "Adana", "lat": 37.0000, "lon": 35.3213, "country": "TR"},
                {"name": "Gaziantep", "lat": 37.0662, "lon": 37.3833, "country": "TR"},
                {"name": "Konya", "lat": 37.8667, "lon": 32.4833, "country": "TR"}
            ]
            
            # Türkçe karakter desteği için normalize et
            search_term = city_name.lower().replace('ı', 'i').replace('ş', 's').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o').replace('ç', 'c')
            
            results = []
            for city in mock_cities:
                city_normalized = city["name"].lower().replace('ı', 'i').replace('ş', 's').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o').replace('ç', 'c')
                if search_term in city_normalized or city_normalized.startswith(search_term):
                    results.append(city)
            
            return results
        
        # Gerçek API kodu
        try:
            url = f"http://api.openweathermap.org/geo/1.0/direct"
            params = {
                'q': city_name,
                'limit': 5,
                'appid': self.api_key
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Şehir arama hatası: {e}")
            return []
    
    def get_weather_by_coords(self, lat, lon):
        
        if self.use_mock:
            
            mock_weather_data = {
                
                (41.0082, 28.9784): {
                    "name": "İstanbul",
                    "main": {"temp": 18.5, "feels_like": 19.2, "humidity": 72, "pressure": 1015},
                    "weather": [{"main": "Clouds", "description": "parçalı bulutlu", "icon": "02d"}],
                    "wind": {"speed": 4.1},
                    "coord": {"lat": lat, "lon": lon}
                },
                
                (39.9334, 32.8597): {
                    "name": "Ankara",
                    "main": {"temp": 15.2, "feels_like": 16.1, "humidity": 68, "pressure": 1018},
                    "weather": [{"main": "Clear", "description": "açık", "icon": "01d"}],
                    "wind": {"speed": 2.8},
                    "coord": {"lat": lat, "lon": lon}
                },
                
                "default": {
                    "name": "Test Şehri",
                    "main": {"temp": 22.5, "feels_like": 24.2, "humidity": 65, "pressure": 1013},
                    "weather": [{"main": "Clear", "description": "açık", "icon": "01d"}],
                    "wind": {"speed": 3.2},
                    "coord": {"lat": lat, "lon": lon}
                }
            }
            
            
            for coord, data in mock_weather_data.items():
                if coord != "default" and isinstance(coord, tuple):
                    if abs(coord[0] - lat) < 0.1 and abs(coord[1] - lon) < 0.1:
                        return data
            
            
            return mock_weather_data["default"]
        
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'tr'
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Hava durumu alınamadı: {e}")
            return None