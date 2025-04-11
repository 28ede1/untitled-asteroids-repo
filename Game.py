import Sprites
import Assets
import WeatherApi
import GameSaver
import GameMenu
import random
import GameInputBox
import MyTimer
import Settings
import raylib
import pyray

class SpaceGame:
    """
    SpaceGame() handles game mechanics. It manages game states, difficulty progression,
    spawning/despawning of asteroids/treasure/powerups, music, and weather-based mechanics.
    The game's difficulty get's increasingly difficult as the game runs; SpaceGame()
    uses an API to adapt difficulty based on temperature and wind speed data of
    real life cities. Colder temperatures spawn more icy asteroids, hotter temperatures spawn
    fiery ones.
    """

    def __init__(self):

        # Creates the outerspace game background
        self._stars_list = []
        self.make_stars()

        # Weather-based difficulty parameters
        previous_save = GameSaver.load_gamesave_file()
        self._game_temperature_custom = previous_save["City temperature"]
        self._max_speed_range_custom = previous_save["City wind speed range"]
        self._city_custom = previous_save["City selected"]

        # Default difficulty parameters as a failsafe
        # Based on the city, there is a default speed rand to use
        # Save the max speed list copy in order to prevent reference errors
        self._max_speed_range_default = self._max_speed_range_custom[:]
        self._game_temperature_default = self._game_temperature_custom
        self._city_default = self._city_custom

        # Progressive difficulty spawning and speed range difficulty cycles
        self._asteroid_spawning_level = 0
        self._asteroid_speed_level = 0
        self._asteroid_spawn_increase_timer = MyTimer.Timer(4, True, False, self.capped_asteroid_spawn_timer)
        self._asteroid_speed_increase_timer = MyTimer.Timer(10, True, False, self.capped_asteroid_speed_timer)

        # Game entity storage
        self._asteroids_list = []
        self._max_asteroids = 6
        self._power_ups = []  # list of powerup objects
        self._treasure = []  # list of treasure objects

        # Core game component objects
        self._player = Sprites.Spaceship()
        self._game_clock = Sprites.Clock(Assets.game_assets.get_asset_font("slkscr.ttf"))
        self._menu = GameMenu.Menu()  # integrates menu system used by the game

        # Audio management
        self._game_music = Assets.game_assets.get_asset_music("game_music.ogg")
        pyray.set_music_volume(self._game_music, 0.4)
        self._is_music_playing = False

        # Temperature to asteroid type mapping - influences game dynamics based on real-world weather
        self._temperature_to_asteroid_chance = {
            (-float("inf"), 5): {"normal": 0, "icy": 100, "fiery": 0},
            (6, 14): {"normal": 20, "icy": 80, "fiery": 0},
            (15, 23): {"normal": 40, "icy": 60, "fiery": 0},
            (24, 32): {"normal": 45, "icy": 55, "fiery": 0},
            (33, 40): {"normal": 60, "icy": 40, "fiery": 0},
            (41, 50): {"normal": 75, "icy": 25, "fiery": 0},
            (51, 60): {"normal": 85, "icy": 15, "fiery": 0},
            (61, 65): {"normal": 75, "icy": 0, "fiery": 25},
            (66, 70): {"normal": 65, "icy": 0, "fiery": 35},
            (71, 76): {"normal": 30, "icy": 0, "fiery": 70},
            (77, 81): {"normal": 20, "icy": 0, "fiery": 80},
            (82, 90): {"normal": 0, "icy": 0, "fiery": 100},
            (91, 200): {"normal": 0, "icy": 0, "fiery": 100},
        }

        # Used for random name generation for leaderboard entries
        self._char_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Input box positioned near difficulty button for city input
        self._user_input_box = GameInputBox.InputBox(
            pyray.Vector2(Settings.ADJUSTED_WIDTH / 2 - 240 * Settings.SCALE_FACTOR, 250 * Settings.SCALE_FACTOR), Assets.game_assets.get_asset_font("slkscr.ttf"), 
            30 * Settings.SCALE_FACTOR, 470 * Settings.SCALE_FACTOR, 60 * Settings.SCALE_FACTOR, 18, raylib.RED, raylib.WHITE, raylib.BLACK,
            "Enter City"
        )

        # Game Screen Transitioning
        self._screens = {
            "main_menu": self.handle_main_menu,
            "death_menu": self.handle_death_menu,
            "leaderboard": self.handle_leaderboard_menu,
            "options": self.handle_options_menu,
            "start_game": self.handle_start_game,
            "loading_screen": self.handle_loading_screen,
        }

    def start_music(self):
        """Starts the game music if it's not already playing."""
        if not self._is_music_playing:
            pyray.play_music_stream(self._game_music)
            self._is_music_playing = True

    def stop_music(self):
        """Stops the game music if it's currently playing."""
        if self._is_music_playing:
            pyray.stop_music_stream(self._game_music)
            self._is_music_playing = False

    def play_game_over_sfx(self):
        """Play a game over jingle."""
        game_over = Assets.game_assets.get_asset_sound("game_over.ogg")
        pyray.set_sound_volume(game_over, 0.2)
        pyray.play_sound(game_over)
        self.stop_music()

    def play_damage_sfx(self):
        crash = Assets.game_assets.get_asset_sound("crash.ogg")
        pyray.set_sound_volume(crash, 0.2)
        pyray.play_sound(crash)

    def _play_treasure_collect_sfx(self):
        """
        Plays the treasure collection sound.
        """
        collect = Assets.game_assets.get_asset_sound("treasure_collect.ogg")
        pyray.set_sound_volume(collect, 0.2)
        pyray.play_sound(collect)

    def collect_item(self, item, collect_sfx):
        """Helper function to handle power-up collection effects and audio."""
        self.play_collection_sfx(collect_sfx)
        self._power_ups.remove(item)

    def play_collection_sfx(self, collect_sfx):
        sound = Assets.game_assets.get_asset_sound(collect_sfx)
        pyray.set_sound_volume(sound, 0.5)
        pyray.play_sound(sound)

    def update_leaderboard_list(self):
        """Save player score and time lasted to leaderboard."""
        random_name = "".join(random.choices(self._char_string, k=4))
        score = self._player._score_tracker.get_current_points()
        time = self._game_clock.get_current_time()
        self.add_to_leaderboard_list(random_name, score, time)

    def add_to_leaderboard_list(self, random_name, score, time):
        """Append player data to leaderboard list appropriately."""
        if len(self._menu._leaderboard) < 5:
            self._menu._leaderboard.append((random_name, score, time))

        # Maintains a top-5 leaderboard based on score
        elif score >= self._menu._leaderboard[-1][1]:
            self._menu._leaderboard = self._menu._leaderboard[:-1]
            self._menu._leaderboard.append((random_name, score, time))

    def reset_background(self):
        """Reset the outerspace background."""
        self._stars_list.clear()
        self.make_stars()

    def reset_asteroids(self):
        """Clears the asteroids on screen and resets asteroid spawn cap."""
        self._asteroids_list.clear()
        self._max_asteroids = 6

    def reset_difficulty(self):
        """
        Reset the asteroid spawn and speed difficulty levels.
        Set the speed range diffcult to the base speed dependent on the city.
        """
        
        # Use a copy to prevent reference problems
        self._max_speed_range_custom = self._max_speed_range_default[:]
        self._asteroid_spawning_level = 0
        self._asteroid_speed_level = 0

        # Recalibrate the timing of spawn difficulty increase before the speed difficulty increase
        self._asteroid_spawn_increase_timer = MyTimer.Timer(4, True, False, self.capped_asteroid_spawn_timer)
        self._asteroid_speed_increase_timer = MyTimer.Timer(10, True, False, self.capped_asteroid_speed_timer)

    def clear_collectibles(self):
        """Clears all powerups and treasure objects."""
        self._power_ups.clear()
        self._treasure.clear()

    def set_to_death_screen(self):
        """Update menu state flags to set the screen to the death screen."""

        """
        Old system
        self._menu._in_death_menu = True
        self._menu._start_game = False
        """

        # pop the current state (which was start game)
        # push the death menu state
        self._menu._menu_state_stack.pop()
        self._menu._menu_state_stack.push("death_menu")

    def reset_game(self):
        """
        Resets the game state after player death, updates leaderboard,
        and returns to the death menu. Maintains a top-5 leaderboard
        based on score. Reset players data, clear all asteroids and collectibles that spawned,
        reset to the game's starting difficulty.
        """
        self.update_leaderboard_list()
        self.reset_background()
        self.reset_asteroids()
        self.reset_difficulty()
        self.clear_collectibles()
        self._player.reset_player()
        self.set_to_death_screen()
        self.play_game_over_sfx()
        self._game_clock.reset_time()

    def capped_asteroid_speed_timer(self):
        """
        Increases asteroid level over time up to a cap of 6 levels.
        Each level adds 70 speed units to both lower and upper bounds,
        creating a steady difficulty curve as the game progresses.
        """
        if self._asteroid_speed_level < 6:
            self._asteroid_speed_level += 1
            # Increase both min and max speed values by 70 units per level
            self._max_speed_range_custom[0] += 70
            self._max_speed_range_custom[1] += 70

    def capped_asteroid_spawn_timer(self):
        """
        Increases maximum asteroids level on screen over time up to a cap
        of 7 levels. Each level adds 2 more possible asteroids,
        gradually increasing game difficulty.
        """
        if self._asteroid_spawning_level < 7:
            self._asteroid_spawning_level += 1
            self._max_asteroids += 2

    def initiate_asteroid_spawning_mechanics(self):
        """
        Controls the difficulty progression system. First increases asteroid count,
        then transitions to increasing asteroid speed after count reaches maximum.
        This creates a two-phase difficulty curve.
        """
        # Only start increasing speed after max spawn level is reached
        if self._asteroid_spawning_level == 7:
            self._asteroid_speed_increase_timer.active = True
            self._asteroid_speed_increase_timer.update()
        else:
            self._asteroid_spawn_increase_timer.active = True
            self._asteroid_spawn_increase_timer.update()

    def make_stars(self):
        """Generates stars at random positions"""
        for i in range(50):
            random_star_pos = pyray.Vector2(random.randint(0, Settings.ADJUSTED_WIDTH), random.randint(0, Settings.ADJUSTED_HEIGHT))
            self._stars_list.append(
                Sprites.Star(Assets.game_assets.get_asset_texture("star.png"), random_star_pos, 0, pyray.Vector2(15, 15), pyray.Vector2(0, 0))
            )

    def draw_outer_space(self):
        """Manages the twinkling stars background effect."""
        for star in self._stars_list:
            star.dynamically_grow()
            star.movement_update(pyray.Vector2(0, 0), 0, pyray.Vector2(0, 0), (255,255,255,255))

    def draw_treasure(self):
        """
        Spawns treasure with value-weighted randomness.
        Common items (iron) appear more frequently than rare items (diamonds).
        Treasures fall vertically through space.
        """
        self.create_treasure()
        self.handle_treasure_deletion()

    def draw_asteroids(self):
        """
        Spawns and manages asteroids with type probabilities determined
        by temperature. Different asteroid types imply unique behaviors:
        fiery (more damage), icy (freezing effect), and normal.
        Asteroids rotate as they move across screen
        """
        self.create_asteroids()
        for asteroid in self._asteroids_list[:]:
            asteroid.dynamically_rotate()
            asteroid.project_asteroid()
        self.handle_asteroid_deletion()

    def draw_power_ups(self):
        """
        Spawns power-ups with weighted probabilities based on usefulness.
        Each power-up type has unique spawn locations and movement patterns:
        - O2: spawns from top, moves down
        - Ammo: spawns from left, moves right
        - Health: spawns from right, moves left
        The varied item movement patterns require careful player movement to collect
        power ups. Powerups are deleted when they leave the screen.
        """

        self.create_power_up()
        self.handle_power_up_deletion()

    def create_treasure(self):
        """
        Adds treasure if there isn't already one on the screen.
        The treasure is selected with weighted randomness to favor common items.
        """
        treasure_variations = random.choice(
            [
                "diamond.png",
                "emerald.png",
                "emerald.png",
                "ruby.png",
                "iron.png",
                "iron.png",
                "iron.png",
                "iron.png",
                "emerald.png",
                "ruby.png",
                "iron.png",
            ]
        )
        treasure_speed = 200
        if len(self._treasure) < 1:
            random_treasure_pos = pyray.Vector2(random.randint(20, Settings.ADJUSTED_WIDTH - 60), random.randint(-4000, -1000))
            treasure_direction = pyray.Vector2(0, 1)
            treasure = Sprites.Treasure(random_treasure_pos, treasure_speed, treasure_direction)
            treasure.set_texture(Assets.game_assets.get_asset_texture(treasure_variations))
            # Add to treasure list for spawning
            self._treasure += [treasure]

    def create_single_asteroid(self):
        """Creates a single asteroid to add to asteroid list."""
        random_asteroid_pos = pyray.Vector2(random.randint(-15, Settings.ADJUSTED_WIDTH + 30), random.randint(-100, -50))
        random_asteroid_speed = random.randint(self._max_speed_range_custom[0], self._max_speed_range_custom[1])
        random_asteroid_direction = pyray.Vector2(random.randint(-1, 1), 1)

        # Get asteroid_type distributions
        type_chances = self.determine_asteroids_temperature_chance()

        # Weighted selection of asteroid type
        asteroid_type = random.choices(
            ["normal", "icy", "fiery"], weights=[type_chances["normal"], type_chances["icy"], type_chances["fiery"]], k=1
        )[0]

        # Create asteroid based on determined type
        if asteroid_type == "fiery":
            current_asteroid = Sprites.Asteroid(
                random_asteroid_pos,
                random_asteroid_speed,
                random_asteroid_direction,
                pyray.Vector2(101, 84),
                Assets.game_assets.get_asset_texture("fiery_meteor.png"),
            )
        elif asteroid_type == "icy":
            current_asteroid = Sprites.Asteroid(
                random_asteroid_pos,
                random_asteroid_speed,
                random_asteroid_direction,
                pyray.Vector2(101, 84),
                Assets.game_assets.get_asset_texture("icy_meteor.png"),
            )
        else:
            current_asteroid = Sprites.Asteroid(random_asteroid_pos, random_asteroid_speed, random_asteroid_direction)
        self._asteroids_list += [current_asteroid]

    def create_asteroids(self):
        """
        Adds asteroid as long as max hasn't been reached yet.
        """
        if len(self._asteroids_list) < self._max_asteroids:
            self.create_single_asteroid()

    def create_power_up(self):
        """
        Adds a power-up to the game, ensuring that:
        - Only one power-up of each type is active at a time.
        - The power-up is selected based on weighted randomness (favoring more common items).
        - The selected power-up has its own spawn position and movement direction.
        Power-ups can be:
        - O2: Oxygen power-up, moves down from the top of the screen.
        - Ammo: Ammunition power-up, moves from left to right.
        - HP: Health power-up, moves from right to left.
        This method handles the creation and addition of a new power-up to the game.
        """
        select_pwrup = random.choice(["O2", "O2", "O2", "O2", "O2", "HP", "HP", "HP", "Ammo", "Ammo", "Ammo", "Ammo", "Ammo"])
        pwrup_speed = 300

        # Based on the powerup type, have a spawn rate, position and direction of movement, and class
        self._power_up_stats = {
            "O2": {
                "class": Sprites.O2_PowerUP,
                "rarity": 13,
                "pos": pyray.Vector2(random.randint(20, Settings.ADJUSTED_WIDTH - 60), random.randint(-1500, -500)),
                "direction": pyray.Vector2(0, 1),
            },
            "Ammo": {
                "class": Sprites.Ammo_PowerUP,
                "rarity": 4,
                "pos": pyray.Vector2(random.randint(-3000, -500), random.randint(20, Settings.ADJUSTED_HEIGHT - 60)),
                "direction": pyray.Vector2(1, 0),
            },
            "HP": {
                "class": Sprites.HeartCapsule_PowerUP,
                "rarity": 1,
                "pos": pyray.Vector2(random.randint(Settings.ADJUSTED_WIDTH, 3000), random.randint(20, Settings.ADJUSTED_HEIGHT - 60)),
                "direction": pyray.Vector2(-1, 0),
            },
        }

        # Ensure only one power-up of the selected type is on screen at a time
        if len(self._power_ups) < 1 and not any(
            isinstance(pwrup, self._power_up_stats[select_pwrup]["class"]) for pwrup in self._power_ups
        ):
            select_pwrup_stats = self._power_up_stats[select_pwrup]
            self._power_ups.append(
                select_pwrup_stats["class"](select_pwrup_stats["pos"], pwrup_speed, select_pwrup_stats["direction"])
            )

    def handle_treasure_deletion(self):
        """
        Updates the position of each treasure as it falls and removes it if it falls off the screen.
        """
        for treasure in self._treasure[:]:
            # remove treasure objects as they exit the sides of the screens
            treasure.movement_update(treasure.get_direction(), 0, pyray.Vector2(0, 0), (255,255,255,255))
            pos = treasure.get_position()
            if pos.y > Settings.ADJUSTED_HEIGHT:
                self._treasure.remove(treasure)

    def handle_asteroid_deletion(self):
        """
        Updates the position of each asteroid as it falls
        and removes it if it falls off the screen.
        """
        for asteroid in self._asteroids_list[:]:

            # Update asteroid position
            pos = asteroid.get_position()
            if pos.y > Settings.ADJUSTED_HEIGHT or (pos.x < -15 or pos.x > Settings.ADJUSTED_WIDTH + 30):
                self._asteroids_list.remove(asteroid)

    def handle_power_up_deletion(self):
        """
        Updates the position of each power differently based on type.
        remove powerup if it goes off the screen.
        """
        for power_up in self._power_ups[:]:
            # Note: Movement update of each power_up is initilized differently to change movement
            power_up.movement_update(power_up.get_direction(), 0, pyray.Vector2(0, 0), (255,255,255,255))
            pos = power_up.get_position()

            if isinstance(power_up, Sprites.O2_PowerUP):
                if pos.y > Settings.ADJUSTED_HEIGHT:
                    self._power_ups.remove(power_up)
            elif isinstance(power_up, Sprites.Ammo_PowerUP):
                if pos.x > Settings.ADJUSTED_WIDTH:
                    self._power_ups.remove(power_up)
            elif isinstance(power_up, Sprites.HeartCapsule_PowerUP):
                if pos.x < -15:
                    self._power_ups.remove(power_up)

    def determine_asteroids_temperature_chance(self):
        """
        Maps current temperature to asteroid type probabilities.
        Ries real-world weather data to gameplay, helping create
        varied difficulty based on chosen location. Returns
        the distribution for the game to use.
        """
        temperature = self._game_temperature_custom

        # Default distribution if no matching temperature range
        chances = {"normal": 33, "icy": 33, "fiery": 34}

        for temp_range in self._temperature_to_asteroid_chance:
            # Check if the temperature falls within any of the defined ranges and update the chances accordingly
            if temp_range[0] <= temperature <= temp_range[1]:
                chances = self._temperature_to_asteroid_chance[temp_range]
                break
        return chances

    def deal_player_damage(self, texture):
        """
        Damage player based on asteroid texture.
        Reset score multiplier for player.
        """
        # Fiery meteors deal triple damage
        if texture == Assets.game_assets.get_asset_texture("fiery_meteor.png"):
            for i in range(3):
                self._player.take_damage()
            self.play_damage_sfx()

        # Icy meteors freeze player and deal single damage
        elif texture == Assets.game_assets.get_asset_texture("icy_meteor.png"):
            self._player.freeze_player()
            self._player.take_damage()

        # Normal meteors deal double damage
        else:
            for i in range(2):
                self._player.take_damage()
            self.play_damage_sfx()

    def check_player_death(self):
        """
        End the game if player runs out of oxygen or dies from
        getting hit by asteroids. Reset the game if necessary
        """
        if self._player._oxygen_meter.get_current_oxygen_level() == 0 or self._player._current_health == 0:
            self.reset_game()

    def create_asteroid_hitbox(self, asteroid):
        """
        Creates a rectangular collision box for an asteroid.
        Returns the pyray.Rectangle object used for the hitbox.
        """
        asteroid_hitbox = pyray.Rectangle(
            asteroid.get_position().x - asteroid._sprite_texture.width / 2,
            asteroid.get_position().y - asteroid._sprite_texture.width / 2,
            asteroid.get_size().x,
            asteroid.get_size().y,
        )
        return asteroid_hitbox

    def create_player_hitbox(self):
        """
        Creates a rectangular collision box for an player.
        Returns the pyray.Rectangle object used for the hitbox.
        """
        player_hitbox = pyray.Rectangle(
            self._player.get_position().x, self._player.get_position().y, self._player.get_size().x, self._player.get_size().y
        )
        return player_hitbox

    def get_player_triangle_data(self, player):
        """
        Returns the vertices of the triangular Sprites.Spaceship as a tuple.
        Tuple is used to track the vertices needed to simulate a triangle collision box.
        """
        player_hitbox = self.create_player_hitbox()
        v1 = pyray.Vector2(player_hitbox.x + player_hitbox.width / 2, player_hitbox.y - 8)
        v2 = pyray.Vector2(player_hitbox.x, player_hitbox.y + player_hitbox.height)
        v3 = pyray.Vector2(player_hitbox.x + player_hitbox.width, player_hitbox.y + player_hitbox.height)
        return (v1, v2, v3)

    def get_asteroid_cicle_data(self, asteroid):
        """
        Returns the center and radius of asteroid as a tuple.
        Tuple is used to track the radius and center
        needed to simulate a circular collision box.
        """
        center = pyray.Vector2(int(asteroid.get_position().x), int(asteroid.get_position().y))
        radius = asteroid.get_size().x / 2
        return (center, radius)

    def check_asteroid_player_collision(self, asteroid):
        """
        Checks if the asteroid collides with the player. Uses A
        circle hitbox detection for the asteroid with any side of the player triangular hitbox sides.
        Hit by regular asteroid: player damage.
        hit by icy asteroid: deal some damage and freeze player for a period of time.
        Hit by firey asteroid: extra player damage.
        For every hit, reset score multiplier for the player and
        remove asteroid from the asteroid list.
        """
        center, radius = self.get_asteroid_cicle_data(asteroid)

        # Vertices for the player hitbox triangle sides
        v1, v2, v3 = self.get_player_triangle_data(self._player)

        # Triangle-circle collision detection for player-asteroid hit
        if (
            pyray.check_collision_circle_line(center, radius, v1, v2)
            or pyray.check_collision_circle_line(center, radius, v1, v3)
            or pyray.check_collision_circle_line(center, radius, v2, v3)
        ):
            self._player.get_player_points().reset_multiplier()
            self.deal_player_damage(asteroid.get_texture())
            self._asteroids_list.remove(asteroid)

    def check_asteroid_laser_collision(self, asteroid):
        """
        Checks if any of the player's lasers collide with the asteroid.
        If so, the laser is destroyed.
        """
        center, radius = self.get_asteroid_cicle_data(asteroid)
        for laser in self._player.get_lasers():
            laser_hitbox = pyray.Rectangle(laser.get_position().x, laser.get_position().y, laser.get_size().x, laser.get_size().y)
            if pyray.check_collision_circle_rec(center, radius, laser_hitbox):
                self._player._laser_projectiles.remove(laser)

    def check_player_powerup_collision(self, powerup):
        """
        Checks if the powerup collides with the player. Uses A
        rectangular hitbox detection for both player and powerup.
        Collected uncased O2 powerup: refuel oxygen
        Collected heart powerup: add one heart to player
        Collected ammo powerup: increase player laser ammo by 1
        """

        # Takes a parameter since powerups vary by size
        power_up_hitbox = self.create_power_up_hitbox(powerup)

        player_hitbox = self.create_player_hitbox()

        if pyray.check_collision_recs(power_up_hitbox, player_hitbox):
            # O2 requires unlocking first (shoot to unlock
            self.increase_player_stats(powerup)

    def check_laser_O2_powerup_collision(self, powerup):
        """
        Checks if any of the player's lasers collide with the cased O2 Powerup.
        If so, the laser is destroyed and the O2 Powerup is unlocked for the player
        to collect the oxygen.
        """
        # Create player hitboxes for collision detection
        power_up_hitbox = self.create_power_up_hitbox(powerup)
        for laser in self._player.get_lasers():
            laser_hitbox = pyray.Rectangle(laser.get_position().x, laser.get_position().y, laser.get_size().x, laser.get_size().y)

            if (
                isinstance(powerup, Sprites.O2_PowerUP)
                and powerup.get_lock_status() == True
                and pyray.check_collision_recs(power_up_hitbox, laser_hitbox)
            ):
                explosion = Assets.game_assets.get_asset_sound("explosion.ogg")
                pyray.set_sound_volume(explosion, 0.1)
                pyray.play_sound(explosion)
                # So that player can now collect oxygen bubble
                powerup.change_lock_status(False)
                self._player._laser_projectiles.remove(laser)

    def asteroid_collision_check(self):
        """
        Handles collision detection between asteroids, player, and lasers.
        Uses circle-triangle collision for more accurate hit detection.
        Different asteroid types cause different effects on player on collision:
        - Fiery: Higher damage (3 hearts)
        - Icy: Freezes player temporarily + moderate damage
        - Normal: Standard damage (2 hearts)
        If asteroids collide with the lasers, delete the laser, NOT the asteroid.
        """

        for asteroid in self._asteroids_list:
            self.check_asteroid_player_collision(asteroid)
            self.check_asteroid_laser_collision(asteroid)

    def powerup_collision_check(self):
        """
        Manages collisions between player and power-ups, and laser interactions
        with locked O2 power-ups. Each power-up has unique collection mechanics:
        - O2: Must be unlocked by shooting first
        - Ammo: Direct collection
        - Health: Direct collection
        This causes the player to have to make strategic decisions around oxygen management.
        """

        for powerup in self._power_ups:
            self.check_player_powerup_collision(powerup)
            self.check_laser_O2_powerup_collision(powerup)

    def treasure_collision_check(self):
        """
        Handles player-treasure collisions. When player
        collides with treasure, they add the treasures point value to
        their school. Different treasures have different point values, with rarer items worth more points.
        All treasures increase the score multiplier equally.
        """
        treasure_points = {
            Assets.game_assets.get_asset_texture("iron.png"): 50,
            Assets.game_assets.get_asset_texture("diamond.png"): 200,
            Assets.game_assets.get_asset_texture("emerald.png"): 100,
            Assets.game_assets.get_asset_texture("ruby.png"): 75,
        }
        for treasure in self._treasure[:]:
            treasure_hitbox = self.create_treasure_hitbox(treasure)
            player_hitbox = self.create_player_hitbox()

            if pyray.check_collision_recs(treasure_hitbox, player_hitbox):
                self.increase_player_points(treasure, treasure_points)

    def increase_player_stats(self, powerup):
        """
        Depending on the type of powerup upon collect, either
        increase ammo, health, or oxygen, award points and increase score multiplier.
        Remove powerup from the powerup list.
        """
        if isinstance(powerup, Sprites.O2_PowerUP) and powerup.get_lock_status() == False:
            self._player.get_oxygen_meter().increase_oxygen()
            self.collect_item(powerup, "bubble.ogg")
            self._player.get_player_points().increase_points(50)
            self._player.get_player_points().increase_multiplier(0.1)

        # Ammo and health can be collected directly
        elif isinstance(powerup, Sprites.Ammo_PowerUP):
            self._player.increase_ammo()
            self.collect_item(powerup, "ammo_collect.ogg")
            self._player.get_player_points().increase_points(50)
            self._player.get_player_points().increase_multiplier(0.1)

        elif isinstance(powerup, Sprites.HeartCapsule_PowerUP):
            self._player.increase_health()
            self.collect_item(powerup, "heart_collect.ogg")
            self._player.get_player_points().increase_points(50)
            self._player.get_player_points().increase_multiplier(0.1)

    def create_power_up_hitbox(self, powerup):
        """
        Creates a rectangular collision box for an powerup.
        Returns the pyray.Rectangle object used for the powerup.
        """
        power_up_hitbox = pyray.Rectangle(powerup.get_position().x, powerup.get_position().y, powerup.get_size().x, powerup.get_size().y)
        return power_up_hitbox

    def create_treasure_hitbox(self, treasure):
        """
        Creates and returns a hitbox (pyray.Rectangle) for a given treasure object.
        """
        treasure_hitbox = pyray.Rectangle(
            treasure.get_position().x, treasure.get_position().y, treasure.get_size().x, treasure.get_size().y
        )
        return treasure_hitbox

    def increase_player_points(self, treasure, treasure_points):
        """
        Handles the actions when a treasure is collected, plays the collection sound.
        removes the treasure, and increases the player's points and player's score multiplier.
        """
        self._play_treasure_collect_sfx()
        self._treasure.remove(treasure)
        treasure_texture = treasure.get_texture()
        self._player.get_player_points().increase_points(treasure_points[treasure_texture])
        self._player.get_player_points().increase_multiplier(0.1)

    def initialize_collision_checks(self):
        """Runs all collision detection systems each frame."""
        self.asteroid_collision_check()
        self.powerup_collision_check()
        self.treasure_collision_check()

    def spawn_obstacles_collectibles(self):
        """Manages the spawning of all game elements."""
        self.initiate_asteroid_spawning_mechanics()
        self.draw_asteroids()
        self.draw_power_ups()
        self.draw_treasure()
        self.draw_outer_space()

    def initialize_game(self):
        """Main game loop content - updates all game elements each frame."""
        self.spawn_obstacles_collectibles()
        self._player.initialize_player_mechanics()
        self._game_clock.run_clock()
        self.initialize_collision_checks()
        self.start_music()
        pyray.update_music_stream(self._game_music)

    def should_exit_menu_status(self):
        """Checks if user has clicked exit button."""
        return self._menu._exit_clicked

    def change_game_difficulty(self, city):
        """
        Weather API integration that modifies game difficulty based on
        real-world weather data. Temperature affects asteroid types,
        while wind speed affects asteroid movement speed.

        Falls back to defaults if city data cannot be retrieved.
        """
        city_data = WeatherApi.get_city_temp_wspd(city)
        if "temperature" in city_data and "windspeed" in city_data:

            # Scale wind speed to appropriate game speed range
            wind_speed_range = [city_data["windspeed"] * 100 + 1, city_data["windspeed"] * 100 + 50]
            self._city_custom = city
            self._game_temperature_custom = city_data["temperature"]
            self._max_speed_range_custom = wind_speed_range
            # Store a list with the same data, but don't let them reference each other
            self._max_speed_range_default = wind_speed_range[:]


        else:
            # Fallback to defaults if API call fails
            self._city_custom = self._city_default
            self._game_temperature_custom = self._game_temperature_default
            self._max_speed_range_custom = self._max_speed_range_default[:]

    def run_optimized(self):
        """
        Main game loop that handles menu navigation, game state transitions,
        and drawing appropriate buttons based on game state.
        Uses DoublyLinkedStack data structure for better efficiency.

        """

        # Initialize with the main menu state
        self._menu._menu_state_stack.push("main_menu")

        while not pyray.window_should_close() and not self.should_exit_menu_status():
            pyray.begin_drawing()
            pyray.clear_background((0,0,0,0))

            # This current_state is used to determine what new menu to now run
            current_state = self._menu._menu_state_stack.top()

            # Menu screen to run based on current game state
            if current_state in self._screens:
                self._screens[current_state]()
            else:
                print(current_state + " not recognized.")

            pyray.end_drawing()

        # store the games data to be saved (city data, player leaderboard)
        saved_data = {"Game Leaderboard": self._menu._leaderboard, "City selected": self._city_custom, "City temperature": self._game_temperature_custom, 
                    "City wind speed range": self._max_speed_range_custom}

        GameSaver.save_game_data_file(saved_data)

        # Close the game
        self.cleanup_asteroids_game()

    def handle_main_menu(self):
        """
        Handles the main menu logic, including drawing the menu and resetting the input box.
        """
        self._menu.run_menu()
        self._user_input_box.reset_input_box()

    def handle_death_menu(self):
        """
        Handles the death menu logic, drawing the death screen.
        """
        self._menu.run_death_menu()

    def handle_leaderboard_menu(self):
        """
        Handles the leaderboard menu logic, drawing the leaderboard.
        """
        self._menu.run_leaderboard_menu()

    def handle_options_menu(self):
        """
        Handles the options menu, including drawing difficulty information and handling user input for difficulty and whether to erase data.
        """
        self._menu.run_options_menu()
        self._menu.draw_difficulty_information(
            self._city_custom, str(self._game_temperature_custom), str(self._max_speed_range_custom) 
        )

        if self._menu._difficulty_clicked:
            # Only display the input box if the difficulty button hasn't been clicked
            self._user_input_box.enable_input_box()
            if self._user_input_box._enter_is_pressed:
                city_typed = self._user_input_box._text_to_save
                self.change_game_difficulty(city_typed)
                self._user_input_box.reset_input_box()

        # Erase save data upon button click
        if self._menu._erase_file_clicked:
            # Reset games leaderboard, and city data displays in-game as well
            self._game_temperature_custom = 65
            self._max_speed_range_custom = [200, 250]
            self._max_speed_range_default = [200, 250]
            self._city_custom = "Default"
            self._menu._leaderboard = []
            self._menu._erase_file_clicked = False

    def handle_start_game(self):
        """
        Initializes the game, checks player death, and manages the start of the game.
        """
        self.initialize_game()
        self.check_player_death()

    def handle_loading_screen(self):
        """
        Displays loading screen while game resources initialize.
        Repeatedly updates start_timer in the mean time.
        """
        loading_texture = Assets.game_assets.get_asset_texture("loading_screen.png")
        loading_texture_source = pyray.Rectangle(0, 0, loading_texture.width, loading_texture.height)
        loading_texture_dest = pyray.Rectangle(0, 0, Settings.ADJUSTED_WIDTH, Settings.ADJUSTED_HEIGHT)
        pyray.draw_texture_pro(loading_texture, loading_texture_source, loading_texture_dest, pyray.Vector2(), 0, raylib.WHITE)
        self._menu._start_timer.update()

    def cleanup_asteroids_game(self):
        """
        Performs cleanup when the game loop ends:
        unload assets and close the window.
        """
        Assets.game_assets.unload()
        pyray.close_audio_device()
        pyray.close_window()


if __name__ == "__main__":
    game_test = SpaceGame()
    game_test.run_optimized()
