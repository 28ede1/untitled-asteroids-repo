# An Untitled Asteroids Game

Asteroids game clone where you survive as long as possible avoiding asteroids while collecting powerups to keep you alive and treasure to increase your score.

## Requirements
    
  * Python 3.9+ (seems to work best for python 3.12)

## Installation/Setup

  * git clone this_repository
  * cd untitled-asteroids-repo
  * pip install -r requirements.txt
  * get weather api key from https://rapidapi.com/weatherbit/api/weather/playground/5933364be4b08ab68dbc3786
  * create .env file in project_root and set WEATHER_API_KEY=your_api_key

## To run

python Game.py

## Core Gameplay

### Game Controls

  * Move Player - Arrow Keys
  * Shoot Asteroid - Spacebar

#### Asteroids
Asteroids spawn randomly from the top of the screen and fall to the bottom of the screen at different times. Asteroids come in three types: Normal (Deals regular damage to the player upon collision), Icy (Deals less damage but freezes the player for a brief period), Fiery (Deals more damage to the player).

#### Player, Powerups

While avoiding asteroids, the player can collect various items; Treasure increases the player's score, Ammo refills the player's ammo capacity, Health packs restore player health, and Oxygen tanks can be shot to collect the resulting oxygen bubble to. Player oxygen drains over time and the player must manage ammo to collect enough oxygen bubbles to survive. The player's score multiplier also increases as they collect treasures and power-ups while avoiding asteroid collisions. However, the multiplier resets if the player is hit by an asteroid.

#### Difficulty Progression

The game features a dynamic difficulty system that adjusts based on the player’s survival time: 

Asteroid Frequency: Initially, asteroids spawn at regular intervals. As the player survives, the number of asteroids increases.

Asteroid Speed: Over time, the speed range of asteroids increases in a set number of intervals, making it increasingly harder to avoid asteroids.

The user can go into options and change the difficulty by typing a location in latitude,longitude format. The locations temperature is used to determine
the types of asteroids that spawn, and the wind speed is used to determine the starting speed range of the asteroids.

#### Weather API Usage

A weather API collects temperature and wind speed information for a latitude, longitude location entered by the player through the Difficulty button in the options menu. The temperature is used to modify the distribution of asteroid types, simulating weather-impact on asteroid spawning. The wind speed influences the default speed at which asteroids spawn.

#### Weather "Api" (fake version)

Contains seperate function for retrieving location temperature and windspeed from latitute and longitude parameters. Meant to mock the main WeatherAPI get method.

#### Save/Load Feature

The game includes a save/load feature that allows players to save their difficulty settings (temperature and wind speed) based on location provided, in addition to saving leaderboard data. The player can also click a button in settings to reset data to a fresh save file.

#### Leaderboard

Upon death, the player’s time survived and points are recorded in a leaderboard, which tracks the top 5 scores.

## Gameplay Demo 

[![Video Title](https://img.youtube.com/vi/HkXz9sZ7LCc/maxresdefault.jpg)](https://youtu.be/HkXz9sZ7LCc) 

## Screenshots 

![Image](https://github.com/user-attachments/assets/81c6e9b8-80dc-4d3a-8df3-12543938e3e9)
![Image](https://github.com/user-attachments/assets/0e654e30-d04c-42c6-be5e-627beb832cf3)
![Image](https://github.com/user-attachments/assets/b6ba0ef1-a3fa-4aff-9524-1819eda80059)
![Image](https://github.com/user-attachments/assets/1cf8714f-59b4-48a7-bbb5-30f066ed14e5)
    
## Project Structure
The codebase is organized into several modules:

  * Game.py handles main game mechanics, difficulty, traversing menu screens
  * Sprites.py contains classes for game entities
  * WeatherApi.py handles API calls for weather data
  * WeatherApiFake.py handles getting a location weather data as a mock for WeatherApi.py
  * MyTimer.py handles timers used for various game/player mechanics
  * Assets.py manages the loading of textures (including sound, music)
  * Settings.py has constants used by the other python files
  * GameSaver.py handles game saving/loading/erasing of player data
  * GameMenu.py handles content displayed for each menu screen
  * DoublyLinkedStack.py is the data structure used for menu traversal
  * InputBox.py handles a text input box used for location selection

  * audio, font, and images folders store audio files, fonts, and image files respectively
  * SavedGameData folder saves player_data file used for retrieve saved player information
## Credits

Sprite Assets:

  * Hearts and Health Bar by VampireGirl, itch.io https://fliflifly.itch.io/hearts-and-health-bar (Creative Commons 0)

  * Space Shooter Redux by Kenny, https://www.kenney.nl/assets/space-shooter-redux (Creative Commons 0)

  * Water Cannon VFX by anton_chi, https://anton-chi.itch.io/water-cannon (Free for Personal and Commercial Use, no redistribution)

  * Treasure+ by SchiGho, https://ninjikin.itch.io/treasure, (Creative Commons BY 4.0)

  * 8-Bit Screen By Tisã, https://samplefocus.com/samples/8-bit-scream (Standard License, Royalty Free)

  * Spacebar, https://www.pixilart.com/art/spacebar-55abfeff259a667

  * The King's Heart (loop) by Free Game Music 1, https://soundcloud.com/rmaren/movement-while-my-heart-still, (Creative Commons License)

  * Pixabay Content License (https://pixabay.com/service/license-summary/):

  * Retro Coin 4 by nettimato, https://pixabay.com/sound-effects/retro-coin-4-236671/

  * Coin Received by RibhavAgrawal, https://pixabay.com/sound-effects/coin-recieved-230517/

  * Sci-Fi Bubble Pop by paespedro, https://pixabay.com/sound-effects/sci-fi-bubble-pop-89059/

  * Mag In by nettimato, https://pixabay.com/sound-effects/mag-in-82094/

  * Lighter Click by Alex_Jauk, https://pixabay.com/sound-effects/lighter-click-271118/

  * Menu Button by Leszek_Szary,  https://pixabay.com/sound-effects/menu-button-88360/

  * Breaking Glass by wjl, https://pixabay.com/sound-effects/breaking-glass-84819/