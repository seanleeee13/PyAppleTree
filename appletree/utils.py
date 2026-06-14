lazy import traceback
lazy import tempfile
lazy import atexit
lazy import os

AppleTreeVersion = "1.0.0a0.dev7"

class AppleTreeError(Exception):
    def __init__(self, code, message, err_message, um):
        self.code = code
        self.message = message
        self.error_message = err_message
        self.user_mistake = um
        super().__init__(self.message)

class AppleTreeEnum:
    ORANGE = "\033[38;5;208m"
    GRAY = "\033[90m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"
    VERSION = "1.0.0a0.dev3"

def tempfile_wrapper(func, *args, index=0, binary=True):
    with tempfile.NamedTemporaryFile("wb+" if binary else "w+", delete_on_close=False, delete=False) as f:
        name = f.name
    args = list(args)
    args.insert(index, name)
    atexit.register(lambda: clean(name))
    try:
        return func(*args)
    except KeyboardInterrupt:
        raise
    except AppleTreeError:
        clean(name)
        raise
    except Exception as e:
        clean(name)
        raise AppleTreeError(
            code=f"analyze/utils#tempfile_wrapper<{func.__name__}>.1", message="Error in tempfile_wrapper",
            err_message=traceback.format_exc(), um=False
        ) from e

def clean(name):
    try:
        if os.path.exists(name):
            os.remove(name)
    except:
        pass

class None_open:
    def __enter__(self):
        pass
    def __exit__(self, *args):
        pass
    def __bool__(self):
        return False

def safe_open(filename, mode):
    if not filename or not os.path.exists(filename):
        return None_open()
    else:
        return open(filename, mode=mode)