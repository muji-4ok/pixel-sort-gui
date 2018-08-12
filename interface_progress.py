import tkinter as tk
from tkinter import ttk


class Progress(tk.Frame):
    def __init__(self, master, title, message):
        super().__init__(master)
        self.grid(row=0, column=0, sticky='news')

        # Toplevel config ----------------
        master.protocol("WM_DELETE_WINDOW", lambda: 1)
        master.title(title)
        master.resizable(False, False)
        master.iconbitmap("app_icon.ico")

        # Label ----------------
        self.label = tk.Label(master)
        self.label['text'] = message
        self.label['font'] = ('Times', 15)
        self.label.grid(row=0, column=0)

        # Progress ----------------
        self.progress = ttk.Progressbar(master)
        self.progress['mode'] = 'indeterminate'
        self.progress['length'] = 200
        self.progress.grid(row=1, column=0)

        # Center window ----------------
        master.update_idletasks()
        w = master.winfo_width()
        h = master.winfo_height()
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        master.geometry(f'{w}x{h}+{(ws - w) // 2}+{(hs - h) // 2 - 100}')
        self.progress.start(10)
