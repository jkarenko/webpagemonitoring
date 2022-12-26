import toml


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        with open("config.toml", "r") as f:
            self.config = toml.load(f)

    def get_config(self):
        return self.config
