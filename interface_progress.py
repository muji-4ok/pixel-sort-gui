import tkinter as tk
from tkinter import ttk


class Progress(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky='news')

        # Toplevel config ----------------
        master.protocol("WM_DELETE_WINDOW", lambda: 1)
        master.title('Sorting')
        master.resizable(False, False)
        master.iconbitmap("app_icon.ico")

        # Label ----------------
        self.label = tk.Label(master)
        self.label['text'] = 'Please wait. Sorting in progress...'
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


def progress_toplevel(master):
    # Main holders creation ----------------
    root = tk.Toplevel()
    root.protocol("WM_DELETE_WINDOW", lambda: 1)
    main = tk.Frame(root)
    main.grid(row=0, column=0, sticky='news')

    # Toplevel config ----------------
    root.title('Sorting')
    root.resizable(False, False)
    root.transient(master)
    root.iconbitmap("app_icon.ico")

    # Label ----------------
    label = tk.Label(root)
    label['text'] = 'Please wait. Sorting in progress...'
    label['font'] = ('Times', 15)
    label.grid(row=0, column=0)

    # Progress ----------------
    progress = ttk.Progressbar(root)
    progress['mode'] = 'indeterminate'
    progress['length'] = 200
    progress.grid(row=1, column=0)

    # Center window ----------------
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    root.geometry(f'{w}x{h}+{(ws - w) // 2}+{(hs - h) // 2 - 100}')
    progress.start(10)

    return root
