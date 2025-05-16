import json
import os

class ConfigManager:
    CONFIG_FILE = "config.json"

    @staticmethod
    def save_config(data):
        with open(ConfigManager.CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_config():
        if os.path.exists(ConfigManager.CONFIG_FILE):
            with open(ConfigManager.CONFIG_FILE, "r") as f:
                return json.load(f)
        return None
