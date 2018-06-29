import tkinter as tk
from tkinter import ttk


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
