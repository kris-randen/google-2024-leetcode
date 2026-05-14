"""

2077. Paths in Maze That Lead to Same Room
Medium
Topics
Companies
Hint
A maze consists of n rooms numbered from 1 to n, and some rooms are connected by corridors. You are given a 2D integer array corridors where corridors[i] = [room1i, room2i] indicates that there is a corridor connecting room1i and room2i, allowing a person in the maze to go from room1i to room2i and vice versa.

The designer of the maze wants to know how confusing the maze is. The confusion score of the maze is the number of different cycles of length 3.

For example, 1 → 2 → 3 → 1 is a cycle of length 3, but 1 → 2 → 3 → 4 and 1 → 2 → 3 → 2 → 1 are not.
Two cycles are considered to be different if one or more of the rooms visited in the first cycle is not in the second cycle.

Return the confusion score of the maze.



Example 1:


Input: n = 5, corridors = [[1,2],[5,2],[4,1],[2,4],[3,1],[3,4]]
Output: 2
Explanation:
One cycle of length 3 is 4 → 1 → 3 → 4, denoted in red.
Note that this is the same cycle as 3 → 4 → 1 → 3 or 1 → 3 → 4 → 1 because the rooms are the same.
Another cycle of length 3 is 1 → 2 → 4 → 1, denoted in blue.
Thus, there are two different cycles of length 3.
Example 2:


Input: n = 4, corridors = [[1,2],[3,4]]
Output: 0
Explanation:
There are no cycles of length 3.


Constraints:

2 <= n <= 1000
1 <= corridors.length <= 5 * 104
corridors[i].length == 2
1 <= room1i, room2i <= n
room1i != room2i
There are no duplicate corridors.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
4.5K
Submissions
8.1K
Acceptance Rate
55.1%

"""

class UnionFind:
    def __init__(self, n):
        self.id = [None] + [i for i in range(n)]
        self.comps = {i: {i} for i in range(n)}

    @property
    def count(self):
        return len(self.comps)

    def size(self, r):
        return len(self.comps[r])

    def parent(self, i):
        return self.id[i]

    def assign(self, i, p):
        self.id[i] = p

    def is_root(self, i):
        return i == self.parent(i)

    def not_root(self, i):
        return not self.is_root(i)

    def path(self, i):
        p = [i]
        while self.not_root(i):
            i = self.parent(i)
            p += [i]
        return p

    def compress(self, path):
        root = path[-1]
        for p in path: self.assign(p, root)
        return root

    def find(self, i):
        return self.compress(self.path(i))

    def split(self, p, q):
        return (p, q) if self.size(p) > self.size(q) else (q, p)

    def merge(self, s, l):
        self.comps[l].update(self.comps.pop(s))

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if p != q: self.join(p, q)

    def join(self, p, q):
        l, s = self.split(p, q)
        self.assign(s, l)
        self.merge(s, l)


def three_cycles(n, corridors):
    uf = UnionFind(n)
    for u, v in corridors:
        uf.union(u, v)
    count = 0
    for root in uf.comps:
        if len(uf.comps[root]) == 3: count += 1
    return count