import json
import os.path
import os


"""
Data to be saved is game difficulty (which uses location, location temperature
and location windspeed), as well as the game's leaderboard. At first, these 
are the defaults to use before any save file has been used.
"""

def save_game_data_file(data_dictionary):
    """
    Saves the provided dictionary to a file in JSON format inside the SavedGameData folder.
    data_dictionary is the data you want the game to save. If save data file doesn't
    exist, it will create one, and write the provided dictionary to a file
    called player_data.txt. If a file already exists its data will be overridden.
    """

    save_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "SavedGameData/player_data.txt"))
    with open(save_file_path, "w") as game_save_file:
        json.dump(data_dictionary, game_save_file)


def load_gamesave_file():
    """
    Returns the game data from the 'player_data.txt' file located in the
    'SavedGameData' folder if there exist data there. The function reads the JSON data from the file,
    and returns the resulting dictionary. If the file is empty, return defaults.
    """
    save_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "SavedGameData/player_data.txt"))
    
    # If the file has data in it, return said data 
    if os.path.getsize(save_file_path) > 0:
        with open(save_file_path) as game_save_file:
            return json.load(game_save_file)
        
    # Return defaults
    else:
        data = {
            "Game Leaderboard": [],
            "Location": "Default",
            "Location temperature": 55,
            "Location wind speed range": [200, 250],
        }
        return data


def erase_game_save_file():
    """
    Erases all data in the dictionary by setting each key's value to the defaults. Returns a fresh dictionary.
    """
    fresh_data = {"Game Leaderboard": [], "Location": "Default", "Location temperature": 65, "Location wind speed range": [200, 250]}
    return fresh_data
