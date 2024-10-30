from collections import defaultdict
from functools import reduce

class NMap:
    def __init__(self, ns):
        self.ns = ns
        self.nmap = reduce(
            lambda acc, ni: acc[ni[1]].append(ni[0]) or acc,
            enumerate(ns), defaultdict(list)
        )

    def get(self, k):
        return None if not k in self.nmap else self.ns[self.nmap[k][0]]

    def ln(self, k):
        return 0 if not self.get(k) else len(self.nmap[k])

    def gets(self, k, l):
        if self.get(k) is None or \
           self.get(l) is None or \
           (k == l and self.ln(k) < 2):
            return []
        return [self.get(k), self.get(l)]


def find_sum(ns, k):
    nmap = NMap(ns)
    for n in ns:
        if tsum := nmap.gets(n, k - n): return tsum
    return []

if __name__ == '__main__':
    ns, k = [2, 4, 6, 8, 10, 19], 21
    print(find_sum(ns, k))