import requests
import os
from dotenv import load_dotenv
import math


load_dotenv()
apikey = os.getenv("WEATHER_API_KEY")

# Whether a real weather API key is configured. When False, the game falls back
# to the offline WeatherApiFake so it can run with zero setup.
API_KEY_AVAILABLE = bool(apikey)

"""
This API parses data from a weather information database. This implementation specifically retreives
temperature and windspeed information from a latitute,longitude location specified
"""

def get_location_lat_long_temp_wspd(lat, long):

    # Without a configured key we can't query the real API; signal an error so
    # callers fall back to defaults (or the offline mock).
    if not apikey:
        return {"error": "WEATHER_API_KEY is not set"}

    # ensures parameters represent integers or float strings, which are required to query
    try:
        lat = float(lat)
        long = float(long)
    except (ValueError, TypeError):
        return {"error": "lat and long must be numbers"}

    querystring = {"lon": long,"lat": lat,"units":"imperial","lang":"en"}

    url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"

    headers = {
        "x-rapidapi-key": apikey,
        "x-rapidapi-host": "weatherbit-v1-mashape.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        return {"error": "Failed to fetch data. Please try again later."}

    weather = response.json()
    location_data_to_return = {"temperature" : math.ceil(weather['data'][0]['temp']), "windspeed" : math.ceil(weather['data'][0]['wind_spd']), "city_name" : weather['data'][0]['city_name']}

    return location_data_to_return

if __name__ == "__main__":
    lat, long = "42.7", "-73.2"
    print(get_location_lat_long_temp_wspd(lat, long))


