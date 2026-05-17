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
        d.name for d in LOCALES_PATH.iterdir() if d.is_dir() and not d.name.startswith("_") and not d.name.startswith(".")
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

class sstr(str):
    def __new__(cls, obj):
        return super(sstr, cls).__new__(cls, obj)
    def __init__(self, obj):
        self.object = obj
    def __add__(self, value):
        if isinstance(value, str):
            return sstr(str(self) + value)
        return sstr(super().__add__(value))
    def __radd__(self, value):
        if isinstance(value, str):
            return sstr(value + str(self))
        return sstr(super(sstr, value).__add__(self.object))
    def __mod__(self, value):
        if isinstance(value, dict) and "br" in value.keys():
            br_flag = str(value["br"]).startswith("<")
            processed_tpl = self
            if br_flag:
                processed_tpl = re.sub(r"%\(br=(.*?)\)s", r"\1", processed_tpl)
                processed_tpl = re.sub(r"%\(!br=(.*?)\)s", "", processed_tpl)
            else:
                processed_tpl = re.sub(r"%\(br=(.*?)\)s", "", processed_tpl)
                processed_tpl = re.sub(r"%\(!br=(.*?)\)s", r"\1", processed_tpl)
            return str.__mod__(processed_tpl, value)
        else:
            return super().__mod__(value)

def get_data(p, color=True):
    try:
        if p.startswith("br=") or p.startswith("!br="):
            return sstr(f"%({p})s")
        return getattr(Color, p.upper()) if color else ""
    except:
        return ""

def get_translation(lang, word, color=True):
    if LOCALES_CACHE.get(lang, {}) or load_locales(lang):
        tr = LOCALES_CACHE[lang].get(word, None)
    else:
        return
    if tr == None:
        return "word"
    flag = False
    if not isinstance(tr, list) and not isinstance(tr, tuple):
        tr = [tr]
        flag = True
    for idx, x in enumerate(tr):
        parts = re.split(r"<(.*?)>", x)
        result = "".join(get_data(p, color) if i % 2 else p for i, p in enumerate(parts))
        tr[idx] = sstr(result)
    if flag:
        tr = tr[0]
    return tr

def translate(word, color=True):
    a = get_translation(get_config()["lang"], word, color)
    if a == "word":
        print(word)
        return word
    return a

_ = translate