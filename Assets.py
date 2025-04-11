from pyray import init_window, init_audio_device, load_texture, load_font, load_music_stream, load_sound, Texture2D, Font, Sound, Music, unload_texture, unload_font,  unload_sound, unload_music_stream
import Settings
import os


class Assets:
    def __init__(self):
        """
        Initializes the window, audio device, and asset dictionary.
        This method sets up the game window and the audio system to ensure rendering and sound work correctly.
        """

        # Init_window is needed for any imported texture to be drawn
        # Init_audio_device is needed for any imported audio to be used
        init_window(Settings.ADJUSTED_WIDTH, Settings.ADJUSTED_HEIGHT, "GAME")
        init_audio_device()
        self._assets = {}

    def get_asset_texture(self, key):
        """
        Loads and returns a texture. Only loads once to save memory.
        """
        if key in self._assets:
            return self._assets[key]
        else:
            # Load the texture if it's not already loaded
            # Note: all abspath does is get rid of .. (which stands for relative path)
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "images/" + key))
            self._assets[key] = load_texture(base_path)
            return self._assets[key]

    def get_asset_font(self, key):
        """
        Loads and returns a font. Only loads once to save memory.
        """
        if key in self._assets:
            return self._assets[key]
        else:
            # Load the font if it's not already loaded
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "font/" + key))
            self._assets[key] = load_font(base_path)
            return self._assets[key]

    def get_asset_sound(self, key):
        """
        Loads and returns a sound. Only loads once to save memory.
        """
        if key in self._assets:
            return self._assets[key]
        else:
            # Load the sound if it's not already loaded
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "audio/" + key))
            self._assets[key] = load_sound(base_path)
            return self._assets[key]

    def get_asset_music(self, key):
        """
        Loads and returns music. Only loads once to save memory.
        """
        if key in self._assets:
            return self._assets[key]
        else:
            # Load the music if it's not already loaded
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "audio/" + key))
            self._assets[key] = load_music_stream(base_path)
            return self._assets[key]

    def unload(self):
        """
        Unloads all assets to free up memory.
        """
        for texture in self._assets:
            if type(texture) == Texture2D:
                unload_texture(texture)
            elif type(texture) == Font:
                unload_font(texture)
            elif type(texture) == Sound:
                unload_sound(texture)
            elif type(texture) == Music:
                unload_music_stream(texture)
        self._assets.clear()  # clear the asset dictionary


# create an instance of the Assets class to manage assets
game_assets = Assets()
