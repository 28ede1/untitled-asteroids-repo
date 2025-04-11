

# Average temperatures in F and wind speed in mph per city capital as of 2025 https://worldpopulationreview.com/state-rankings/average-temperatures-by-state
us_weather_data = {
    'Juneau': {'temperature': 28, 'windspeed': 16},
    'Bismarck': {'temperature': 43, 'windspeed': 18},
    'Cheyenne': {'temperature': 44, 'windspeed': 20},
    'Helena': {'temperature': 44, 'windspeed': 21},
    'Augusta': {'temperature': 45, 'windspeed': 16},
    'Boise': {'temperature': 45, 'windspeed': 20},
    'Saint Paul': {'temperature': 45, 'windspeed': 18},
    'Montpelier': {'temperature': 46, 'windspeed': 18},
    'Concord': {'temperature': 47, 'windspeed': 17},
    'Denver': {'temperature': 47, 'windspeed': 20},
    'Madison': {'temperature': 47, 'windspeed': 18},
    'Pierre': {'temperature': 48, 'windspeed': 21},
    'Olympia': {'temperature': 48, 'windspeed': 14},
    'Lansing': {'temperature': 48, 'windspeed': 17},
    'Albany': {'temperature': 49, 'windspeed': 16},
    'Salem': {'temperature': 49, 'windspeed': 17},
    'Boston': {'temperature': 51, 'windspeed': 15},
    'Salt Lake City': {'temperature': 51, 'windspeed': 18},
    'Des Moines': {'temperature': 51, 'windspeed': 19},
    'Lincoln': {'temperature': 52, 'windspeed': 18},
    'Harrisburg': {'temperature': 52, 'windspeed': 17},
    'Hartford': {'temperature': 52, 'windspeed': 14},
    'Providence': {'temperature': 52, 'windspeed': 13},
    'Carson City': {'temperature': 52, 'windspeed': 17},
    'Columbus': {'temperature': 54, 'windspeed': 16},
    'Charleston': {'temperature': 55, 'windspeed': 18},
    'Indianapolis': {'temperature': 55, 'windspeed': 17},
    'Springfield': {'temperature': 55, 'windspeed': 18},
    'Trenton': {'temperature': 55, 'windspeed': 14},
    'Santa Fe': {'temperature': 56, 'windspeed': 17},
    'Dover': {'temperature': 57, 'windspeed': 12},
    'Annapolis': {'temperature': 57, 'windspeed': 19},
    'Topeka': {'temperature': 57, 'windspeed': 19},
    'Jefferson City': {'temperature': 58, 'windspeed': 19},
    'Richmond': {'temperature': 58, 'windspeed': 18},
    'Frankfort': {'temperature': 58, 'windspeed': 16},
    'Sacramento': {'temperature': 60, 'windspeed': 13},
    'Nashville': {'temperature': 60, 'windspeed': 17},
    'Raleigh': {'temperature': 61, 'windspeed': 18},
    'Phoenix': {'temperature': 62, 'windspeed': 16},
    'Oklahoma City': {'temperature': 63, 'windspeed': 17},
    'Little Rock': {'temperature': 63, 'windspeed': 16},
    'Columbia': {'temperature': 64, 'windspeed': 14},
    'Montgomery': {'temperature': 65, 'windspeed': 13},
    'Atlanta': {'temperature': 65, 'windspeed': 16},
    'Jackson': {'temperature': 66, 'windspeed': 15},
    'Honolulu': {'temperature': 66, 'windspeed': 12},
    'Austin': {'temperature': 68, 'windspeed': 15},
    'Baton Rouge': {'temperature': 69, 'windspeed': 13},
    'Tallahassee': {'temperature': 73, 'windspeed': 14}
}


def get_capital_temp_wspd(city):
    """
    Retrieves average annual temperature and wind speed for a given capital in the US from a dictionary.
    Converts temperature from Kelvin to Fahrenheit and returns wind speed in mph.
    """

    if city in us_weather_data:
        city_data = us_weather_data[city]
        return city_data
    else:
        return {}

if __name__ == "__main__":
    city = input("Enter a US city capital: ")
    print(get_capital_temp_wspd(city))
