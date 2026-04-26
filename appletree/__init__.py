lazy from .__main__ import main, json
lazy from .utils import AppleTreeVersion

def help():
    print(f"PyAppleTree Version {AppleTreeVersion}")
    print("Usage: python -m appletree [options] [file name]")

__all__ = [
    "help",
    "main",
    "json"
]