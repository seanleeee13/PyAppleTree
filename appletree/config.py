lazy from .locales import get_default_lang, validate_lang
lazy from pathlib import Path
lazy import json

CONFIG_DIR = Path.home() / ".appletree"
CONFIG_FILE = CONFIG_DIR / "config.json"
CONFIG_CACHE = {}

def get_default_setting():
    return {"lang": get_default_lang()}

def validate_setting(key, value):
    if key == "lang":
        return validate_lang(value)
    else:
        return False

def validate_settings(config):
    for k in config.keys():
        if not validate_setting(k, config[k]):
            return False
    return True

def init_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        save_config(**get_default_setting(), cov=True)

def get_config():
    global CONFIG_CACHE
    if not CONFIG_CACHE or not validate_settings(CONFIG_CACHE):
        init_config()
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                CONFIG_CACHE = json.load(f)
        except (json.JSONDecodeError, OSError):
            CONFIG_CACHE = get_default_setting()
    if not validate_settings(CONFIG_CACHE):
        default = get_default_setting()
        for k in default:
            if CONFIG_CACHE.get(k, "ERR") == "ERR" or not validate_setting(k, CONFIG_CACHE[k]):
                CONFIG_CACHE[k] = default[k]
        for k in set(CONFIG_CACHE.keys()) - set(default.keys()):
            del CONFIG_CACHE[k]
        save_config(**CONFIG_CACHE)
    return CONFIG_CACHE

def save_config(cov=False, **config):
    if not cov:
        new_config = get_config()
    else:
        new_config = {}
    for key in config.keys():
        if validate_setting(key, config[key]):
            new_config[key] = config[key]
            CONFIG_CACHE.update({key: config[key]})
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(new_config, f, indent=4)