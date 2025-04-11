from Settings import SCALE_FACTOR, ADJUSTED_HEIGHT, ADJUSTED_WIDTH
from DoublyLinkedStack import DoublyLinkedStack
from Assets import game_assets
from MyTimer import Timer
from pyray import Vector2, Rectangle, get_mouse_position, draw_text_ex, check_collision_point_rec, is_mouse_button_pressed, draw_text_pro, draw_rectangle_lines_ex, measure_text_ex, draw_rectangle_pro, play_sound, set_sound_volume
from GameSaver import load_gamesave_file
from raylib import MOUSE_BUTTON_LEFT, GRAY, LIGHTGRAY, WHITE, BLACK, YELLOW, RED

class Menu:
    """
    Menu class that handles the user interface, button interactions,
    and transitions between different menu states (main menu, options, leaderboard, etc.).
    """

    def __init__(self):
        self._buttons = {}
        self._difficulty_clicked = False
        self._erase_file_clicked = False
        self._exit_clicked = False

        # Load the saved leaderboard data
        self._leaderboard = load_gamesave_file()["Game Leaderboard"]
        self._title = "untitled asteroids game"
        self.create_buttons()
        self._start_timer = Timer(1.5, False, False, self.start_game_after_delay)
        self._menu_state_stack = DoublyLinkedStack()

        # Game screen button events tied to each menu state
        self._menu_event_handlings = {
            "main_menu": self.main_menu_buttons_handling,
            "death_menu": self.death_menu_buttons_handling,
            "leaderboard": self.leaderboard_buttons_handling,
            "options": self.options_buttons_handling,
        }

    def score_sort(self, entry):
        """
        Sort helper function used to sort leaderboard entries by score.
        Takes in entry, a tuple containing player data (name, score, time).
        Returns int, The score of the player.
        """
        return entry[1]

    def sort_leaderboard(self):
        """
        Sort the leaderboard by score in descending order.
        """
        self._leaderboard.sort(key=self.score_sort, reverse=True)

    def draw_leaderboard_stats(self):
        """
        Draws the leaderboard stats (player name, score, and time) on the screen.
        It sorts the leaderboard before displaying it.
        """
        if len(self._leaderboard) > 0:
            self.sort_leaderboard()
        text_height = 120 * SCALE_FACTOR
        place = 1
        for player_data in self._leaderboard:
            player_data = player_data[0] + "    score: " + str(player_data[1]) + "    time: " + str(player_data[2])
            text_dimensions = measure_text_ex(game_assets.get_asset_font("slkscreb.ttf"), player_data, 40 * SCALE_FACTOR, 0)
            centered_txt_width = (ADJUSTED_WIDTH - text_dimensions.x) * SCALE_FACTOR  / 2
            draw_text_ex(
                game_assets.get_asset_font("slkscreb.ttf"),
                str(place) + ". " + player_data,
                Vector2(centered_txt_width, text_height),
                40 * SCALE_FACTOR,
                0,
                YELLOW,
            )
            text_height += 60 * SCALE_FACTOR
            place += 1

    def start_game_after_delay(self):
        """
        This function is called after a timer delay to push menu_screen then start_game.

        This is so that loading screen can be the game state for a while, (so handle_loading_screen in Game.py can be called).
        And so that menu_screen is always the bottom of the stack as it should be
        """
        self._menu_state_stack.pop()
        self._menu_state_stack.push("start_game")

    def create_buttons(self):
        """
        Creates all buttons for the menu with their positions, sizes, and text.
        """
        self._buttons["start"] = Button(
            Vector2(ADJUSTED_WIDTH / 2 - 310, 450), 550 * SCALE_FACTOR, 80 * SCALE_FACTOR, "START", game_assets.get_asset_font("slkscreb.ttf"), 40 * SCALE_FACTOR
        )
        self._buttons["stats"] = Button(
            Vector2(ADJUSTED_WIDTH / 2 - 310, 550), 550 * SCALE_FACTOR, 80 * SCALE_FACTOR, "LEADERBOARD", game_assets.get_asset_font("slkscreb.ttf"), 40 * SCALE_FACTOR
        )
        self._buttons["exit"] = Button(
            Vector2(ADJUSTED_WIDTH / 2 - 310, 650), 550 * SCALE_FACTOR, 80 * SCALE_FACTOR, "EXIT", game_assets.get_asset_font("slkscreb.ttf"), 40 * SCALE_FACTOR
        )
        self._buttons["main menu"] = Button(
            Vector2(ADJUSTED_WIDTH / 2 - 310, 550), 550 * SCALE_FACTOR, 80 * SCALE_FACTOR, "MAIN MENU", game_assets.get_asset_font("slkscreb.ttf"), 40 * SCALE_FACTOR
        )
        self._buttons["options"] = Button(
            Vector2(ADJUSTED_WIDTH / 2 - 310, 750), 550 * SCALE_FACTOR, 80 * SCALE_FACTOR, "OPTIONS", game_assets.get_asset_font("slkscreb.ttf"), 40 * SCALE_FACTOR
        )
        self._buttons["difficulty"] = Button(
            Vector2(ADJUSTED_WIDTH / 2 - 310, 750), 550 * SCALE_FACTOR, 80 * SCALE_FACTOR, "DIFFICULTY", game_assets.get_asset_font("slkscreb.ttf"), 40 * SCALE_FACTOR
        )
        self._buttons["erase file"] = Button(
            Vector2(ADJUSTED_WIDTH / 2 - 310, 750), 200 * SCALE_FACTOR, 50 * SCALE_FACTOR, "ERASE SAVE", game_assets.get_asset_font("slkscreb.ttf"), 20 * SCALE_FACTOR
        )

    def draw_title(self):
        """
        Draws the title of the game in the center of the screen.
        """
        title_text_dimensions = measure_text_ex(game_assets.get_asset_font("slkscreb.ttf"), self._title, 50 * SCALE_FACTOR, 0)
        centered_title_width = (ADJUSTED_WIDTH - title_text_dimensions.x) * SCALE_FACTOR / 2 
        draw_text_ex(game_assets.get_asset_font("slkscreb.ttf"), self._title, Vector2(centered_title_width, 120 * SCALE_FACTOR), 50 * SCALE_FACTOR, 0, WHITE)

    def draw_difficulty_information(self, city, temp, speed):
        """
        Displays difficulty settings (city, temperature, and speed range) in the options menu.
        city (str): The name of the selected city.
        temp (str): The temperature in Fahrenheit.
        speed (str): The speed range selected.
        """
        draw_text_ex(
            game_assets.get_asset_font("slkscreb.ttf"),
            "City: " + city,
            Vector2(self._buttons["difficulty"].get_button_position().x * SCALE_FACTOR - 20, 340 * SCALE_FACTOR),
            35 * SCALE_FACTOR,
            0,
            WHITE,
        )

        draw_text_ex(
            game_assets.get_asset_font("slkscreb.ttf"),
            "Temperature: " + temp + " F",
            Vector2(self._buttons["difficulty"].get_button_position().x * SCALE_FACTOR - 20, 440 * SCALE_FACTOR),
            35 * SCALE_FACTOR,
            0,
            WHITE,
        )
        draw_text_ex(
            game_assets.get_asset_font("slkscreb.ttf"),
            "Speed range: " + speed,
            Vector2(self._buttons["difficulty"].get_button_position().x * SCALE_FACTOR - 20, 540 * SCALE_FACTOR),
            35 * SCALE_FACTOR,
            0,
            WHITE,
        )

    def play_button_click_sfx(self):
        """
        Plays a sound effect when a button is clicked.
        """
        button_click = game_assets.get_asset_sound("button_click.ogg")
        set_sound_volume(button_click, 0.4)
        play_sound(button_click)

    def check_button_clicks_optimized(self):
        """
        Checks for mouse button clicks and handles the logic for each menu state.
        Changes states based on button clicks (start, stats, options, exit, etc.).
        Uses DoublylinkedList.
        """

        # call handling method based on the current_state
        current_state = self._menu_state_stack.top()
        self._menu_event_handlings[current_state]()

    def main_menu_buttons_handling(self):
        """Check clicks for buttons on main menu."""
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(
            get_mouse_position(), self._buttons["start"].get_rectangle()
        ):
            # Pop but dont push start game screen yet, until timer has finished, then push menu and start to recalibrate
            self._menu_state_stack.push("loading_screen")
            self.play_button_click_sfx()
            self._start_timer.activate()
        elif is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(
            get_mouse_position(), self._buttons["stats"].get_rectangle()
        ):
            self._menu_state_stack.push("leaderboard")
            self.play_button_click_sfx()
        elif is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(
            get_mouse_position(), self._buttons["options"].get_rectangle()
        ):
            self._menu_state_stack.push("options")
            self.play_button_click_sfx()
        elif is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(
            get_mouse_position(), self._buttons["exit"].get_rectangle()
        ):
            self._exit_clicked = True

    def options_buttons_handling(self):
        """Check clicks for buttons on options menu."""
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(
            get_mouse_position(), self._buttons["main menu"].get_rectangle()
        ):
            self._menu_state_stack.pop()  # Go back to the main menu
            self._menu_state_stack.push("main_menu")
            self._difficulty_clicked = False
            self._erase_file_clicked = False
            self.play_button_click_sfx()

        elif is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(
            get_mouse_position(), self._buttons["difficulty"].get_rectangle()
        ):
            if self._difficulty_clicked != True:
                self._difficulty_clicked = True
                self.play_button_click_sfx()
            else:
                self._difficulty_clicked = False
                self.play_button_click_sfx()

        elif is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(
            get_mouse_position(), self._buttons["erase file"].get_rectangle()
        ):
            if self._erase_file_clicked != True:
                self._erase_file_clicked = True
                self.play_button_click_sfx()

    def leaderboard_buttons_handling(self):
        """Check clicks for buttons on leaderboard menu."""
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(
            get_mouse_position(), self._buttons["main menu"].get_rectangle()
        ):
            self._menu_state_stack.pop()
            self._menu_state_stack.push("main_menu")
            self.play_button_click_sfx()

    def death_menu_buttons_handling(self):
        """Check clicks for buttons on death menu."""
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(
            get_mouse_position(), self._buttons["main menu"].get_rectangle()
        ):
            self._menu_state_stack.pop()  # go to main menu
            self.play_button_click_sfx()
        elif is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(
            get_mouse_position(), self._buttons["exit"].get_rectangle()
        ):
            self._exit_clicked = True

    def run_menu(self):
        """
        Runs the main menu by drawing buttons and handling button click checks.
        """

        self._buttons["start"].draw_button(RED, BLACK, Vector2(ADJUSTED_WIDTH / 2 - 240 * SCALE_FACTOR, 250 * SCALE_FACTOR))
        self._buttons["stats"].draw_button(RED, BLACK, Vector2(ADJUSTED_WIDTH / 2 - 240 * SCALE_FACTOR, 350 * SCALE_FACTOR))
        self._buttons["options"].draw_button(RED, BLACK, Vector2(ADJUSTED_WIDTH / 2 - 240 * SCALE_FACTOR, 450 * SCALE_FACTOR))
        self._buttons["exit"].draw_button(RED, BLACK, Vector2(ADJUSTED_WIDTH / 2 - 240 * SCALE_FACTOR, 550 * SCALE_FACTOR))
        self.draw_title()
        # self.check_button_clicks()
        self.check_button_clicks_optimized()

    def run_leaderboard_menu(self):
        """
        Runs the leaderboard menu by drawing the 'main menu' button and displaying leaderboard stats.
        """
        self._buttons["main menu"].draw_button(RED, BLACK, Vector2(ADJUSTED_WIDTH / 2 - 280 * SCALE_FACTOR, 650 * SCALE_FACTOR))
        # self.check_button_clicks()
        self.check_button_clicks_optimized()
        self.draw_leaderboard_stats()

    def run_death_menu(self):
        """
        Runs the death menu, drawing 'main menu' and 'exit' buttons, and displaying 'GAME OVER' text.
        """
        self._buttons["main menu"].draw_button(RED, BLACK, Vector2(ADJUSTED_WIDTH / 2 - 635, 450 * SCALE_FACTOR))
        self._buttons["exit"].draw_button(RED, BLACK, Vector2(ADJUSTED_WIDTH / 2 + 40, 450 * SCALE_FACTOR))
        # self.check_button_clicks()
        self.check_button_clicks_optimized()
        title_text_dimensions = measure_text_ex(game_assets.get_asset_font("slkscreb.ttf"), "GAME OVER", 100 * SCALE_FACTOR, 0)
        
        centered_title_width = (ADJUSTED_WIDTH - title_text_dimensions.x) * SCALE_FACTOR/ 2 
        centered_title_height = (ADJUSTED_HEIGHT - title_text_dimensions.y) * SCALE_FACTOR / 2 
        draw_text_ex(
            game_assets.get_asset_font("slkscreb.ttf"),
            "GAME OVER",
            Vector2(centered_title_width *  SCALE_FACTOR - 57, int(centered_title_height / 1.5) * SCALE_FACTOR),
            100 * SCALE_FACTOR,
            0,
            WHITE,
        )

    def run_options_menu(self):
        """
        This function runs the options menu by drawing buttons and checking for button clicks.
        It allows the player to go back to the main menu or access difficulty settings.
        """
        self._buttons["main menu"].draw_button(RED, BLACK, Vector2(ADJUSTED_WIDTH / 2 - 280 * SCALE_FACTOR, 650 * SCALE_FACTOR))
        self._buttons["difficulty"].draw_button(RED, BLACK, Vector2(ADJUSTED_WIDTH / 2 - 280 * SCALE_FACTOR, 150 * SCALE_FACTOR))
        self._buttons["erase file"].draw_button(RED, BLACK, Vector2(ADJUSTED_WIDTH - 300, 650 * SCALE_FACTOR))
        # self.check_button_clicks()
        self.check_button_clicks_optimized()


class Button:
    """
    Every button is a stylized rectangle object with text that can be clicked and interacted with.
    It includes features like hover effects, repositioning, and drawing to the screen.
    """

    def __init__(self, pos, width, height, text, font, font_size):
        self._pos = pos
        self._text = text
        self._font = font
        self._font_size = font_size
        self._width = width
        self._height = height
        # Create a rectangle representing the button's area, used for hover detection and drawing
        self._rectangle = Rectangle(self._pos.x, self._pos.y, self._width, self._height)
        self._hovered_yet = False

    def get_button_position(self):
        """
        Returns the current position of the button.
        """
        return self._pos

    def reposition_button(self, pos):
        """
        Repositions the button to a new position (Vector2).
        Updates the button's rectangle to reflect the new position.
        """
        self._pos = pos
        self._rectangle = Rectangle(self._pos.x, self._pos.y, self._width, self._height)

    def is_hovered(self):
        """
        Checks if the mouse cursor is hovering over the button.
        Returns True if the mouse cursor is inside the button's rectangle, otherwise False.
        """
        mouse_pos = get_mouse_position()
        in_rectangle_width = self._pos.x <= mouse_pos.x <= self._pos.x + self._width 
        in_rectangle_height = self._pos.y <= mouse_pos.y <= self._pos.y + self._height 
        return in_rectangle_width and in_rectangle_height

    def draw_button(self, color1, color2, pos):
        """
        Draws the button, including hover effects. Changes color on hover.
        """
        # Update the button position
        self.reposition_button(pos)

        # Set the button colors based on hover status
        box_color, text_color = self._get_button_colors(color1, color2)

        # Draw the button's background
        self._draw_button_background(box_color)

        # Measure text and draw the button text
        self._draw_button_text(text_color)

        # Draw the button's border
        self._draw_button_border()

    def _get_button_colors(self, color1, color2):
        """
        Determines the button colors based on the hover state.
        """
        # Default button colors
        box_color, text_color = color1, color2

        # If the button is hovered, change the colors
        if self.is_hovered():
            box_color, text_color = GRAY, LIGHTGRAY
            if not self._hovered_yet:
                self._play_hover_sound()
                self._hovered_yet = True
        else:
            self._hovered_yet = False

        return box_color, text_color

    def _play_hover_sound(self):
        """
        Plays the hover sound when the mouse enters the button.
        """
        button_click = game_assets.get_asset_sound("button_hover.ogg")
        set_sound_volume(button_click, 0.4)
        play_sound(button_click)

    def _draw_button_background(self, box_color):
        """
        Draws the button background with the specified color.
        """
        draw_rectangle_pro(self._rectangle, Vector2(0, 0), 0, box_color)

    def _draw_button_text(self, text_color):
        """
        Draws the button's text centered within the button.
        """
        text_dimensions = measure_text_ex(self._font, self._text, self._font_size, 0.0)
        text_width, text_height = text_dimensions.x, text_dimensions.y
        draw_text_pro(
            self._font,
            self._text,
            Vector2(
                self._pos.x + self._rectangle.width / 2 - text_width / 2, self._pos.y + self._rectangle.height / 2 - text_height / 2
            ),
            Vector2(0, 0),
            0,
            self._font_size,
            0.0,
            text_color,
        )

    def _draw_button_border(self):
        """
        Draws the border of the button.
        """
        draw_rectangle_lines_ex(self._rectangle, 2.0 * SCALE_FACTOR, WHITE)

    def get_rectangle(self):
        """
        Returns the button's rectangle for collision detection (e.g., for clicks).
        """
        return self._rectangle