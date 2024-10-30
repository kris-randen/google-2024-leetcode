class Heap:
    def __init__(self, keys=None, compare=lambda x, y: x < y):
        self.pq = [None] + ([] if not keys else keys)
        self.qp = {key: index for index, key in enumerate(self.pq)}
        self.compare = compare; self.N = None
        self.heapify()

    @property
    def size(self):
        return self.N if self.N else len(self.pq) - 1

    def valid(self, i):
        if not i: return None
        return i if 1 <= i <= self.size else None

    def up(self, i):
        return i // 2

    def left(self, i):
        return 2 * i

    def right(self, i):
        return 2 * i + 1

    def val(self, i):
        return self.pq[i] if self.valid(i) else None

    def comp(self, i, j):
        return self.compare(self.val(i), self.val(j))

    def pref(self, i, j):
        if i and j: return i if self.comp(i, j) else j
        return i if not j else j

    def parent(self, i):
        return self.valid(self.up(i))

    def left_child(self, i):
        return self.valid(self.left(i))

    def right_child(self, i):
        return self.valid((self.right(i)))

    def child(self, i):
        return self.pref(self.left_child(i), self.right_child(i))

    def unbal(self, p, c):
        return self.pref(p, c) == c

    def bal_pref(self, p, c):
        return None if self.unbal(p, c) else self.pref(p, c)

    def bal_up(self, c):
        p = self.parent(c)
        return not p or self.pref(p, c) == p

    def bal_down(self, p):
        c = self.child(p)
        return not c or self.pref(p, c) == p

    def unbal_up(self, c):
        return self.parent(c) if not self.bal_up(c) else None

    def unbal_down(self, p):
        return self.child(p) if not self.bal_down(p) else None

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]] = i; self.qp[self.pq[j]] = j
        return j

    def swim(self, c):
        while p := self.unbal_up(c):
            c = self.swap(c, p)

    def sink(self, p):
        while c := self.unbal_down(p):
            p = self.swap(p, c)

    def insert(self, key):
        self.pq.append(key); n = self.size
        self.qp[key] = n
        self.swim(n)


    def pop(self):
        self.swap(self.N, 1)
        top = self.pq.pop()
        self.qp.pop(top)
        self.sink(1)
        return top

    def top(self):
        return self.pq[1]

    def update(self, key, new):
        i = self.qp[key]
        self.pq[i] = new
        self.sink(i)
        self.swim(i)
        return key

    def heapify(self):
        for p in range(self.size, 0, -1): self.sink(p)

    def sort(self):
        self.N = self.size
        while self.N > 1:
            self.swap(1, self.N)
            self.N -= 1
            self.sink(1)
        sorted_list = self.pq[1:].copy()
        self.N = None
        self.heapify()
        return sorted_list


class HeapDict:
    def __init__(self, weights=None, compare=lambda x, y: x < y):
        self.__wt = {} if not weights else weights
        self.__pq = [None] + list(self.__wt.keys())
        self.__qp = {k: i for i, k in enumerate(self.__pq)}
        self.__cmp = compare; self.N = None
        self.__heapify()

    def __keys(self):
        return self.__pq[1:].copy()

    def __str__(self):
        return f"{self.__keys()}"

    def size(self):
        return self.N if self.N else len(self.__wt)

    def __wt_ind(self, i):
        return self.__wt[self.__pq[i]]

    def __cmp_ind(self, i, j):
        return self.__cmp(self.__wt_ind(i), self.__wt_ind(j))

    def __pref(self, i, j):
        if i and j:
            return i if self.__cmp_ind(i, j) else j
        return i if not j else j

    def __valid(self, i):
        return i if 1 <= i <= self.size() else None

    def __up(self, i):
        return i // 2

    def __left(self, i):
        return 2 * i

    def __right(self, i):
        return 2 * i + 1

    def __parent(self, c):
        return self.__valid(self.__up(c))

    def __l_child(self, p):
        return self.__valid(self.__left(p))

    def __r_child(self, p):
        return self.__valid(self.__right(p))

    def __child(self, p):
        return self.__pref(self.__l_child(p), self.__r_child(p))

    def __bal_up(self, c):
        p = self.__parent(c)
        return not p or self.__pref(p, c) == p

    def __bal_dn(self, p):
        c = self.__child(p)
        return not c or self.__pref(p, c) == p

    def __unbal_up(self, c):
        return self.__parent(c) if not self.__bal_up(c) else None

    def __unbal_dn(self, p):
        return self.__child(p) if not self.__bal_dn(p) else None

    def __swap(self, i, j):
        assert self.__valid(i) and self.__valid(j)
        self.__pq[i], self.__pq[j] = self.__pq[j], self.__pq[i]
        self.__qp[self.__pq[i]], self.__qp[self.__pq[j]] = i, j

    def __climb(self, i, j):
        self.__swap(i, j); return j

    def __swim(self, c):
        while not self.__bal_up(c):
            c = self.__climb(c, self.__unbal_up(c))

    def __sink(self, p):
        while not self.__bal_dn(p):
            p = self.__climb(p, self.__unbal_dn(p))

    def __heapify(self):
        for p in range(self.size(), 0, -1): self.__sink(p)

    def __assign(self, key, val):
        i = self.__qp[key]; self.__wt[key] = val
        return i

    def __balance(self, i):
        self.__swim(i); self.__sink(i)

    def __append(self, key, val):
        self.__pq.append(key)
        self.__wt[key] = val

    def __sort_one(self):
        self.__swap(self.N, 1)
        self.N -= 1; self.__sink(1)

    def __sort_keys(self):
        self.N = self.size()
        while self.N > 1: self.__sort_one()
        self.N = None; return self.__keys()


    def update(self, key, val):
        i = self.__assign(key, val)
        self.__balance(i)

    def push(self, key, val):
        if key in self.__wt: self.update(key, val)
        self.__append(key, val)
        self.__swim(self.size())

    def pop(self):
        self.__swap(self.size(), 1)
        top = self.__pq.pop()
        self.__sink(1)
        return top

    def sorted_keys(self):
        keys_sorted = self.__sort_keys()
        self.__heapify()
        return keys_sorted

    def sorted_vals(self):
        keys = self.sorted_keys()
        return list(map(lambda key: self.__wt[key], keys))

    def sorted_key_vals(self):
        return list(zip(self.sorted_keys(), self.sorted_vals()))

if __name__ == '__main__':
    vs = [11, 2, 1, 5, 4, 7, 9, 3, 25, 17, 13]
    vs_dict = dict(enumerate(vs, start=1))
    print(vs_dict)
    pq = HeapDict(vs_dict)
    print(f"heap = {pq}")
    sorted_keys = pq.sorted_keys()
    print(f"sorted_keys = {sorted_keys}")
    sorted_vals = pq.sorted_vals()
    print(f"sorted_vals = {sorted_vals}")
    sorted_key_vals = pq.sorted_key_vals()
    print(f"sorted_key_vals = {sorted_key_vals}")
