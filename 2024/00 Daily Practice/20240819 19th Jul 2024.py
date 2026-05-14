"""
"""

from toolz.curried import pipe, map, filter

class Point:
    def __init__(self, i, j):
        self.p = (i, j)

    @property
    def i(self):
        return self.p[0]

    @property
    def j(self):
        return self.p[1]

    def __repr__(self):
        return f'Point({self.i},{self.j})'

    def up(self):
        return Point(self.i - 1, self.j)

    def dn(self):
        return Point(self.i + 1, self.j)

    def lt(self):
        return Point(self.i, self.j - 1)

    def rt(self):
        return Point(self.i, self.j + 1)

    def adj(self):
        return self.up(), self.dn(), self.lt(), self.rt()


class Board:
    def __init__(self, matrix):
        self.b = matrix; self.m, self.n = len(self.b), len(self.b[0])

    def __getitem__(self, ind):
        return self.b[ind]

    def __setitem__(self, ind, row):
        self.b[ind] = row

    def val(self, p: Point):
        return self[p.i][p.j]

    def assign(self, p: Point, val='X'):
        self[p.i][p.j] = val

    def valid(self, p: Point):
        return 0 <= p.i < self.m and 0 <= p.j < self.n

    def flat(self, p: Point):
        return p.i * self.n + p.j

    def flag(self, p: Point, val='O'):
        return self.val(p) == val

    def inflate(self, v):
        return Point(v // self.n, v % self.n)

    def tp_bdry(self, p: Point):
        return p.i == 0

    def bt_bdry(self, p: Point):
        return p.i == self.m - 1

    def lt_bdry(self, p: Point):
        return p.j == 0

    def rt_bdry(self, p: Point):
        return p.j == self.n - 1

    def bdry(self, p: Point):
        return \
            self.tp_bdry(p) or \
            self.bt_bdry(p) or \
            self.lt_bdry(p) or \
            self.rt_bdry(p)

    def inside(self, p: Point):
        return self.valid(p) and not self.bdry(p)

    def ps(self):
        return (Point(i, j) for i in range(self.m) for j in range(self.n))

    def psf(self):
        return pipe(
            self.ps(),
            map(self.flat)
        )

    def ns(self, p):
        return pipe(
            p.adj(),
            filter(self.valid)
        )

    def ns_flagged(self, p):
        if not self.flag(p): return set()
        return pipe(
            self.ns(p),
            filter(self.flag)
        )

    def nbrs(self, v):
        return pipe(
            self.ns_flagged(self.inflate(v)),
            map(self.flat)
        )

    def adj(self):
        return pipe(
            self.psf(),
            map(lambda v: (v, set(self.nbrs(v)))),
            dict
        )

class Graph:
    def __init__(self, b: Board):
        self.b = b; self.V = b.m * b.n
        self.adj = b.adj()

if __name__ == '__main__':
    matrix = [['O', 'X', 'O', 'X'], ['O', 'X', 'O', 'X']]
    b = Board(matrix)
    ns = b.ns(Point(0, 2))
    print(b.adj())












# class Point1:
#     def __init__(self, i, j):
#         self.p = (i, j)
#
#     @property
#     def i(self):
#         return self.p[0]
#
#     @property
#     def j(self):
#         return self.p[1]
#
#     def __repr__(self):
#         return f"Point({self.i}, {self.j})"
#
#     def up(self):
#         return Point1(self.i - 1, self.j)
#
#     def dn(self):
#         return Point1(self.i + 1, self.j)
#
#     def lt(self):
#         return Point1(self.i, self.j - 1)
#
#     def rt(self):
#         return Point1(self.i, self.j + 1)
#
#     def adj(self):
#         return self.up(), self.dn(), self.lt(), self.rt()
#
# class Board1:
#     def __init__(self, matrix):
#         self.b = matrix
#         self.m, self.n = len(self.b), len(self.b[0])
#
#     def __getitem__(self, ind):
#         return self.b[ind]
#
#     def __setitem__(self, ind, row):
#         self.b[ind] = row
#
#     def flatten(self, p: Point1):
#         return p.i * self.n + p.j
#
#     def inflate(self, v):
#         return Point1(v // self.n, v % self.n)
#
#     def ps(self):
#         return (Point1(i, j) for i in range(self.m) for j in range(self.n))
#
#     def __iter__(self):
#         return self.ps()
#
#     def val(self, p):
#         return self[p.i][p.j]
#
#     def valid(self, p):
#         return 0 <= p.i < self.m and 0 <= p.j < self.n
#
#     def ns(self, p):
#         return filter(self.valid, p.adj())
#
#     def flagged(self, p: Point1, val='O'):
#         return self.val(p) == val
#
#     def ps_flat(self):
#         return map(self.flatten, self.ps())
#

# if __name__ == '__main__':
#     pass
#     # matrix = [[0, 1, 2, 3], [3, 7, 0, 5]]
#     # b = Board1(matrix)
#     # ns = b.ns(Point1(0, 2))
#     # print(f"ns = {ns}")
#     # print(f"ps_flat = {b.ps_flat()}")

