from operator import mul
from functools import reduce

def zeros(ns):
    return len([n for n in ns if n == 0])


def nonzero(ns):
    return [n for n in ns if not n == 0]


def prod(ns):
    return reduce(
        mul,
        nonzero(ns),
        1
    )


def find_product(ns):
    if (n := len(ns)) == 0:
        return ns
    if (nz := zeros(ns)) > 1:
        return [0] * n
    p = prod(ns)
    if nz == 1:
        return [(p if v == 0 else 0) for v in ns]
    return [p // v for v in ns]