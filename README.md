# An Untitled Asteroids Game

A retro-styled Asteroids game clone where you survive as long as possible avoiding asteroids while collecting powerups to keep you alive and treasure to increase your score. 

## Prequisities/Libraries needed

  * Knowledge of Object-Oriented Programming, Inheritance, File Processing, Data Strutures, and Game-Loop logic
  * Knowledge of utilizing API's
  * WeatherApi (https://rapidapi.com/oktamovshohjahon/api/weather-api138/playground/apiendpoint_acb2971f-25d4-4a29-b5d6-87b9f3f8131b)
  * Python, installed with the pip package
  * pyray, raylib, pygbag, requests libraries installed
  * Dependencies: cffi, pycparser, idna, certifi, urllib3, charset-normalizer
  
## To play the game via web browser: 

  (Note: Work in progess, expect bugs with the screen display*, minimize screen for best results.)
  
  Click here: https://28ede1.github.io/untitled-asteroids-repo/
  
## To run the program in your terminal:

1. Install Python (with pip included) if it is not already installed

   * You can type, python --version, in terminal to see the version number if it exists. 

2. Install the raylib package (installing raylib should install the raylib/pyray modules). 

   * pip install raylib
     
3. Install the requests module (for the Weather API). 

   * pip install requests

4. Git clone this repository

5. In the WeatherApi.py get_city_temp_wsp() method, replace url and headers with your API information

   * Make sure you are subscribed to the api
   * The header containing the key and host, can be pasted from here, as well as the url
     
6. Inside the folder top folder (ex: untitled_asteroids_repository) type, 
   * python Game.py

## Core Gameplay

This game utilizes a state stack system to manage various game screens, enabling smooth transitions between menus and gameplay. The core gameplay loop activates when the game enters the Gameplay state. The game involves avoiding randomly spawning asteroids, collecting treasures, and managing resources, with a progressive difficulty system that adapts as the player survives. The player can choose a city, and the cities weather data is used by the program to change the types of asteroids that can spawn as well as their speeds.

#### Asteroids
Asteroids spawn randomly from the top of the screen and are deleted upon exiting the edges of the game window. Asteroids come in three types: Normal (Deals regular damage to the player upon collision), Icy (Deals less damage but freezes the player for a brief period), Fiery (Deals more damage to the player).

#### Player, Powerups

While avoiding asteroids, the player can collect various items; Treasure increases the player's score, Ammo refills the player's ammo capacity, Health packs restore player health, and Oxygen tanks can be shot to collect the resulting oxygen bubble to. Player oxygen drains over time and the player must manage ammo to collect enough oxygen bubbles to survive. The player's score multiplier also increases as they collect treasures and power-ups while avoiding asteroid collisions. However, the multiplier resets if the player is hit by an asteroid.

#### Difficulty Progression

The game features a dynamic difficulty system that adjusts based on the player’s survival time: 

Asteroid Frequency: Initially, asteroids spawn at regular intervals. As the player survives, the number of asteroids increases.

Asteroid Speed: Over time, the speed range of asteroids increases in a set number of intervals, making the game more challenging.

The user can go into options and change the difficulty by typing a city. The cities temperature is used to determine
the types of asteroids that spawn, and the wind speed is used to determine the starting speed range of the asteroids.

#### Weather API Usage

https://rapidapi.com/oktamovshohjahon/api/weather-api138/playground/apiendpoint_acb2971f-25d4-4a29-b5d6-87b9f3f8131b

A weather API collects temperature and wind speed information for a city entered by the player through the Difficulty button in the options menu. The temperature is used to modify the distribution of asteroid types, simulating weather-impact on asteroid spawning. The wind speed influences the default speed at which asteroids spawn.

#### Weather "Api" (fake version)

As of 4/10/2025, the import requests module is not compatible for pgybag, the library used for running the python code in browser. So, a seperate class with a custom get method selects a cities temperature and wind speed information from a dictionary. The temperature and windspeed work the same.

#### Save/Load Feature

The game includes a save/load feature that allows players to save their difficulty settings (temperature and wind speed). This ensures that the game will remember the player's last difficulty configuration when resumed. The player can also click a button in settings to reset data to a fresh save file.

#### Leaderboard

Upon death, the player’s time survived and points are recorded in a leaderboard, which tracks the top 5 scores.

## Game Controls

  * Move Player - Arrow Keys
  * Shoot Asteroid - Spacebar

## Gameplay Demo (game.py ran in terminal version)

[![Video Title](https://img.youtube.com/vi/HkXz9sZ7LCc/0.jpg)](https://youtu.be/HkXz9sZ7LCc) 

## Screenshots (game.py ran in terminal version)

![Image](https://github.com/user-attachments/assets/848e3a33-85b3-4694-b306-830418d6a5d2)
![Image](https://github.com/user-attachments/assets/0e654e30-d04c-42c6-be5e-627beb832cf3)
![Image](https://github.com/user-attachments/assets/81c6e9b8-80dc-4d3a-8df3-12543938e3e9)
![Image](https://github.com/user-attachments/assets/b6ba0ef1-a3fa-4aff-9524-1819eda80059)
![Image](https://github.com/user-attachments/assets/1cf8714f-59b4-48a7-bbb5-30f066ed14e5)

## Author's Notes

### Purpose

  * To practice implementing a data structure in a practical use case (Ex: Using a stack to implement a menu screen and button navigation system efficiently)
  * To Practice with complex OOP and structuring a complex program in a reasonable way way
  * To understand and appreciate the basic intricacies of what goes into game development
    
### Project Structure
The codebase is organized into several modules:

  * Game.py handles game mechanics, difficulty, traversing menu screens
    This version is used for running the game via terminal.
  * main.py handles game mechanics, difficulty, traversing menu screens
    This version is used for running the game in browser.
    main.py will use a "mock" version of the weather get request, since the Api used    
    for this project doesn't work as indended for main.py
  * Sprites.py contains classes for game entities
  * WeatherApi.py handles API calls for weather data (used by game.py)
  * WeatherApiFake.py handles getting a city capital weather data (used by main.py)
  * MyTimer.py handles timers used for various game/player mechanics
  * Assets.py manages the loading of textures (including sound, music)
  * Settings.py has constants used by the other python files
  * GameSaver.py handles game saving/loading/erasing of player data
  * Menu
  * DoublyLinkedStack.py is the data structure used for menu traversal
  * InputBox.py handles a text input box used for city selection
  

### Design process

  * Created the gaming objects, utilizing an inheritance structure. All moving/none moving entities like asteroids, players, powerups, and treasure inherited a 2D sprite class meant to encapsulate functionality
  * Created the game loop and mechanics
  * Created the Menu System once the game loop has been finished
  * Implemented API for gathering temperature and wind speed of a city, in order to be used for the difficulty system
  * Implemented a button that allowed the user to change the city being selected, thereby changed the game's difficulty
  * Created a Save/Load file system to save leaderboard information and city data for when the game is ran again.
  * Figured out how to deploy a web version of the game on github
  * Created a WeatherApiFake class for handling weather input for a city for the browser version of the game run with main.py
  
### Challenges

  * How to structure a game from scratch: Start from building the menu system? Or start from bulding the game loop?
  * Implementing the menu system: Originally used a handful of booleans to determine what screens should be currently draw. This was not only cumbersome to develop more menu screens further (since more boolean logic would have to be introduced) but also error prone (with me having to keep track of the nested logic). My approach to this was using a first in-last in approach to menu states, with the use of a linked Stack data structure. 
  * Learning a complete new graphics library (Raylib), took some time to understand.
  * Memory management was a concern when it came to figuring out how to infinitely drawn powers while player is alive. There would need to be a system to keep track of the list of asteroids, power ups, and treasure leaving the screen as well as one deletion as the objects left the game screen. I used lists to keep track of the maximum objects that can be spawned as well as iterate through the game objects currently drawn on screen to determine whether to delete any.
  * Learned how to properly install Python with functions like pip and pyinstaller, as well as how to properly set python to Path system environment variable so that python can be typed in the terminal regardless of what folder you are in. Had to learn in order to use pip for installing dependencies/modules
  * Had to learn how to install a module with pip (and ensure that python is installed with pip)
  * Configuring the game to run via webbrowser using pygbag + raylib

### How i figured out how to run (IGNORE THIS, this is just for my future reference)

1. Installed Python if it is not already installed

   * You can type, python --version, in terminal to see the version number if it exists. The version used to implement this program was Python 3.13.2 on Windows for reference.
   
   * If not, install the latest version of python here for your operating system: https://www.python.org/downloads/

   * Be sure to add pip as an optional feature to download, and add Python to Path System Environment Variable.

2. Install the latest version of pip if it isn't installed already

   * python -m pip install --upgrade pip

3. Install the raylib package (installing raylib installs the raylib/pyray modules)

   * python -m pip install setuptools
   * python -m pip install raylib==5.5.0.0

4. Install the requests module (for the Weather API) 

   * python.exe -m pip install requests
   * Note that this installs the module globally*

5. Git clone this repository
   
6. Inside the folder code type
   * python Game.py
  
For deploying a version a game in browser (for future reference only):

1. Have a main.py file at the top directory of the folder.
2. Import sys, Import asyncio at the top of the file
3. Find the main game loop function. Make it an async function by 1. adding async before the def keyword and 2. adding await asyncio.sleep(0) after the .enddrawing() method (or similar counter part) inside the while loop
4. Last line of the main.py file should be asyncio.run(SpaceGame().run_optimized()). Nothing should come after this.
5. Like in the WeatherApi.py file, if there is an import requests, this will cause an error. Replace with the following..
   
import sys

if sys.platform not in ("emscripten", "wasi"):
    import requests

   to fix this. API just wont work without doing this.
   
6. Follow these instructions for running the first deployment.

  note: for raylib, under run:

  sudo apt-get install ffmpeg pngquant
  python3 -m pip install git+https://github.com/pygame-web/pygbag
  python3 -m pygbag --build --git --template noctx-nofs.tmpl --ume_block 0 $GITHUB_WORKSPACE/main.py

  you must add the first line, and must add --git like shown to the 3rd line
  
  https://pygame-web.github.io/wiki/publishing/github.io/

  Follow the rest of the instructions for deploying.

  Link should be published to username.github.io/repo-name/
  
## Credits

Sprite Assets:

  * Hearts and Health Bar by VampireGirl, itch.io https://fliflifly.itch.io/hearts-and-health-bar (Creative Commons 0)
  * Space Shooter Redux by Kenny, https://www.kenney.nl/assets/space-shooter-redux (Creative Commons 0)
  * Water Cannon VFX by anton_chi, https://anton-chi.itch.io/water-cannon (Free for Personal and Commercial Use, no redistribution)
  * Treasure+ by SchiGho, https://ninjikin.itch.io/treasure, (Creative Commons BY 4.0)
  * 8-Bit Screen By Tisã, https://samplefocus.com/samples/8-bit-scream (Standard License, Royalty Free)
  * Spacebar, https://www.pixilart.com/art/spacebar-55abfeff259a667
  * The King's Heart (loop) by Free Game Music 1, https://soundcloud.com/rmaren/movement-while-my-heart-still, (Creative Commons License)

Pixabay Content License (https://pixabay.com/service/license-summary/):

  * Retro Coin 4 by nettimato, https://pixabay.com/sound-effects/retro-coin-4-236671/
  * Coin Received by RibhavAgrawal, https://pixabay.com/sound-effects/coin-recieved-230517/
  * Sci-Fi Bubble Pop by paespedro, https://pixabay.com/sound-effects/sci-fi-bubble-pop-89059/
  * Mag In by nettimato, https://pixabay.com/sound-effects/mag-in-82094/
  * Lighter Click by Alex_Jauk, https://pixabay.com/sound-effects/lighter-click-271118/
  * Menu Button by Leszek_Szary,  https://pixabay.com/sound-effects/menu-button-88360/
  * Breaking Glass by wjl, https://pixabay.com/sound-effects/breaking-glass-84819/

## Known Issues/Features to add

* BUG: game freezes for a bit when choosing a new city for the first time. Likely to do with the Weather API. (When ran using python Game.py)
* BUG: Screen sizing and mouse cursor position is off (depending on device) when running the web version
* FEATURE: implement a save/load file system somehow for the web version
