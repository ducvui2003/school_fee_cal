import os
import json
from src.const import SETTINGS_FILE, SETTINGS_FOLDER, HISTORY_FOLDER, APP_NAME

DEFAULT_SETTINGS = {"output_folder": SETTINGS_FOLDER, "history": HISTORY_FOLDER}


class AppSettings:
    """
    Manage application settings using a JSON file.
    Automatically creates the settings folder if it doesn't exist.
    """

    DEFAULTS = {
        "output_folder": SETTINGS_FOLDER,
        "history": HISTORY_FOLDER,
    }

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.settings_folder = SETTINGS_FOLDER
        os.makedirs(self.settings_folder, exist_ok=True)
        self.settings_file = SETTINGS_FILE
        self._settings = self.DEFAULTS.copy()
        self.load()

    def load(self):
        """Load settings from JSON file. Use defaults if file does not exist."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    self._settings.update(json.load(f))
            except Exception as e:
                print(f"Failed to load settings, using defaults: {e}")

    def save(self):
        """Save current settings to JSON file."""
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def get(self, key: str, default=None):
        """Get a setting value, fallback to default."""
        return self._settings.get(key, default)

    def set(self, key: str, value):
        """Set a setting value."""
        self._settings[key] = value
        self.save()

    def all(self):
        """Return all settings as a dictionary."""
        return self._settings.copy()


app_settings = AppSettings(APP_NAME)
