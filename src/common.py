from random import sample
from itertools import chain


def writelines(filepath, lines):  # pragma: no cover
    with open(filepath, 'w') as f:
        f.writelines('\n'.join(lines))


def readlines(filepath):  # pragma: no cover
    with open(filepath, 'r') as f:
        return f.readlines()


def uniq_randomize_list(a_list):  # pragma: no cover
    return sample(list(set(a_list)), len(list(set(a_list))))


def flatten(a_list):
    return list(chain.from_iterable(a_list))


def chunk_list(a_list, chunk_size):
    return [a_list[i:i + chunk_size] for i in range(0, len(a_list), chunk_size)]
