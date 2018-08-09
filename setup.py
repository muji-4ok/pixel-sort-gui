import os
import sys

from cx_Freeze import setup, Executable


# Change this
python_root = r'C:\Users\Arseny\AppData\Local\Programs\Python\Python36'
dll_path = r'path\to\dll'

# Fix bugs
include_files = [
    python_root + r'\DLLs\tk86t.dll',
    python_root + r'\DLLs\tcl86t.dll',
    r'app_icon.ico',
    dll_path
]
os.environ['TCL_LIBRARY'] = python_root + r'\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = python_root + r'\tcl\tk8.6'

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = dict(packages=[], excludes=[], include_files=include_files)

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('pixelsorter.py', base=base)
]

setup(name='pixelsorter',
      version='1.0',
      options=dict(build_exe=build_options),
      executables=executables)
