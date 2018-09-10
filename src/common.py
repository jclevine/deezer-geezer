from random import sample
from itertools import chain


def writelines(filepath, lines):  # pragma: no cover
    with open(filepath, 'w') as f:
        f.writelines(lines)


def uniq_randomize_list(a_list):  # pragma: no cover
    return sample(list(set(a_list)), len(list(set(a_list))))


def flatten(a_list):
    return list(chain.from_iterable(a_list))
