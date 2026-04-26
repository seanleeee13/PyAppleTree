lazy from pathlib import Path
# lazy import json

CONFIG_DIR = Path.home() / ".appletree"
CONFIG_FILE = CONFIG_DIR / "config.json"

# def init_config():
#     CONFIG_DIR.mkdir(parents=True, exist_ok=True)
#     if not CONFIG_FILE.exists():
#         save_config({"lang": "ko"})

# def get_config():
#     init_config()
#     try:
#         with open(CONFIG_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except (json.JSONDecodeError, OSError):
#         return {"lang": "ko"}

# def save_config(config):
#     with open(CONFIG_FILE, "w", encoding="utf-8") as f:
#         json.dump(config, f, indent=4)

import locale

def get_default_lang():
    """OS 설정에 따라 기본 언어(ko/en) 결정"""
    try:
        # 'ko_KR', 'en_US' 같은 값을 가져옵니다.
        default_locale = locale.getdefaultlocale()[0] 
        if default_locale and default_locale.startswith('ko'):
            return "ko"
    except:
        pass
    return "en" # 한국어가 아니면 무조건 글로벌 표준인 영어로!

def init_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        # 여기서 하드코딩 'ko' 대신 감지된 기본값을 넣습니다.
        save_config({"lang": get_default_lang(), "theme": "dark"})
