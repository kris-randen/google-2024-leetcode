"""
Data Structures
1. Union Find
2. Index Priority Queue
3. Left Leaning Red Black (LLRB) Binary Search Tree
4. Trie
5. LRU Cache
6. Interval Search Tree
7. kd-Tree

Algorithms

a. Graphs
1. DFS
2. BFS
3. Dijkstra (SSSP non-negative) O(m log (n))
4. Bellman-Ford (SSSP) O(mn)
5. Floyd-Warshall (APSP) O(n ^ 3)
6. Johnson (APSP) O(mn * log (n))
7. Minimum Spanning Tree Prim
8. Minimum Spanning Tree Kruskal
9. Max Flow - Min Cut Ford Fulkerson
10. Strong Connected Components Kosaraju
11. DAG SSSP (general edge weights)

b. Trees
1.  1D Range Search
2. Line Segment Intersection
3. Rectangle Intersection
4. Huffman Encoding

c. String
1. Knuth-Morris-Pratt
2. Boyer-Moore
3. Rabin-Karp


Patterns

Greedy
1. Fractional Knapsack
2. Scheduling

Dynamic Programming
1. Weight Independent Sets (WIS) in Path Graphs
2. Knapsack (Infinite)
3. Knapsack (Finite)
4. Sequence Alignment
"""
import random

"""
==============
DATASTRUCTURES
==============
"""

"""
1. Union-Find
"""
"""
API

bool find(p, q): Returns if p and q belong to the same subset
int union(p, q): Joins (unions) the sets p and q belong to and returns the root

"""

"""
Implementation
"""


class UnionFind:
    def __init__(self, n, es=None):
        self.id = [_ for _ in range(n)]
        self.sz = [1 for _ in range(n)]
        self.n = n
        self.cs = n  # Number of disjoint sets
        self.es = [] if not es else es
        for e in self.es:
            self.union(e[0], e[1])

    def parent(self, c):
        return self.id[c]

    def assign(self, c, p):
        self.id[c] = p; return p

    def is_root(self, p):
        return p == self.parent(p)

    def path_of(self, p):
        path = [p]
        while not self.is_root(p):
            p = self.parent(p);
            path.append(p)
        return path

    def compress(self, p):
        path = self.path_of(p);
        r = path[-1]
        for q in path: self.assign(q, r)
        return r

    def root(self, p):
        return self.compress(p)

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def order(self, p, q):
        r, s = self.root(p), self.root(q)
        return (r, s) if self.sz[r] > self.sz[s] else (s, r)

    def union(self, s, t):
        if self.find(s, t): return
        p, c = self.order(s, t)
        self.assign(c, p)
        self.sz[p] += self.sz[c]
        self.cs -= 1
        return p


class ValidatorUnionFind:
    def __init__(self, n, es=None):
        self.n = n;
        self.es = [] if not es else es
        self.sets = [{i} for i in range(n)]
        for e in self.es: self.add(e)

    def get(self, p):
        for i in range(len(self.sets)):
            if p in self.sets[i]: return i
        return None

    def add(self, e):
        p, q = e;
        r, s = self.get(p), self.get(q)
        if r == s: return
        self.sets[r] = self.sets[r].union(self.sets[s])
        self.sets.pop(s)

    def find(self, p, q):
        return self.get(p) == self.get(q)

    def union(self, p, q):
        self.add([p, q])


def gen_test_case_union_find(n):
    es, qs = [], []
    for i in range(n // 2):
        p, q = random.randint(0, n - 1), random.randint(0, n - 1)
        es.append([p, q])
    for i in range(n):
        p, q = random.randint(0, n - 1), random.randint(0, n - 1)
        qs.append([p, q])
    return n, es, qs


def gen_test_cases_union_find(lo, hi):
    tests = []
    for i in range(lo, hi):
        tests.append(gen_test_case_union_find(i))
    return tests


def validate_union_find(uf, vf, qs):
    for q in qs:
        assert uf.find(q[0], q[1]) == vf.find(q[0], q[1])


def test_union_find():
    lo, hi = 10, 56
    tests = gen_test_cases_union_find(lo, hi)
    for test in tests:
        n, es, qs = test
        uf = UnionFind(n, es)
        vf = ValidatorUnionFind(n, es)
        validate_union_find(uf, vf, qs)


"""
2. Indexed Priority Queue
"""
"""
API

IndexPQ[Key]

int   top(): returns the top element index
void  push(i, key): inserts key at index i
int   pop(): returns the top element and removes (deletes) it
int   change(i, key): changes the existing value at index i to key
[int] sort(): returns the sorted permutation of indices
"""

"""
Implementation
"""


class IndexPQ:
    def __init__(self, keys, order=None):
        self.keys = [None] + keys
        self.n = len(keys);
        self.N = None
        self.pq = [-1] + [1 + i for i in range(self.n)]
        self.qp = [-1] + [1 + i for i in range(self.n)]
        self.order = order if order else (lambda x, y: x if x < y else y)
        self.heapify()

    def key(self, i):
        return self.keys[self.pq[i]]

    def size(self):
        return self.n if not self.N else self.N

    def ord(self, i, j):
        p, q = self.key(i), self.key(j)
        if p and q: return i if self.order(p, q) == p else j
        return i if not p else j

    def pref(self, i, j):
        if i and j: return self.ord(i, j)
        return i if not j else j

    def up(self, i):
        return i // 2

    def lt(self, i):
        return 2 * i

    def rt(self, i):
        return (2 * i) + 1

    def is_legit(self, i):
        return 1 <= i <= self.size()

    def legit(self, i):
        if self.is_legit(i): return i

    def parent(self, c):
        return self.legit(self.up(c))

    def left(self, p):
        return self.legit(self.lt(p))

    def right(self, p):
        return self.legit(self.rt(p))

    def child(self, p):
        return self.pref(self.left(p), self.right(p))

    def bal_up(self, c):
        p = self.parent(c)
        if not p: return True
        return self.pref(p, c) == p

    def bal_down(self, p):
        return self.pref(self.child(p), p) == p

    def unbal_parent(self, c):
        if not self.bal_up(c): return self.parent(c)

    def unbal_child(self, p):
        if not self.bal_down(p): return self.child(p)

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j

    def lift(self, c):
        p = self.unbal_parent(c)
        if p: self.swap(p, c); return p

    def drop(self, p):
        c = self.unbal_child(p)
        if c: self.swap(c, p); return c

    def swim(self, c):
        while not self.bal_up(c): c = self.lift(c)

    def sink(self, p):
        while not self.bal_down(p): p = self.drop(p)

    def heapify(self):
        for i in reversed(range(1, self.size() + 1)):
            self.sink(i)

    def push(self, i, key):
        assert self.qp[i] == -1, f'key at index {i} already exists. Try using change key method instead.'
        self.n += 1;
        self.keys[i] = key
        self.pq[self.n] = i;
        self.qp[i] = self.n
        self.swim(self.n)
        return self.qp[i]

    def top(self):
        return self.key(self.pq[1])

    def del_top(self):
        i = self.pq[1]
        top = self.key(i)
        self.keys[i] = None
        self.swap(1, self.size())
        self.qp[i] = self.pq[self.size()] = -1
        self.n -= 1;
        self.sink(1)
        return i, top

    def pop(self):
        return self.del_top()

    def change(self, i, key):
        old = self.key(i)
        self.keys[i] = key
        self.sink(self.qp[i])
        self.swim(self.qp[i])
        return old

    def sort(self):
        self.N = self.size()
        while self.N > 1:
            self.swap(1, self.N)
            self.N -= 1;
            self.sink(1)
        self.N = None
        res = [self.keys[i] for i in self.pq]
        self.heapify()
        return res[1:]


def gen_test_case_index_pq(n, maxN=100):
    v = random.sample(range(1, maxN), n)
    return v


def gen_test_cases_index_pq(lo, hi, maxN=100):
    tests = []
    for i in range(lo, hi):
        tests.append(gen_test_case_index_pq(i))
    return tests


def validate_index_pq(vs):
    pq = IndexPQ(vs)
    svs = sorted(vs, reverse=True)
    assert svs == pq.sort()


def test_index_pq(lo=10, hi=56):
    for v in gen_test_cases_index_pq(lo, hi):
        validate_index_pq(v)


"""
3. LLRB
"""
"""
API
"""

"""
Implementation
"""

"""
4. Trie
"""
"""
API
"""

"""
Implementation
"""

"""
5. LRU Cache
"""
"""
API
"""

"""
Implementation
"""

"""
6. Interval Search Tree
"""
"""
API
"""

"""
Implementation
"""

"""
7. kd-Tree
"""
"""
API
"""

"""
Implementation
"""

"""
==========
ALGORITHMS
==========
"""
"""
a. Graphs
"""
from collections import defaultdict


class Graph:
    def __init__(self, V, es=None, directed=True):
        self.V = V;
        self.directed = directed
        self.adj = defaultdict(set)
        self.es = es if es else []
        for u, v in self.es:
            self.add(u, v)

    def add(self, u, v):
        self.adj[u].add(v)
        if not self.directed: self.adj[v].add(u)


"""
1. DFS
"""


class DFS:
    def __init__(self, g):
        self.g = g
        self.visited = [0] * self.g.V

    def clear(self):
        self.visited = [0] * self.g.V

    def find(self, s, t):
        def dfs(u, v):
            if u == v: return True
            if self.visited[u]: return False
            self.visited[u] = 1
            for u in self.g.adj[u]:
                if self.find(u, v): return True
            return False

        self.clear()
        return dfs(s, t)

    def acyclic(self):
        def dfs(u):
            if self.visited[u] == -1: return False
            if self.visited[u] == 1: return True
            self.visited[u] = -1
            for v in self.g.adj[u]:
                if not dfs(v): return False
            self.visited[u] = 1
            return True

        self.clear()
        for v in range(self.g.V):
            if not dfs(v): return False
        return True

    def paths(self, s, t):
        all_ps = []

        def dfs(u, w, ps):
            if self.visited[u] and u != w: return
            if u == w:
                ps.append(u)
                all_ps.append(ps)
                return
            self.visited[u] = 1
            for v in self.g.adj[u]:
                dfs(v, w, ps + [u])
            self.visited[u] = 0

        self.clear()
        dfs(s, t, [])
        return all_ps


"""
2. BFS
"""

from collections import deque


class BFS:
    def __init__(self, g):
        self.g = g
        self.visited = [0] * self.g.V

    def paths(self, s, t):
        all_paths = []

        def bfs(u):
            q = deque([u])
            while q:
                v = q.popleft()
                self.visited[v] = 1
                for w in self.g.adj[v]:
                    if not self.visited[w]:
                        pass
                pass
            pass

        pass


"""
Single Source Shortest Paths (SSSP)
"""
"""
3. Dijkstra (non-negative)
"""

"""
4. Bellman-Ford (general)
"""

"""
5. DAG SSSP (general)
"""

"""
All Pairs Shortest Paths (APSP)
"""
"""
5. Floyd-Warshall
"""

"""
6. Johnson
"""

"""
5. Prim's MST
"""

"""
6. Kruskal's MST
"""

"""
7. Kosaraju's SCC
"""

"""
b. Trees
"""
"""
1. 1D Range Search
"""

"""
2. Line Segment Intersection
"""

"""
3. Rectangle Intersection
"""

"""
4. Huffman Encoding
"""

"""
c. String
"""
"""
Deterministic Finite Automaton DFA
"""

"""
1. Knuth-Morris-Pratt (KMP) 
"""

"""
2. Boyer-Moore
"""

"""
3. Rabin-Karp (Hashing)
"""

"""
==========
PATTERNS
==========
"""

"""
a. Recursion and Backtracking
"""

"""
b. Greedy
"""
"""
1. Scheduling
"""

"""
2. Knapsack (Fractional)
"""

"""
c. Dynamic Programming
"""
"""
1. Knapsack (with repetitions)
"""

"""
2. Knapsack (without repetitions)
"""

"""
3. Weight Independent Sets (WIS) in Path Graphs
"""

"""
4. Sequence Alignment
"""

"""
d. Two-Pointer
"""

"""
e. Sliding Window
"""

class DiGraph:
    def __init__(self, V):
        self.V = V
        self.adj_out = [set() for _ in range(self.V)]
        self.adj_in = [set() for _ in range(self.V)]

    def add_edge(self, u, v):
        self.adj_out[u].add(v)
        self.adj_in[v].add(u)

    def degree_out(self, v):
        return len(self.adj_out[v])

    def degree_in(self, v):
        return len(self.adj_in[v])

class DFS:
    def __init__(self, G: DiGraph, s=0):
        self.G = G; self.V = self.G.V; self.s = s
        self.marked = [False for _ in range(self.V)]
        self.edge_to = [None for _ in range(self.V)]
        self.dfs(self.G, self.s)

    def dfs(self, G, v):
        self.marked[v] = True
        for w in G.adj_out[v]:
            if not self.marked[w]:
                self.dfs(G, w)
                self.edge_to[w] = v

class BFS:
    def __init__(self, G, s=0):
        self.G = G; self.V = self.G.V; self.s = s
        self.marked = [False for _ in range(self.V)]
        self.edge_to = [None for _ in range(self.V)]
        self.dist_to = [None for _ in range(self.V)]
        self.bfs(self.G, self.s)

    def bfs(self, G, v):
        q = [v]
        self.marked[v] = True
        self.edge_to[v] = v
        self.dist_to[v] = 0
        while q:

            pass