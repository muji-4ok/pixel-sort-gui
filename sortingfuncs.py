# Only sorting functions
import colorsys


def hue(p):
    return colorsys.rgb_to_hls(*map(lambda x: x / 255, p))[0]


def saturation(p):
    return colorsys.rgb_to_hls(*map(lambda x: x / 255, p))[2]


def lightness(p):
    if len(p) > 3:
        p.pop()

    return sum(p)


def luminace(p):
    return min(p) + max(p)


def luma(p):
    r, g, b = p
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def median(p):
    return sorted(p)[1]


def red(p):
    return p[0]


def green(p):
    return p[1]


def blue(p):
    return p[2]


funcs = ['hue', 'saturation', 'lightness', 'luminace', 'luma', 'median', 'red',
         'green', 'blue']
