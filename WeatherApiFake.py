# Average temperatures in F and wind speed in mph per city capital (Americas)
capital_weather_data = {
    ("42", "50"): {'temperature': 28, 'windspeed': 16, 'city': "Williamstown"}
}

def get_city_temp_wspd(lat, long):

    if (lat, long) in capital_weather_data:
        city_data = capital_weather_data[(lat, long)]
        return city_data
    else:
        return {}


if __name__ == "__main__":
    lat, long = "42", "50"
    print(get_city_temp_wspd(lat, long))
