import os
import sys

from cx_Freeze import setup, Executable

# Fix bugs
include_files = [
    r'C:\Users\Arseny\AppData\Local\Programs\Python\Python36\DLLs\tk86t.dll',
    r'C:\Users\Arseny\AppData\Local\Programs\Python\Python36\DLLs\tcl86t.dll',
    r'app_icon.ico',
    r'PixelSorterCpp.exe'
]
os.environ['TCL_LIBRARY'] = r'C:\Users\Arseny\AppData\Local\Programs' \
                            r'\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Arseny\AppData\Local\Programs' \
                           r'\Python\Python36\tcl\tk8.6'

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
