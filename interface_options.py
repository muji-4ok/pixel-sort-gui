import tkinter as tk

from sorting import *
from sortingfuncs import funcs


def options_toplevel(master, func='lightness', path='rows', reverse=False,
                     mirror=False, angle=0, max_intervals=0,
                     randomize=False, progress=0):
    # Main holders creation ----------------
    root = tk.Toplevel()
    main = tk.Frame(root)
    main.grid(row=0, column=0, sticky='news')

    # Toplevel config ----------------
    root.title('Pixel sorting options')
    root.resizable(False, False)
    root.transient(master)
    root.iconbitmap("app_icon.ico")

    # Options ----------------

    #
    #
    # General ----------------
    general_f = tk.LabelFrame(root)
    general_f['text'] = 'General'
    general_f.grid(row=0, column=0, sticky='news')

    func_v = tk.StringVar()
    func_v.set(func)
    func_menu = tk.OptionMenu(general_f, func_v, *funcs)
    func_menu['width'] = len(max(funcs, key=len))
    func_menu.grid(row=0, column=0, sticky='ew')

    reverse_v = tk.BooleanVar()
    reverse_v.set(reverse)
    reverse_check = tk.Checkbutton(general_f, text='Reverse',
                                   variable=reverse_v)
    reverse_check.grid(row=1, column=0, sticky='ew')

    mirror_v = tk.BooleanVar()
    mirror_v.set(mirror)
    mirror_check = tk.Checkbutton(general_f, text='Mirror', variable=mirror_v)
    mirror_check.grid(row=2, column=0, sticky='ew')
    # General ----------------
    #
    #

    #
    #
    # Path ----------------
    path_f = tk.LabelFrame(root)
    path_f['text'] = 'Path'
    path_f.grid(row=0, column=1, sticky='news')

    path_v = tk.StringVar()
    path_v.set(path)
    path_menu = tk.OptionMenu(path_f, path_v, *paths_keys)
    path_menu['width'] = len(max(paths_keys, key=len))
    path_menu.grid(row=0, column=0, sticky='ew')

    angle_v = tk.IntVar()
    angle_v.set(angle)
    angle_scale = tk.Scale(path_f)
    angle_scale['from_'] = -180
    angle_scale['to'] = 180
    angle_scale['orient'] = 'horizontal'
    angle_scale['length'] = 180
    angle_scale['tickinterval'] = 60
    angle_scale['label'] = 'Angle'
    angle_scale['variable'] = angle_v
    angle_scale.grid(row=1, column=0, sticky='ew')

    interval_v = tk.IntVar()
    interval_v.set(max_intervals)
    interval_scale = tk.Scale(path_f)
    interval_scale['from_'] = 0
    interval_scale['to'] = 1000
    interval_scale['orient'] = 'horizontal'
    interval_scale['length'] = 180
    interval_scale['label'] = 'Interval'
    interval_scale['variable'] = interval_v
    interval_scale.grid(row=2, column=0, sticky='ew')

    randomize_v = tk.BooleanVar()
    randomize_v.set(randomize)
    randomize_check = tk.Checkbutton(path_f, text='Randomize',
                                     variable=randomize_v)
    randomize_check.grid(row=3, column=0, sticky='ew')

    progress_v = tk.DoubleVar()
    progress_v.set(progress)
    progress_scale = tk.Scale(path_f)
    progress_scale['from_'] = 0
    progress_scale['to'] = 1
    progress_scale['resolution'] = 0.01
    progress_scale['orient'] = 'horizontal'
    progress_scale['length'] = 180
    progress_scale['label'] = 'Progress'
    progress_scale['variable'] = progress_v
    progress_scale.grid(row=4, column=0, sticky='ew')
    # Path ----------------
    #
    #

    # Center window ----------------
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    root.geometry(f'{w}x{h}+{(ws - w) // 2}+{(hs - h) // 2 - 100}')

    def get_options():
        params = {'func': func_v.get(),
                  'path': path_v.get(),
                  'reverse': reverse_v.get(),
                  'mirror': mirror_v.get(),
                  'angle': angle_v.get(),
                  'max_intervals': interval_v.get(),
                  'randomize': randomize_v.get(),
                  'progress': progress_v.get()}

        return params

    root.get_options = get_options

    return root


default_options = {'func': 'lightness',
                   'path': 'rows',
                   'reverse': False,
                   'mirror': False,
                   'angle': 0,
                   'max_intervals': 0,
                   'randomize': False,
                   'progress': 0}
