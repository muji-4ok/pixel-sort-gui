import ctypes

from PIL import Image

PATH_TO_DLL = "PixelSorterVCDLL.dll"
DLL = ctypes.WinDLL(PATH_TO_DLL)
DLL.sortImage.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p,
                          ctypes.c_char_p, ctypes.c_int, ctypes.c_bool,
                          ctypes.c_int, ctypes.c_bool, ctypes.c_bool,
                          ctypes.c_bool, ctypes.c_bool, ctypes.c_int]
DLL.sortImage.restype = ctypes.POINTER(ctypes.c_char)


def sort(im, path=None, reverse=False, mirror=False, angle=0, to_interval=False,
         max_intervals=0, randomize=False, merge=False, low_threshold=0):
    im = im.convert("RGBA")
    im_bytes = im.tobytes()
    im_bytes_p = ctypes.c_char_p(im_bytes)

    data_ptr = DLL.sortImage(im.width, im.height, im_bytes_p,
                             bytes(path, "UTF-8"),
                             max_intervals, randomize, angle, merge, reverse,
                             mirror, to_interval, low_threshold)

    out_data = ctypes.string_at(data_ptr, im.width * im.height * 4)
    im_out = Image.frombytes("RGB", im.size, out_data, "raw", "RGBX", 0, 1)

    return im_out
