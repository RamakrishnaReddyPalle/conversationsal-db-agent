import yaml
import os

class Settings:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.mongo_uri = os.getenv('MONGO_URI')
        self.mongo_db = os.getenv('DATABASE_NAME')

settings = Settings() 