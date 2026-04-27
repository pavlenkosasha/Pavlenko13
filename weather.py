import requests

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=test_key"
    response = requests.get(url)
    return response.json()