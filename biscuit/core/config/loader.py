import toml
import os


class ConfigLoader:
    """
    Loads configurations for biscuit from json file.
    """
    def __init__(self, master, config_file="settings.toml"):
        self.base = master.base

        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        with open(os.path.join(self.base.configdir, self.config_file), 'r') as settingsfile:
            config = toml.load(settingsfile)
        return config

    def get_config(self):
        return self.config
