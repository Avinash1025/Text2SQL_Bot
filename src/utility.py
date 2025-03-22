import yaml
import os

def load_config():
    with open(f"{os.getcwd()}/config/config.yml") as file:
        config = yaml.safe_load(file)
    return config

