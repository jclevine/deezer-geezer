from random import sample


def writelines(filepath, lines):  # pragma: no cover
    with open(filepath, 'w') as f:
        f.writelines(lines)


def uniq_randomize_list(a_list):  # pragma: no cover
    return sample(list(set(a_list)), len(list(set(a_list))))
