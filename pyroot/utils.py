lazy import traceback
lazy import tempfile
lazy import atexit
lazy import os

class PyRootError(Exception):
    def __init__(self, code, message, err_message, um):
        self.code = code
        self.message = message
        self.error_message = err_message
        self.version = "1.0.0"
        self.user_mistake = um

def tempfile_wrapper(func, *args, index=0, binary=True):
    with tempfile.NamedTemporaryFile("wb+" if binary else "w+", delete_on_close=False, delete=False) as f:
        name = f.name
    args = list(args)
    args.insert(index, name)
    atexit.register(lambda: clean(name))
    try:
        return func(*args)
    except PyRootError:
        clean(name)
        raise
    except:
        clean(name)
        raise PyRootError(
            code=f"analyze/utils#tempfile_wrapper<{func.__name__}>.1", message="Error in tempfile_wrapper",
            err_message=traceback.format_exc(), um=False
        )

def clean(name):
    try:
        if os.path.exists(name):
            os.remove(name)
    except:
        pass