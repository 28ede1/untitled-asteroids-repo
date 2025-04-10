

# Average temperatures in F and wind speed in mph per state as of 2025 https://worldpopulationreview.com/state-rankings/average-temperatures-by-state
us_weather_data={
    'Alaska': {'temperature': 28, 'windspeed': 16},
    'North Dakota': {'temperature': 43, 'windspeed': 18},
    'Wyoming': {'temperature': 44, 'windspeed': 20},
    'Montana': {'temperature': 44, 'windspeed': 21},
    'Maine': {'temperature': 45, 'windspeed': 16},
    'Idaho': {'temperature': 45, 'windspeed': 20},
    'Minnesota': {'temperature': 45, 'windspeed': 18},
    'Vermont': {'temperature': 46, 'windspeed': 18},
    'New Hampshire': {'temperature': 47, 'windspeed': 17},
    'Colorado': {'temperature': 47, 'windspeed': 20},
    'Wisconsin': {'temperature': 47, 'windspeed': 18},
    'South Dakota': {'temperature': 48, 'windspeed': 21},
    'Washington': {'temperature': 48, 'windspeed': 15},
    'Michigan': {'temperature': 48, 'windspeed': 17},
    'New York': {'temperature': 49, 'windspeed': 15},
    'Oregon': {'temperature': 49, 'windspeed': 16},
    'Massachusetts': {'temperature': 51, 'windspeed': 15},
    'Utah': {'temperature': 51, 'windspeed': 18},
    'Iowa': {'temperature': 51, 'windspeed': 18},
    'Nebraska': {'temperature': 52, 'windspeed': 18},
    'Pennsylvania': {'temperature': 52, 'windspeed': 17},
    'Connecticut': {'temperature': 52, 'windspeed': 14},
    'Rhode Island': {'temperature': 52, 'windspeed': 14},
    'Nevada': {'temperature': 52, 'windspeed': 17},
    'Ohio': {'temperature': 54, 'windspeed': 16},
    'West Virginia': {'temperature': 55, 'windspeed': 18},
    'Indiana': {'temperature': 55, 'windspeed': 17},
    'Illinois': {'temperature': 55, 'windspeed': 18},
    'New Jersey': {'temperature': 55, 'windspeed': 14},
    'New Mexico': {'temperature': 56, 'windspeed': 17},
    'Delaware': {'temperature': 57, 'windspeed': 12},
    'Maryland': {'temperature': 57, 'windspeed': 19},
    'Kansas': {'temperature': 57, 'windspeed': 19},
    'Missouri': {'temperature': 58, 'windspeed': 19},
    'Virginia': {'temperature': 58, 'windspeed': 19},
    'Kentucky': {'temperature': 58, 'windspeed': 16},
    'California': {'temperature': 60, 'windspeed': 13},
    'Tennessee': {'temperature': 60, 'windspeed': 17},
    'North Carolina': {'temperature': 61, 'windspeed': 18},
    'Arizona': {'temperature': 62, 'windspeed': 15},
    'Oklahoma': {'temperature': 63, 'windspeed': 16},
    'Arkansas': {'temperature': 63, 'windspeed': 16},
    'South Carolina': {'temperature': 64, 'windspeed': 15},
    'Alabama': {'temperature': 65, 'windspeed': 14},
    'Georgia': {'temperature': 65, 'windspeed': 15},
    'Mississippi': {'temperature': 66, 'windspeed': 15},
    'Hawaii': {'temperature': 66, 'windspeed': 14},
    'Texas': {'temperature': 68, 'windspeed': 15},
    'Louisiana': {'temperature': 69, 'windspeed': 13},
    'Florida': {'temperature': 73, 'windspeed': 14}
}


def get_state_temp_wspd(state):
    """
    Retrieves average annual temperature and wind speed for a given state in the US from a dictionary.
    Converts temperature from Kelvin to Fahrenheit and returns wind speed in mph.
    """

    if state in us_weather_data:
        state_data = us_weather_data[state]
        return state_data

if __name__ == "__main__":
    state = input("Enter a US state: ")
    print(get_state_temp_wspd(state))
