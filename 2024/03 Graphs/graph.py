
from collections import defaultdict
from typing import List, Any


class Graph:
    """
    Undirected Graph
    """

    def __init__(self, V):
        self.V = V
        self.adj = defaultdict(set)

    def add_edge(self, u, v):
        self.adj[u].add(v)
        self.adj[v].add(u)

"""

2D Graph for problems with 2D Matrix inputs

"""


class Point:
    def __init__(self, i, j):
        self.p = (i, j)

    def __iter__(self):
        yield self.i
        yield self.j

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __hash__(self):
        return hash((self.i, self.j))

    @property
    def i(self):
        return self.p[0]

    @property
    def j(self):
        return self.p[1]

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
    def __init__(self, board):
        self.b = board
        self.m, self.n = len(self.b), len(self.b[0])

    def val(self, p: Point):
        return self[p.i][p.j]

    def __getitem__(self, index: int) -> List[Any]:
        return self.b[index]

    def __setitem__(self, index: int, row: List[Any]):
        self.b[index] = row

    def assign(self, p: Point, val):
        self[p.i][p.j] = val

    def valid(self, p: Point):
        return 0 <= p.i < self.m and 0 <= p.j < self.n

    def lt_bdry(self, p: Point):
        return p.j == 0

    def rt_bdry(self, p: Point):
        return p.j == self.n - 1

    def tp_bdry(self, p: Point):
        return p.i == 0

    def bt_bdry(self, p: Point):
        return p.i == self.m - 1

    def bdry(self, p: Point):
        return \
            self.lt_bdry(p) or \
            self.rt_bdry(p) or \
            self.tp_bdry(p) or \
            self.bt_bdry(p)

    def bdry_flat(self, v):
        return self.bdry(self.inflate(v))

    def not_bdry_flat(self, v):
        return not self.bdry_flat(v)

    def flatten(self, p: Point):
        return (p.i * self.n) + p.j

    def inflate(self, k):
        return Point(k // self.n, k % self.n)

    def all_ns(self, p: Point):
        return filter(self.valid, p.adj())

    def is_flagged(self, p: Point, val='O'):
        return self.val(p) == val

    def ns(self, p: Point):
        if self.val(p) == 'X': return set()
        return filter(self.is_flagged, self.all_ns(p))

    def ns_flat(self, k):
        return map(self.flatten, self.ns(self.inflate(k)))

    def ps(self):
        return (Point(i, j) for i in range(self.m) for j in range(self.n))

    def __iter__(self):
        return self.ps()

    def __len__(self):
        return len(self.b)

    def ps_flat(self):
        return map(self.flatten, self.ps())

    def adj(self):
        return dict(map(lambda p: (p, set(self.ns_flat(p))), self.ps_flat()))


class Graph2D:
    def __init__(self, b: Board):
        self.b, self.m, self.n = b, b.m, b.n
        self.V = self.m * self.n
        self.adj = b.adj()


class CC:
    def __init__(self):
        self.count, self.marked, self.cc = 0, [], {}

    def execute(self, g):
        self.marked = [0 for _ in range(g.V)]
        self.cc = defaultdict(set)
        for v in range(g.V):
            if not self.marked[v]:
                self.dfs(g, v)
                self.count += 1

    def dfs(self, g, v):
        self.marked[v] = 1
        self.cc[self.count].add(v)
        for w in g.adj[v]:
            if not self.marked[w]:
                self.dfs(g, w)


class Capture:
    def __init__(self, board):
        self.b = Board(board)
        self.g = Graph2D(self.b)
        cc = CC()
        cc.execute(self.g)
        self.cc = cc.cc

    def surrounded(self, ind):
        return all(map(self.b.not_bdry_flat, self.cc[ind]))

    def mark(self, v, val='X'):
        self.b.assign(self.b.inflate(v), val)

    def capture_cc(self, ind, val='X'):
        for v in self.cc[ind]: self.mark(v, val)

    def capture(self, val='X'):
        for ind in self.cc:
            if self.surrounded(ind): self.capture_cc(ind, val)
