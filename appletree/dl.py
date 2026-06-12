def dl(*data, **kw):
    with open("debug.log", "a", encoding="utf-8") as f:
        print(*data, **kw, file=f)