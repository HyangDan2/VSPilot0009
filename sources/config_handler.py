
import os
import json
from datetime import datetime

CONFIG_DIR = "config"
DEFAULT_FILE = os.path.join(CONFIG_DIR, "params.json")

def save_params_to_json(params):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(DEFAULT_FILE, 'w') as f:
        json.dump(params, f, indent=4)

def load_params_from_json():
    if not os.path.exists(DEFAULT_FILE):
        return None
    with open(DEFAULT_FILE, 'r') as f:
        return json.load(f)

def save_named_config(params):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(CONFIG_DIR, f"config_{timestamp}.json")
    with open(path, 'w') as f:
        json.dump(params, f, indent=4)

def list_all_saved_configs():
    if not os.path.exists(CONFIG_DIR):
        return []
    return [f for f in os.listdir(CONFIG_DIR) if f.endswith(".json")]

def load_config_by_name(name):
    path = os.path.join(CONFIG_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        return json.load(f)
