import collections
import math
import random

from PIL import ImageFilter

from util import *


def apply_angle(f):
    def wrapper(width, height, angle):
        to_flip_y = angle >= 0

        if to_flip_y:
            pass
        else:
            angle = -angle

        to_flip_x = angle > 90

        if to_flip_x:
            times, angle = divmod(angle, 90)
        else:
            times = 0

        to_transpose = angle > 45

        if to_transpose:
            width, height = height, width
            angle = 90 - angle

        result = f(width, height, angle)

        for path in result:
            new_path = []

            for i, j in path:
                if to_flip_y:
                    i = height - 1 - i

                if times % 2:
                    j = width - 1 - j

                if to_transpose:
                    i, j = j, i

                new_path.append((i, j))

            yield new_path

    return wrapper


def apply_intervals(path, max_intervals, randomize=False, progress=0):
    for seq in path:
        if max_intervals < 2:
            yield seq
            continue

        for subseq in intervals(seq, max_intervals, randomize, progress):
            yield subseq


def intervals(seq, max_intervals, randomize=False, progress=0):
    start = 0

    while start < len(seq):
        if randomize:
            size = random.randint(0, round(max_intervals))
        else:
            size = round(max_intervals)

        segment = seq[start:start + size]
        start += size
        max_intervals *= 1 + progress

        if segment:
            yield segment


def rows(width, height):
    for i in range(height):
        seq = []

        for j in range(width):
            seq.append((i, j))

        yield seq


def columns(width, height):
    for j in range(width):
        seq = []

        for i in range(height):
            seq.append((i, j))

        yield seq


def edges_columns(im):
    width, height = im.size
    im_edges = im.filter(ImageFilter.FIND_EDGES).convert('1')
    pixels = matrix(list(im_edges.getdata()), im.size)

    for j in range(width):
        seq = []

        for i in range(height):
            val = pixels[i][j]

            if val == 255:
                yield [(i, j)]

                if len(seq) > 0:
                    yield seq

                seq = []
            else:
                seq.append((i, j))

        if len(seq) > 0:
            yield seq


def edges_rows(im):
    width, height = im.size
    im_edges = im.filter(ImageFilter.FIND_EDGES).convert('1')
    pixels = matrix(list(im_edges.getdata()), im.size)

    for i in range(height):
        seq = []

        for j in range(width):
            val = pixels[i][j]

            if val == 255:
                yield [(i, j)]

                if len(seq) > 0:
                    yield seq

                seq = []
            else:
                seq.append((i, j))

        if len(seq) > 0:
            yield seq


def edges_angled(im, angle):
    width, height = im.size
    im_edges = im.filter(ImageFilter.FIND_EDGES).convert('1')
    pixels = matrix(list(im_edges.getdata()), im.size)

    for coords in angled(width, height, angle):
        seq = []

        for i, j in coords:
            val = pixels[i][j]

            if val == 255:
                yield [(i, j)]

                if len(seq) > 0:
                    yield seq

                seq = []
            else:
                seq.append((i, j))

        if len(seq) > 0:
            yield seq


def rectangles(width, height):
    max_border_dist = min(width // 2, height // 2)

    for border_dist in range(max_border_dist):
        i0 = border_dist
        j0 = border_dist
        i1 = height - border_dist
        j1 = width - border_dist

        seq = []

        for j in range(j0, j1):
            seq.append((i0, j))

        for i in range(i0 + 1, i1):
            seq.append((i, j1 - 1))

        for j in reversed(range(j0, j1 - 1)):
            seq.append((i1 - 1, j))

        for i in reversed(range(i0 + 1, i1 - 1)):
            seq.append((i, j0))

        seq = collections.deque(seq)
        seq.rotate(random.randint(-len(seq), len(seq)))
        seq = list(seq)

        yield seq


def diagonal(width, height):
    for path in angled(width, height, 45):
        yield path


def diagonal_line(width, height):
    seq = []

    for path in angled(width, height, 45):
        seq.extend(path)

    yield seq


@apply_angle
def angled(width, height, angle):
    deltay = round((width - 1) * math.tan(math.radians(angle)))

    def bres_line():
        deltax = width - 1
        err = 0
        deltaerr = deltay
        y = 0

        for x in range(deltax + 1):
            yield y, x
            err += deltaerr

            if 2 * err >= deltax:
                y += 1
                err -= deltax

    line = list(bres_line())

    for di in range(-deltay, height):
        seq = []

        for i, j in line:
            i += di

            if 0 <= i < height:
                seq.append((i, j))
            elif seq:
                break

        yield seq


paths = {'columns': ('columns', 'width', 'height'),
         'rows': ('rows', 'width', 'height'),
         'angled': ('angled', 'width', 'height', 'angle'),
         'diagonal': ('diagonal', 'width', 'height'),
         'diagonal line': ('diagonal_line', 'width', 'height'),
         'rectangles': ('rectangles', 'width', 'height'),
         'edges rows': ('edges_rows', 'im'),
         'edges columns': ('edges_columns', 'im'),
         'edges angled': ('edges_angled', 'im', 'angle')}
paths_keys = list(paths.keys())
