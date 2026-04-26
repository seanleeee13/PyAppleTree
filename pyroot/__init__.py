lazy from .__main__ import main, json
lazy from .utils import PyRootVersion

def help():
    print(f"PyRoot Version {PyRootVersion}")
    print("Usage: python -m pyroot [options] [file name]")

__all__ = [
    "help",
    "main",
    "json"
]