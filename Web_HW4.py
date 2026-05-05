
import requests

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=test_key"
    response = requests.get(url)
    return response.json()

from weather import get_weather
from unittest.mock import patch

# Тест: перевірка успішного отримання даних
@patch("weather.requests.get")
def test_get_weather_success(mock_get):
    mock_get.return_value.json.return_value = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 300}
    }

    result = get_weather("Kyiv")

    assert result["weather"][0]["description"] == "clear sky"
    assert result["main"]["temp"] == 300


# Тест: перевірка структури відповіді
@patch("weather.requests.get")
def test_get_weather_keys(mock_get):
    mock_get.return_value.json.return_value = {
        "weather": [{}],
        "main": {}
    }

    result = get_weather("Kyiv")

    assert "weather" in result
    assert "main" in result