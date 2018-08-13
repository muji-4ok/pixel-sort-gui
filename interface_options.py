import tkinter as tk
from util import *


class Options(tk.Frame):
    paths = ['columns', 'rows', 'angled', 'rectangles', 'edges rows']
    funcs = ['lightness', 'hue', 'saturation', 'value']
    default_options = {'path': 'rows',
                       'reverse': False,
                       'mirror': False,
                       'angle': 0,
                       'max_intervals': 0,
                       'randomize': False,
                       'merge': False,
                       'to_interval': False,
                       'low_threshold': 0,
                       'func': 'lightness'}

    def __init__(self, master, options_d):
        super().__init__(master)
        self.grid(row=0, column=0, sticky='news')

        # Toplevel config ----------------
        master.title('Pixel sorting options')
        master.resizable(False, False)
        master.iconbitmap("app_icon.ico")

        # Options ----------------

        #
        #
        # General ----------------
        self.general_f = tk.LabelFrame(master)
        self.general_f['text'] = 'General'
        self.general_f.grid(row=0, column=0, sticky='news')

        self.func_v = tk.StringVar(value=options_d['func'])
        self.func_menu = tk.OptionMenu(self.general_f, self.func_v, *self.funcs)
        self.func_menu['width'] = len(max(self.funcs, key=len))
        self.func_menu.grid(row=0, column=0, sticky='ew')

        self.reverse_v = tk.BooleanVar(value=options_d['reverse'])
        self.reverse_check = tk.Checkbutton(self.general_f, text='Reverse',
                                            variable=self.reverse_v)
        self.reverse_check.grid(row=1, column=0, sticky='ew')

        self.mirror_v = tk.BooleanVar(value=options_d['mirror'])
        self.mirror_check = tk.Checkbutton(self.general_f, text='Mirror',
                                           variable=self.mirror_v)
        self.mirror_check.grid(row=2, column=0, sticky='ew')

        self.merge_v = tk.BooleanVar(value=options_d['merge'])
        self.merge_check = tk.Checkbutton(self.general_f, text='Merge',
                                          variable=self.merge_v)
        self.merge_check.grid(row=3, column=0, sticky='ew')

        self.to_interval_v = tk.BooleanVar(value=options_d['to_interval'])
        self.to_interval_check = tk.Checkbutton(self.general_f,
                                                text='Do intervals',
                                                variable=self.to_interval_v,
                                                command=self.to_interval_click)
        self.to_interval_check.grid(row=4, column=0, sticky='ew')
        # General ----------------
        #
        #

        #
        #
        # Path ----------------
        self.path_f = tk.LabelFrame(master)
        self.path_f['text'] = 'Path'
        self.path_f.grid(row=0, column=1, sticky='news')

        self.path_v = tk.StringVar(value=options_d['path'])
        self.path_v.trace_add('write', self.path_menu_click)
        self.path_menu = tk.OptionMenu(self.path_f, self.path_v, *self.paths)
        self.path_menu['width'] = len(max(self.paths, key=len))
        self.path_menu.grid(row=0, column=0, sticky='ew')

        self.interval_v = tk.IntVar(value=options_d['max_intervals'])
        self.interval_scale = tk.Scale(self.path_f)
        self.interval_scale['from_'] = 0
        self.interval_scale['to'] = 1000
        self.interval_scale['orient'] = 'horizontal'
        self.interval_scale['length'] = 180
        self.interval_scale['label'] = 'Interval'
        self.interval_scale['variable'] = self.interval_v
        self.interval_scale.grid(row=3, column=0, sticky='ew')

        self.randomize_v = tk.BooleanVar(value=options_d['randomize'])
        self.randomize_check = tk.Checkbutton(self.path_f, text='Randomize',
                                              variable=self.randomize_v)
        self.randomize_check.grid(row=4, column=0, sticky='ew')
        # Path ----------------
        #
        #

        #
        #
        # Additional ----------------
        self.additional_f = tk.LabelFrame(master)
        self.additional_f['text'] = 'Additional'
        self.additional_f.grid(row=0, column=2, sticky='news')

        self.angle_v = tk.IntVar(value=options_d['angle'])
        self.angle_scale = tk.Scale(self.additional_f)
        self.angle_scale['from_'] = -180
        self.angle_scale['to'] = 180
        self.angle_scale['orient'] = 'horizontal'
        self.angle_scale['length'] = 180
        self.angle_scale['tickinterval'] = 60
        self.angle_scale['label'] = 'Angle'
        self.angle_scale['variable'] = self.angle_v
        self.angle_scale.grid(row=0, column=0, sticky='ew')

        self.low_threshold_v = tk.IntVar(value=options_d['low_threshold'])
        self.low_threshold_scale = tk.Scale(self.additional_f)
        self.low_threshold_scale['from_'] = 0
        self.low_threshold_scale['to'] = 200
        self.low_threshold_scale['orient'] = 'horizontal'
        self.low_threshold_scale['length'] = 180
        self.low_threshold_scale['tickinterval'] = 50
        self.low_threshold_scale['label'] = 'Low threshold'
        self.low_threshold_scale['variable'] = self.low_threshold_v
        self.low_threshold_scale.grid(row=1, column=0, sticky='ew')
        # Additional ----------------
        #
        #

        # Center window ----------------
        master.update_idletasks()
        w = master.winfo_width()
        h = master.winfo_height()
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        master.geometry(f'{w}x{h}+{(ws - w) // 2}+{(hs - h) // 2 - 100}')

        # Trigger gray out logic
        self.to_interval_click()
        self.path_menu_click()

    def path_menu_click(self, v1=None, v2=None, v3=None):  # Needed for trace
        try:
            self.path_menu
        except AttributeError:
            return

        self.angle_scale['state'] = 'disabled'
        self.angle_scale['foreground'] = rgb(155, 109, 133)
        self.low_threshold_scale['state'] = 'disabled'
        self.low_threshold_scale['foreground'] = rgb(155, 109, 133)

        state = self.path_v.get()

        if state == 'angled':
            self.angle_scale['state'] = 'normal'
            self.angle_scale['foreground'] = rgb(5, 5, 10)
        elif state == 'edges rows':
            self.low_threshold_scale['state'] = 'normal'
            self.low_threshold_scale['foreground'] = rgb(5, 5, 10)

    def to_interval_click(self):
        state = self.to_interval_v.get()

        if state:
            self.interval_scale['state'] = 'normal'
            self.interval_scale['foreground'] = rgb(5, 5, 10)
            self.randomize_check['state'] = 'normal'
        else:
            self.interval_scale['state'] = 'disabled'
            self.interval_scale['foreground'] = rgb(155, 109, 133)
            self.randomize_check['state'] = 'disabled'

    def get_options(self):
        params = {'path': self.path_v.get(),
                  'reverse': self.reverse_v.get(),
                  'mirror': self.mirror_v.get(),
                  'angle': self.angle_v.get(),
                  'max_intervals': self.interval_v.get(),
                  'randomize': self.randomize_v.get(),
                  'merge': self.merge_v.get(),
                  'to_interval': self.to_interval_v.get(),
                  'low_threshold': self.low_threshold_v.get(),
                  'func': self.func_v.get()}

        return params
