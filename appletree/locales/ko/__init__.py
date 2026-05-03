lazy from . import analyze
lazy from . import main

translate_data = {}
translate_data.update(analyze.translate_data)
translate_data.update(main.translate_data)