# Average temperatures in F and wind speed in mph per city capital (Americas)
capital_weather_data = {
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
    'Olympia': {'temperature': 48, 'windspeed': 15},
    'Lansing': {'temperature': 48, 'windspeed': 17},
    'Albany': {'temperature': 49, 'windspeed': 15},
    'Salem': {'temperature': 49, 'windspeed': 16},
    'Boston': {'temperature': 51, 'windspeed': 15},
    'Salt Lake City': {'temperature': 51, 'windspeed': 18},
    'Des Moines': {'temperature': 51, 'windspeed': 18},
    'Lincoln': {'temperature': 52, 'windspeed': 18},
    'Harrisburg': {'temperature': 52, 'windspeed': 17},
    'Hartford': {'temperature': 52, 'windspeed': 14},
    'Providence': {'temperature': 52, 'windspeed': 14},
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
    'Richmond': {'temperature': 58, 'windspeed': 19},
    'Frankfort': {'temperature': 58, 'windspeed': 16},
    'Sacramento': {'temperature': 60, 'windspeed': 13},
    'Nashville': {'temperature': 60, 'windspeed': 17},
    'Raleigh': {'temperature': 61, 'windspeed': 18},
    'Phoenix': {'temperature': 62, 'windspeed': 15},
    'Oklahoma City': {'temperature': 63, 'windspeed': 16},
    'Little Rock': {'temperature': 63, 'windspeed': 16},
    'Columbia': {'temperature': 64, 'windspeed': 15},
    'Montgomery': {'temperature': 65, 'windspeed': 14},
    'Atlanta': {'temperature': 65, 'windspeed': 15},
    'Jackson': {'temperature': 66, 'windspeed': 15},
    'Honolulu': {'temperature': 66, 'windspeed': 14},
    'Austin': {'temperature': 68, 'windspeed': 15},
    'Baton Rouge': {'temperature': 69, 'windspeed': 13},
    'Tallahassee': {'temperature': 73, 'windspeed': 14}, 
    'Edmonton': {'temperature': 37, 'windspeed': 7},
    'Victoria': {'temperature': 50, 'windspeed': 6},
    'Winnipeg': {'temperature': 39, 'windspeed': 11},
    'Fredericton': {'temperature': 42, 'windspeed': 10},
    "St. John's": {'temperature': 41, 'windspeed': 14},
    'Halifax': {'temperature': 45, 'windspeed': 9},
    'Toronto': {'temperature': 48, 'windspeed': 9},
    'Charlottetown': {'temperature': 43, 'windspeed': 9},
    'Québec City': {'temperature': 41, 'windspeed': 9},
    'Regina': {'temperature': 39, 'windspeed': 11},
    'Yellowknife': {'temperature': 17, 'windspeed': 8},
    'Iqaluit': {'temperature': 10, 'windspeed': 10},
    'Whitehorse': {'temperature': 30, 'windspeed': 6}, 'Aguascalientes': {'temperature': 68, 'windspeed': 7},
    'Mexicali': {'temperature': 77, 'windspeed': 9},
    'La Paz': {'temperature': 75, 'windspeed': 8},
    'Campeche': {'temperature': 80, 'windspeed': 10},
    'Tuxtla Gutiérrez': {'temperature': 79, 'windspeed': 6},
    'Chihuahua': {'temperature': 65, 'windspeed': 7},
    'Saltillo': {'temperature': 62, 'windspeed': 8},
    'Colima': {'temperature': 81, 'windspeed': 5},
    'Mexico City': {'temperature': 64, 'windspeed': 5},
    'Durango': {'temperature': 61, 'windspeed': 7},
    'Guanajuato': {'temperature': 66, 'windspeed': 6},
    'Chilpancingo': {'temperature': 77, 'windspeed': 5},
    'Pachuca': {'temperature': 60, 'windspeed': 7},
    'Guadalajara': {'temperature': 72, 'windspeed': 6},
    'Toluca': {'temperature': 59, 'windspeed': 6},
    'Morelia': {'temperature': 70, 'windspeed': 6},
    'Cuernavaca': {'temperature': 73, 'windspeed': 5},
    'Tepic': {'temperature': 75, 'windspeed': 6},
    'Monterrey': {'temperature': 74, 'windspeed': 7},
    'Oaxaca': {'temperature': 70, 'windspeed': 5},
    'Puebla': {'temperature': 63, 'windspeed': 6},
    'Querétaro': {'temperature': 66, 'windspeed': 6},
    'Chetumal': {'temperature': 80, 'windspeed': 9},
    'San Luis Potosí': {'temperature': 65, 'windspeed': 7},
    'Culiacán': {'temperature': 78, 'windspeed': 6},
    'Hermosillo': {'temperature': 80, 'windspeed': 7},
    'Villahermosa': {'temperature': 81, 'windspeed': 8},
    'Ciudad Victoria': {'temperature': 77, 'windspeed': 7},
    'Tlaxcala': {'temperature': 62, 'windspeed': 6},
    'Xalapa': {'temperature': 68, 'windspeed': 7},
    'Mérida': {'temperature': 82, 'windspeed': 9},
    'Zacatecas': {'temperature': 60, 'windspeed': 7}
}


def get_capital_temp_wspd(city):
    """
    Retrieves average annual temperature and wind speed for a given capital in the US from a dictionary.
    Converts temperature from Kelvin to Fahrenheit and returns wind speed in mph.
    """

    if city in capital_weather_data:
        city_data = capital_weather_data[city]
        return city_data
    else:
        return {}

if __name__ == "__main__":
    city = input("Enter a US city capital: ")
    print(len(capital_weather_data) == len(set(capital_weather_data.keys())))
    print(get_capital_temp_wspd(city))
    