from weather import get_weather
from unittest.mock import patch

@patch("weather.requests.get")
def test_get_weather_success(mock_get):
    mock_get.return_value.json.return_value = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 300}
    }

    result = get_weather("Kyiv")

    assert result["weather"][0]["description"] == "clear sky"
    assert result["main"]["temp"] == 300