from pyroot.analyze import _analyze

filename = "test/a.py"
input_file = "test/a.txt"
detailed = False

print(_analyze(filename, input_file, detailed))