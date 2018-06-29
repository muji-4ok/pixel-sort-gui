from collections import deque

from sortingpaths import *

from sortingfuncs import *


def sort(im, func=None, path=None, reverse=False, mirror=False, angle=0,
         max_intervals=0, randomize=False, progress=0):
    width, height = im.size  # for eval
    path_gen = paths[path][0]
    path_args = paths[path][1:]
    path = apply_intervals(eval(f"{path_gen}({','.join(path_args)})"),
                           max_intervals, randomize, progress)
    func = eval(func)

    return _sort(im, func, path, reverse, mirror)


def _sort(im, func, path, reverse=False, mirror=False):
    pixels = matrix(list(im.getdata()), im.size)
    new_pixels = new_matrix(im.size)

    def func_map(ij):
        i, j = ij

        return func(pixels[i][j])

    for coords in path:
        reverse = not reverse if mirror else reverse
        new_coords = sorted(coords, key=func_map, reverse=reverse)

        if mirror:
            coords_deque = deque()

            for i, coord in enumerate(new_coords):
                if i % 2:
                    coords_deque.append(coord)
                else:
                    coords_deque.appendleft(coord)

            new_coords = list(coords_deque)

        for (i, j), (ni, nj) in zip(coords, new_coords):
            new_pixels[i][j] = pixels[ni][nj]

    im.putdata(flatten(new_pixels))

    return im
