import toml, os


class ThemeLoader:
    """
    Loads themes for biscuit from json files.
    """
    def __init__(self, master, theme_name, default="default"):
        self.base = master.base

        self.theme_name = theme_name
        self.default = default
        self.theme_data = self.try_load_theme()

    def try_load_theme(self):
        try:
            return self.load_theme()
        except Exception:
            return self.load_theme(self.default)

    def load_theme(self, theme_name):
        with open(os.path.join(self.base.configdir, f'{theme_name}.toml'), 'r') as theme_file:
            theme_data = toml.load(theme_file)
        return theme_data
    
    def get_loaded_theme(self):
        return self.theme_data
