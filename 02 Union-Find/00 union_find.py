"""

The Union-Find Datastructure

"""

class UnionFindN:
    def __init__(self, n):
        self.id = [i for i in range(n)]
        self.sz = [1 for _ in range(n)]
        self.count = n

    def path(self, i):
        p = [i]
        while self.id[i] != i:
            i = self.id[i]
            p.append(i)
        return p

    def compress(self, path):
        root = path[-1]
        for p in path: self.id[p] = root
        return root

    def find(self, i):
        return self.compress(self.path(i))

    def split(self, p, q):
        return (p, q) if self.sz[p] > self.sz[q] else (q, p)

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if p == q: return
        l, s = self.split(p, q)
        self.id[s] = l
        self.sz[l] += self.sz[s]
        self.count -= 1

class UnionFindComps:
    def __init__(self, vals):
        assert len(vals) == len(set(vals))
        self.vals = vals; self.n = len(self.vals)
        self.id = [i for i in range(self.n)]
        self.map = {val: ind for ind, val in enumerate(self.vals)}
        self.comps = {i: set() for i in range(self.n)}
        self.max = 1

    def sz(self, p):
        return len(self.comps[p])

    def path(self, i):
        p = [i]
        while not i == self.id[i]:
            i = self.id[i]; p.append(i)
        return p

    def compressed(self, path):
        root = path[-1]
        for p in path: self.id[p] = root
        return root

    def find(self, i):
        return self.compressed(self.path(i))

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if p == q: return
        self.join(p, q)

    def split(self, p, q):
        return (p, q) if self.sz(p) > self.sz(q) else (q, p)

    def join(self, p, q):
        l, s = self.split(p, q)
        self.id[s] = l
        self.comps[l] = self.comps[l].union(self.comps.pop(s))
        self.max = max(self.max, self.comps[l])

    def connect(self, a, b):
        self.union(self.map[a], self.map[b])


class UnionFind:
    """
    A data structure to manage a partition of a set into disjoint subsets.

    Attributes:
        __id (list): List to store the parent of each element.
        __comps (dict): Dictionary to store the components.
    """

    def __init__(self, n: int):
        """
        Initializes the UnionFind object with n elements, each in its own set.

        Args:
            n (int): The number of elements.
        """
        self.__id: list[int] = list(range(n))
        self.__comps: dict[int, set[int]] = {i: {i} for i in range(n)}

    def __parent(self, i: int) -> int:
        """
        Returns the parent of the element i.
        Args:
            i (int): The element whose parent is to be found.

        Returns:
            int: The parent of the element i.
        """
        return self.__id[i]

    def __assign(self, i, p):
        self.__id[i] = p

    def __is_root(self, i):
        return i == self.__parent(i)

    def __size(self, i):
        return len(self.__comps[self.find(i)])

    def __is_greater(self, i, j):
        return self.__size(i) > self.__size(j)

    def __split(self, p, q):
        return (p, q) if self.__is_greater(p, q) else (q, p)

    def __merge(self, s, l):
        self.__comps[s].update(self.__comps.pop(s))

    def __join(self, p, q):
        l, s = self.__split(p, q)
        self.__assign(s, l)
        self.__merge(s, l)

    @property
    def count(self):
        return len(self.__comps)

    def find(self, i):
        if not self.__is_root(i):
            root = self.find(self.__parent(i))
            self.__assign(i, root)
        return self.__parent(i)

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if not p == q: self.__join(p, q)


if __name__ == '__main__':
    uf = UnionFind(10)
    print(uf.__sizeof__())