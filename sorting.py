import os
import subprocess
from uuid import uuid4

from PIL import Image


def sort(im, path=None, reverse=False, mirror=False, angle=0, to_interval=False,
         max_intervals=0, randomize=False, merge=False):
    in_filename = str(uuid4()) + ".png"
    out_filename = str(uuid4()) + ".png"
    im.save(in_filename)
    max_intervals = str(max_intervals)
    randomize = str(int(randomize))
    angle = str(angle)
    mirror = str(int(mirror))
    merge = str(int(merge))
    reverse = str(int(reverse))
    to_interval = str(int(to_interval))
    subprocess.call(["PixelSorterCpp.exe", in_filename, out_filename, path,
                     max_intervals, randomize, angle, merge, reverse, mirror,
                     to_interval])
    opened_im = Image.open(out_filename)
    out_im = opened_im.copy()
    del opened_im
    os.remove(in_filename)
    os.remove(out_filename)

    return out_im
