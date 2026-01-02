import yaml
import os

def load_config(config_path: str = None) -> dict:
    if config_path is None:
        # Get the directory of the current file (utils/) and go up one level to root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "config", "config.yaml")
        
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config