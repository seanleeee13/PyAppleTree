lazy import json
lazy import os

CONFIG_PATH = os.path.expanduser("~/.code_tester_config.json")

def get_config():
    if not os.path.exists(CONFIG_PATH):
        return {"lang": "en"}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def set_lang(lang):
    config = get_config()
    config["lang"] = lang
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)