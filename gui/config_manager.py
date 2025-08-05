import json
import os
from gui.route import resource_path

CONFIG_FILE = resource_path("config.json")

def cargar_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "idioma": "Español",
        "modo": "oscuro",
        "color_base": "verde",
        "atajos": True
    }

def guardar_config(config_data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4, ensure_ascii=False)
