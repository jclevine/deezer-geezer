from random import sample


def writelines(filepath, lines):
    with open(filepath, 'w') as f:
        f.writelines(lines)


def uniq_randomize_list(a_list):
    return sample(list(set(a_list)), len(list(set(a_list))))
