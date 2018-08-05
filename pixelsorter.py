import os.path
import tkinter as tk
from multiprocessing.pool import ThreadPool
from tkinter import filedialog, messagebox

from PIL import ImageTk, Image

from interface_options import Options
from interface_progress import Progress
from sorting import sort

# Constants ----------------
FILETYPES = [('All', '*.*'), ('JPG', '*.jpg'), ('PNG', '*.png')]


# Functions ----------------
def rgb(*args):
    return '#{0:02x}{1:02x}{2:02x}'.format(*args)


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill='both', expand=True)

        # Variables ----------------
        self.filename_v = tk.StringVar()
        self.filename_v.set('None')
        self.filename = ''
        self.options = Options.default_options
        self.im_id = None
        self.resize_id = None
        self.im = None
        self.source = None
        self.im_tk = None
        self.last_width = 0
        self.last_height = 0
        self.pool = ThreadPool(processes=1)

        # Menu bar ----------------
        self.menubar = tk.Menu(self.master)
        self.master['menu'] = self.menubar
        self.menu_file = tk.Menu(self.menubar, tearoff=0)
        self.menu_file.add_command(label='Open', command=self.file_open)
        self.menu_file.add_command(label='Reset', command=self.file_reset)
        self.menu_file.add_command(label='Save', command=self.file_save)
        self.menu_file.add_command(label='Save as', command=self.file_save_as)
        self.menubar.add_cascade(label='File', menu=self.menu_file)

        # Canvas ----------------
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky='news')

        # Other ----------------
        self.frame_other = tk.Frame(self)
        self.frame_other.grid(row=1, column=0, sticky='news')

        self.filename_label = tk.Label(self.frame_other)
        self.filename_label['textvariable'] = self.filename_v
        self.filename_label['font'] = ('Fixedsys', 18)
        self.filename_label['justify'] = 'left'
        self.filename_label['anchor'] = 'w'
        self.filename_label['fg'] = rgb(0, 204, 0)
        self.filename_label.grid(row=0, column=0, columnspan=3, sticky='news')

        self.sort_button = tk.Button(self.frame_other)
        self.sort_button['text'] = 'Sort'
        self.sort_button['bg'] = rgb(255, 150, 150)
        self.sort_button['font'] = ('Times', 15)
        self.sort_button['command'] = self.file_sort
        self.sort_button.grid(row=1, column=0)

        self.options_button = tk.Button(self.frame_other)
        self.options_button['text'] = 'Options'
        self.options_button['bg'] = rgb(150, 255, 150)
        self.options_button['font'] = ('Times', 15)
        self.options_button['command'] = self.open_options
        self.options_button.grid(row=1, column=1)

        # Events ----------------
        self.canvas.bind('<Configure>', self.queue_resize)

        # Resizing grid ----------------
        self.rowconfigure(0, weight=10)
        self.columnconfigure(0, weight=1)

        for j in range(2):
            self.frame_other.columnconfigure(j, weight=1)

    def queue_resize(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        new_width = event.width
        new_height = event.height

        if width == new_width and height == new_height:
            return

        if (abs(width - self.last_width) > 30 or
                abs(height - self.last_height) > 30):
            self.clear_canvas()

        self.filename_label['wraplength'] = self.canvas.winfo_width()

        if self.resize_id is not None:
            self.master.after_cancel(self.resize_id)

        self.resize_id = self.master.after(300, self.resize)

    def resize(self):
        self.last_width = self.winfo_width()
        self.last_height = self.winfo_height()
        self.resize_id = None
        self.update_canvas()

    def open_options(self):
        options_toplevel = tk.Toplevel()
        options_toplevel.transient(self.master)
        options_frame = Options(options_toplevel, self.options)

        options_toplevel.grab_set()
        self.master.wait_window(options_toplevel)
        options_toplevel.grab_release()

        self.options.clear()
        self.options.update(options_frame.get_options(), )

    def close_progress(self):
        self.progress_toplevel.destroy()

    def clear_canvas(self):
        if self.im_id is not None:
            self.canvas.delete(self.im_id)
            self.im_id = None

    def update_canvas(self):
        if not self.im:
            return

        width, height = self.im.size
        width_canv = self.canvas.winfo_width()
        height_canv = self.canvas.winfo_height()

        # if width > width_canv or height > height_canv:
        maxw = min(width, width_canv)
        maxh = min(height, height_canv)
        ratio = min(maxw / width, maxh / height)

        self.im_tk = ImageTk.PhotoImage(
            self.im.resize((round(width * ratio), round(height * ratio)),
                           Image.ANTIALIAS))

        self.clear_canvas()
        self.im_id = self.canvas.create_image(width_canv // 2, height_canv // 2,
                                              image=self.im_tk)

    def file_reset(self, event=None):
        if not self.im:
            return

        self.im = self.source
        self.im_tk = None
        self.update_canvas()

    def file_open(self, event=None):
        new_filename = filedialog.askopenfilename(filetypes=FILETYPES,
                                                  title='Open image')

        if not new_filename:
            return

        try:
            self.source = Image.open(new_filename).convert('RGB')
            self.im = self.source
            self.im_tk = None
            self.filename = ''
            self.filename_v.set('None')
            self.update_canvas()
        except OSError:
            msg = f'Cannot open {new_filename}'
            messagebox.showwarning('File error', msg)

    def file_save(self, event=None):
        if self.filename:
            self.im.save(self.filename)
        else:
            self.file_save_as()

    def file_save_as(self, event=None):
        if not self.im:
            return

        new_filename = filedialog.asksaveasfilename(filetypes=FILETYPES,
                                                    defaultextension='.jpg',
                                                    title='Save image')

        if not new_filename:
            return

        try:
            self.im.save(new_filename)
            self.filename = new_filename
            self.filename_v.set(os.path.split(new_filename)[1])
        except ValueError:
            msg = f'Cannot save {new_filename}'
            messagebox.showwarning('File error', msg)

    def file_sort(self, event=None):
        if not self.source:
            return

        self.progress_toplevel = tk.Toplevel()
        self.progress_toplevel.transient(self.master)
        self.progress_toplevel.progress_frame = Progress(self.progress_toplevel)

        self.progress_toplevel.grab_set()

        self.result = self.pool.apply_async(sort, args=(self.source.copy(),),
                                            kwds=self.options)

        self.progress_toplevel.after(100, self.check_result)
        self.master.wait_window(self.progress_toplevel)
        self.progress_toplevel.grab_release()

    def check_result(self):
        if self.result.ready():
            im_sorted = self.result.get()
            self.im = im_sorted
            self.close_progress()
            self.update_canvas()
        else:
            self.progress_toplevel.after(100, self.check_result)


# Toplevel config ----------------
root = tk.Tk()
root.title('Pixel sorter')
root.iconbitmap("app_icon.ico")
root.minsize(640, 480)
app = App(root)

root.mainloop()
