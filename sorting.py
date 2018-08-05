import os
from subprocess import call
from uuid import uuid4

from PIL import Image


def sort(im, func=None, path=None, reverse=False, mirror=False, angle=0,
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
    call(["PixelSorter.exe", in_filename, out_filename, path, func,
          max_intervals, randomize, angle, merge, reverse, mirror])
    opened_im = Image.open(out_filename)
    out_im = opened_im.copy()
    del opened_im
    os.remove(in_filename)
    os.remove(out_filename)

    return out_im
