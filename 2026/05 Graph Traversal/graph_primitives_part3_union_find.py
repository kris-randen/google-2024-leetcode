"""
Graph Primitives — Part 3: Union-Find / Dynamic Connectivity

LeetCode-style version.

Part 1 covered plain DFS/BFS traversal.
Part 2 covered DFS/BFS with state:
    parent
    color
    order
    indegree
    path
    grid boundary state

Part 3 covers Union-Find.

Core idea:
    DFS/BFS discovers components by walking the graph.
    Union-Find maintains components while edges are added.

Use Union-Find when the problem mostly asks:
    Are these two nodes in the same component?
    How many components remain?
    Does this edge create a cycle?
    Can I merge these groups?

Design rule:
    Keep it boring and fast for LeetCode.
    No generics. No protocols. No type annotations.

Graph convention from earlier parts:
    g[v] = [w1, w2, w3]

Union-Find convention:
    uf.union(a, b) returns True if it actually merged two components.
    uf.union(a, b) returns False if a and b were already connected.
"""

from collections import defaultdict


# ============================================================
# 1. UNION-FIND CORE
# ============================================================

"""
Why this primitive exists
-------------------------
DFS/BFS is great when the graph is already built and we want to traverse it.

Union-Find is better when edges are being processed one by one and all we need
is component membership.

Core state:
    parent[x]  -> representative pointer
    size[x]    -> size of component rooted at x
    count      -> number of components

Core operations:
    find(x)       -> component representative
    union(a, b)   -> merge components
    connected(a,b)-> same component?

Core invariant:
    Two nodes are connected iff find(a) == find(b).

This builds up to:
    connected components
    graph valid tree
    redundant connection
    accounts merge
    equality equations
    smallest string with swaps
    network connectivity
    Kruskal MST later
"""


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, x):
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]

        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return False

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1

        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def component_size(self, x):
        return self.size[self.find(x)]


# ============================================================
# 2. COMPONENT COUNT FROM EDGES
# ============================================================

"""
Why this primitive exists
-------------------------
If the input is just n + edges, we do not need to build an adjacency list to
count connected components.

We can simply union every edge.

Composition:
    UnionFind
    + union every edge
    -> number of components

Problems:
    323. Number of Connected Components in an Undirected Graph
    547. Number of Provinces
    1319. Number of Operations to Make Network Connected
"""


def count_components(n, edges):
    uf = UnionFind(n)

    for a, b in edges:
        uf.union(a, b)

    return uf.count


# Problem 323. Number of Connected Components in an Undirected Graph
# Reduction:
#     Connected components = components after unioning all edges.


class Solution323:
    def countComponents(self, n, edges):
        return count_components(n, edges)


# Problem 547. Number of Provinces
# Reduction:
#     Matrix entry isConnected[i][j] == 1 is just an undirected edge i -- j.


class Solution547:
    def findCircleNum(self, isConnected):
        n = len(isConnected)
        uf = UnionFind(n)

        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j]:
                    uf.union(i, j)

        return uf.count


# ============================================================
# 3. CYCLE DETECTION / TREE RECOGNITION WITH DSU
# ============================================================

"""
Why this primitive exists
-------------------------
In an undirected graph, an edge (a, b) creates a cycle exactly when a and b are
already connected before adding that edge.

Core invariant:
    if not uf.union(a, b):
        edge (a, b) is redundant / creates a cycle

This builds up to:
    graph valid tree
    redundant connection
    Kruskal MST later
"""


def has_cycle_dsu(n, edges):
    uf = UnionFind(n)

    for a, b in edges:
        if not uf.union(a, b):
            return True

    return False


# Problem 261. Graph Valid Tree
# Reduction:
#     A graph is a tree iff:
#         it has exactly n - 1 edges
#         and those edges connect all nodes without cycles.
#
# With n - 1 edges, no cycle and connected become equivalent enough in practice:
# after unioning all edges, count must be 1.


class Solution261:
    def validTree(self, n, edges):
        if len(edges) != n - 1:
            return False

        return count_components(n, edges) == 1


# Problem 684. Redundant Connection
# Reduction:
#     Return the first edge whose endpoints are already connected.


class Solution684:
    def findRedundantConnection(self, edges):
        uf = UnionFind(len(edges) + 1)

        for a, b in edges:
            if not uf.union(a, b):
                return [a, b]

        return []


# ============================================================
# 4. MINIMUM OPERATIONS TO CONNECT NETWORK
# ============================================================

"""
Why this primitive exists
-------------------------
If a graph has c connected components, then at least c - 1 new cables are needed
to connect them.

But this is possible only if the graph has at least n - 1 total cables.

Composition:
    edge count feasibility
    + UnionFind component count
    -> operations needed

Problem:
    1319. Number of Operations to Make Network Connected
"""


class Solution1319:
    def makeConnected(self, n, connections):
        if len(connections) < n - 1:
            return -1

        return count_components(n, connections) - 1


# ============================================================
# 5. GROUPING BY CONNECTED COMPONENT
# ============================================================

"""
Why this primitive exists
-------------------------
Sometimes Union-Find is used not just to ask whether two nodes are connected,
but to group all nodes by their final component.

Core pattern:
    union all allowed pairs
    then group items by uf.find(i)

This builds up to:
    accounts merge
    smallest string with swaps
    connected swap groups
"""


def groups_from_uf(uf, n):
    groups = defaultdict(list)

    for i in range(n):
        groups[uf.find(i)].append(i)

    return list(groups.values())


# Problem 1202. Smallest String With Swaps
# Reduction:
#     Allowed swaps create connected components of indices.
#     Inside one component, characters can be permuted freely.
#     To get lexicographically smallest string, put smallest chars at smallest indices.


class Solution1202:
    def smallestStringWithSwaps(self, s, pairs):
        uf = UnionFind(len(s))

        for a, b in pairs:
            uf.union(a, b)

        ans = list(s)

        for group in groups_from_uf(uf, len(s)):
            chars = sorted(ans[i] for i in group)

            for i, ch in zip(sorted(group), chars):
                ans[i] = ch

        return "".join(ans)


# ============================================================
# 6. ACCOUNTS MERGE
# ============================================================

"""
Why this primitive exists
-------------------------
Not every Union-Find problem starts with integer nodes.

For string/object nodes, first map each unique object to an integer id.
Then use the same UnionFind.

Core pattern:
    object -> id
    union ids
    group objects by root

Problem:
    721. Accounts Merge
"""


def get_id(x, ids):
    if x not in ids:
        ids[x] = len(ids)

    return ids[x]


class Solution721:
    def accountsMerge(self, accounts):
        ids = {}
        email_to_name = {}

        for account in accounts:
            name = account[0]

            for email in account[1:]:
                get_id(email, ids)
                email_to_name[email] = name

        uf = UnionFind(len(ids))

        for account in accounts:
            first = ids[account[1]]

            for email in account[2:]:
                uf.union(first, ids[email])

        groups = defaultdict(list)

        for email, i in ids.items():
            groups[uf.find(i)].append(email)

        ans = []

        for emails in groups.values():
            emails.sort()
            ans.append([email_to_name[emails[0]]] + emails)

        return ans


# ============================================================
# 7. EQUATION SATISFIABILITY
# ============================================================

"""
Why this primitive exists
-------------------------
Equality constraints merge components.
Inequality constraints verify that two nodes are NOT in the same component.

Core pattern:
    process all == first
    then check all !=

Problem:
    990. Satisfiability of Equality Equations
"""


class Solution990:
    def equationsPossible(self, equations):
        uf = UnionFind(26)

        for eq in equations:
            if eq[1:3] == "==":
                uf.union(ord(eq[0]) - ord("a"), ord(eq[3]) - ord("a"))

        for eq in equations:
            if eq[1:3] == "!=":
                a = ord(eq[0]) - ord("a")
                b = ord(eq[3]) - ord("a")

                if uf.connected(a, b):
                    return False

        return True


# ============================================================
# 8. STONES REMOVED WITH SAME ROW OR COLUMN
# ============================================================

"""
Why this primitive exists
-------------------------
Some problems hide the graph.

For stones:
    two stones are connected if they share a row or column.

Instead of explicitly connecting every pair of stones in the same row/column,
make each row and each column a Union-Find node.
Then each stone unions its row-node with its column-node.

Key fact:
    In each connected component of k stones, we can remove k - 1 stones.
    Total removable stones = total stones - number of connected components.

Problem:
    947. Most Stones Removed with Same Row or Column
"""


class Solution947:
    def removeStones(self, stones):
        ids = {}

        for r, c in stones:
            get_id(("r", r), ids)
            get_id(("c", c), ids)

        uf = UnionFind(len(ids))

        for r, c in stones:
            uf.union(ids[("r", r)], ids[("c", c)])

        roots = set()

        for r, c in stones:
            roots.add(uf.find(ids[("r", r)]))

        return len(stones) - len(roots)


# ============================================================
# 9. QUICK COMPARISON: DFS/BFS VS UNION-FIND
# ============================================================

"""
Use DFS/BFS when:
    you need actual traversal
    you need paths/distances
    the graph is already explicit
    you need to inspect structure from a source

Use Union-Find when:
    edges are being added
    you only need connectivity/group membership
    you need to detect undirected cycles while processing edges
    you need to merge equivalent objects
    you need offline connectivity by sorted thresholds

Union-Find does NOT give paths.
It only tells you whether things are in the same component.
"""


