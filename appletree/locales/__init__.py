lazy from ..config import get_config
lazy from ..utils import Color
lazy from pathlib import Path
lazy import importlib
lazy import locale
lazy import re

LOCALES_PATH = Path(__file__).parent
LOCALES_CACHE = {}

def get_available_langs():
    return [
        d.name for d in LOCALES_PATH.iterdir() if d.is_dir() and not d.name.startswith('_') and not d.name.startswith(".")
    ]

def get_default_lang():
    try:
        default_locale = locale.getdefaultlocale()[0].split("_")[0]
        if validate_lang(default_locale):
            return default_locale
    except:
        pass
    return "en"

def validate_lang(lang):
    return lang in get_available_langs()

def load_locales(lang):
    global LOCALES_CACHE
    try:
        lfile = importlib.import_module(f".{lang}", package=__package__)
        LOCALES_CACHE[lang] = lfile.translate_data
        return True
    except:
        return False

def get_translation(lang, word, color=True):
    if LOCALES_CACHE.get(lang, {}) or load_locales(lang):
        tr = LOCALES_CACHE[lang].get(word, None)
    else:
        return
    flag = False
    if not isinstance(tr, list) and not isinstance(tr, tuple):
        tr = [tr]
        flag = True
    for idx, x in enumerate(tr):
        parts = re.split(r'<(.*?)>', x)
        try:
            if color:
                result = "".join(getattr(Color, p.upper()) if i % 2 else p for i, p in enumerate(parts))
            else:
                result = "".join(p for i, p in enumerate(parts) if i % 2 == 0)
        except AttributeError:
            result = "".join(p for i, p in enumerate(parts) if i % 2 == 0)
            tr[idx] = result
        except:
            tr[idx] = x
        else:
            tr[idx] = result
    if flag:
        tr = tr[0]
    return tr

def translate(word, color=True):
    return get_translation(get_config()["lang"], word, color) or word

_ = translate