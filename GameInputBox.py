from pyray import draw_rectangle_v, draw_rectangle_lines_ex, get_mouse_position, get_char_pressed, is_key_pressed, measure_text_ex, draw_text_pro, Rectangle, Vector2
from raylib import KEY_ENTER, KEY_BACKSPACE, GRAY, WHITE



class InputBox:
    """
    A text box that allows user input with various customization options.

    Features:
    - Allows text input when mouse hovers over it.
    - Supports character limit, backspace, and enter functionality.
    - Can be resized, repositioned, and styled.
    - Displays text or a placeholder ("Enter City") when empty.
    - Tracks mouse hover and input events to show visual changes.
    """

    def __init__(self, pos, font, font_size, width, height, character_limit, border_color, interior_color, text_color, placeholder_text):
        self._input_box_pos = pos
        self._character_limit = character_limit
        self._border_color = border_color
        self._interior_color = interior_color
        self._text_color = text_color
        self._mouse_is_hovering = False
        self._is_enabled = False
        self._input_box_text = ""
        self._text_to_save = ""
        self._placeholder_text = placeholder_text
        self._input_box_font = font
        self._input_box_font_size = font_size
        self._input_box_width = width
        self._input_box_height = height
        self._input_box_rectangle = Rectangle(
            self._input_box_pos.x, self._input_box_pos.y, self._input_box_width, self._input_box_height, 
        )
        self._accepted_characters = "0123456789,."
        self._enter_is_pressed = False

    def draw_input_box(self):
        """
        Draw the input box rectangle on the screen with appropriate border and color,
        based on if the mouse is hovering over it or not
        """
        if self.mouse_in_input_box():
            draw_rectangle_v(self._input_box_pos, Vector2(self._input_box_width, self._input_box_height), GRAY)
            draw_rectangle_lines_ex(self._input_box_rectangle, 10, WHITE)
        else:
            draw_rectangle_v(self._input_box_pos, Vector2(self._input_box_width, self._input_box_height), self._interior_color)
            draw_rectangle_lines_ex(self._input_box_rectangle, 10, self._border_color)

    def mouse_in_input_box(self):
        """
        Checks if the mouse is hovering inside the input box.
        """
        mouse_pos = get_mouse_position()
        in_rectangle_width = self._input_box_pos.x <= mouse_pos.x <= self._input_box_pos.x + self._input_box_width
        in_rectangle_height = self._input_box_pos.y <= mouse_pos.y <= self._input_box_pos.y + self._input_box_height
        return in_rectangle_width and in_rectangle_height

    def handle_input(self):
        """
        Handle user input: character typing, backspace, and enter
        """
        if self.mouse_in_input_box():
            self._mouse_is_hovering = True
        else:
            self._mouse_is_hovering = False

        if self._mouse_is_hovering:  # Allow typing if the mouse is hovering
            user_character = chr(get_char_pressed())  # Convert unicode to character
            if user_character in self._accepted_characters and len(self._input_box_text) <= self._character_limit:
                self._input_box_text += user_character
            if is_key_pressed(KEY_BACKSPACE) and len(self._input_box_text) > 0:
                self._input_box_text = self._input_box_text[:-1]
                # reset the input box UI and save text after hitting enter
            if is_key_pressed(KEY_ENTER):
                self._text_to_save = self._input_box_text
                self._enter_is_pressed = True
                if len(self._text_to_save) > 0:  # Ensure text has at least one character
                    self.adjust_saved_text()  # Format the text for saving

    def get_saved_text(self):
        """
        Returns the text that was saved after pressing enter.
        """
        return self._text_to_save

    def adjust_saved_text(self):
        """
        Adjusts the saved text to have only the first character capitalized and the rest in lowercase.
        This is done for standardized input formatting.
        """
        self._text_to_save = self._text_to_save.lower()
        first_character = self._text_to_save[0]

        # Capitalize the first character
        first_character = first_character.upper()
        self._text_to_save = first_character + self._text_to_save[1:]

    def draw_text_input_UI(self):
        """
        Draws the current input text (or placeholder if empty) inside the input box.
        Text is centered inside the box.
        """
        if len(self._input_box_text) == 0:
            display_text = self._placeholder_text  # Placeholder text
        else:
            display_text = self._input_box_text

        # Measure text dimensions for correct centering
        text_dimensions = measure_text_ex(self._input_box_font, display_text, self._input_box_font_size, 0)
        text_width = text_dimensions.x
        text_height = text_dimensions.y

        # Draw the text (either placeholder or input text)
        draw_text_pro(
            self._input_box_font,
            display_text,
            Vector2(
                self._input_box_pos.x + self._input_box_width / 2 - text_width / 2,
                self._input_box_pos.y + self._input_box_height / 2 - text_height / 2,
            ),
            Vector2(0, 0),
            0,
            self._input_box_font_size,
            0.0,
            self._text_color,
        )

    def enable_input_box(self):
        """
        Enables and draws the input box, processes user input, and displays text.
        """
        self.draw_input_box()
        self.handle_input()
        self.draw_text_input_UI()

    def reset_input_box(self):
        """
        Resets the input box text and saved text after the input has been saved.
        """
        self._input_box_text = ""
        self._text_to_save = ""
        self._enter_is_pressed = False


