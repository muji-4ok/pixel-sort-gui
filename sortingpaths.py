from PIL import ImageFilter


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


paths = ['columns', 'rows', 'angled', 'rectangles', 'edges rows',
         'edges columns', 'edges angled']
