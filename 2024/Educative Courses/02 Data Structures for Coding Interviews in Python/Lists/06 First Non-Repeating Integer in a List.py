from functools import reduce
from collections import defaultdict


def nmap(ns):
    def fold(acc, ni):
        return acc[ni[1]].append(ni[0]) or acc

    return reduce(fold, enumerate(ns), defaultdict(list))


def unique(nmap):
    return {n: si[0] for n, si in nmap.items() if len(si) == 1}


def first(unmap):
    return min(unmap.items(), key=lambda x: x[1])[0]


def find_first_unique(ns):
    return first(unique(nmap(ns)))