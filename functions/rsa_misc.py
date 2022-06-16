

def euclidean(a, b):
    while b:
        a, b = b, a % b
    return a


def split(a, n):
    list_split = []
    for i in range(0, len(a), n):
        list_split.append(a[i:i + n])
    return list_split, len(list_split[-1])
