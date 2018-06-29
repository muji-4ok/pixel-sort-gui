# Helper functions
def new_matrix(size):
    width, height = size
    matrix = []

    while len(matrix) < height:
        matrix.append([None] * width)

    return matrix


def matrix(seq, size):
    width, height = size
    matrix = []
    start = 0

    while len(matrix) < height:
        matrix.append(seq[start:start + width])
        start += width

    return matrix


def flatten(matrix):
    seq = []

    for line in matrix:
        seq += line

    return seq
