from collections.abc import Sequence
from typing import Union


def euclidean(a: Union[float, int], b):
    while b:
        a, b = b, a % b
    return a


def split(a: Sequence, n: int):
    list_split = []
    for i in range(0, len(a), n):
        list_split.append(a[i:i + n])
    return list_split, len(list_split[-1])
