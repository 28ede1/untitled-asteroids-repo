import requests
import os
from dotenv import load_dotenv


"""
This API parses data from a weather information database. This implementation specifically retreives 
"""

load_dotenv()
apikey = os.getenv("WEATHER_API_KEY")

if not apikey:
    raise RuntimeError("API_KEY is not set")

def get_city_temp_wspd(lat, long):

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
    city_data_to_return = {"temperature" : weather['data'][0]['temp'], "windspeed" : weather['data'][0]['wind_spd'], "city_name" : weather['data'][0]['city_name']}

    return city_data_to_return

if __name__ == "__main__":
    lat, long = "42.7", "-73.2"
    print(get_city_temp_wspd(lat, long))


