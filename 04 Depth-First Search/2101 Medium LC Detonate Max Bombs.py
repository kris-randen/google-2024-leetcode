"""

2101. Detonate the Maximum Bombs
Medium
Topics
Companies
Hint
You are given a list of bombs. The range of a bomb is defined as the area where its effect can be felt. This area is in the shape of a circle with the center as the location of the bomb.

The bombs are represented by a 0-indexed 2D integer array bombs where bombs[i] = [xi, yi, ri]. xi and yi denote the X-coordinate and Y-coordinate of the location of the ith bomb, whereas ri denotes the radius of its range.

You may choose to detonate a single bomb. When a bomb is detonated, it will detonate all bombs that lie in its range. These bombs will further detonate the bombs that lie in their ranges.

Given the list of bombs, return the maximum number of bombs that can be detonated if you are allowed to detonate only one bomb.



Example 1:


Input: bombs = [[2,1,3],[6,1,4]]
Output: 2
Explanation:
The above figure shows the positions and ranges of the 2 bombs.
If we detonate the left bomb, the right bomb will not be affected.
But if we detonate the right bomb, both bombs will be detonated.
So the maximum bombs that can be detonated is max(1, 2) = 2.
Example 2:


Input: bombs = [[1,1,5],[10,10,5]]
Output: 1
Explanation:
Detonating either bomb will not detonate the other bomb, so the maximum number of bombs that can be detonated is 1.
Example 3:


Input: bombs = [[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]]
Output: 5
Explanation:
The best bomb to detonate is bomb 0 because:
- Bomb 0 detonates bombs 1 and 2. The red circle denotes the range of bomb 0.
- Bomb 2 detonates bomb 3. The blue circle denotes the range of bomb 2.
- Bomb 3 detonates bomb 4. The green circle denotes the range of bomb 3.
Thus all 5 bombs are detonated.


Constraints:

1 <= bombs.length <= 100
bombs[i].length == 3
1 <= xi, yi, ri <= 105
Seen this question in a real interview before?
1/5
Yes
No
Accepted
124.1K
Submissions
254.8K
Acceptance Rate
48.7%



"""

import math


class UnionFind:
    def __init__(self, n):
        self.id = [i for i in range(n)];
        self.max = 1
        self.comps = {i: {i} for i in range(n)}

    @property
    def count(self):
        return len(self.comps)

    def size(self, p):
        return len(self.comps[p])

    def is_greater(self, p, q):
        return self.size(p) > self.size(q)

    def parent(self, i):
        return self.id[i]

    def assign(self, i, p):
        self.id[i] = p

    def is_root(self, i):
        return i == self.parent(i)

    def is_not_root(self, i):
        return not self.is_root(i)

    def merge(self, s, l):
        self.comps[l].update(self.comps.pop(s))

    def path(self, i):
        p = [i]
        while self.is_not_root(i):
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
        return (p, q) if self.is_greater(p, q) else (q, p)

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if not p == q: self.join(p, q)

    def join(self, p, q):
        l, s = self.split(p, q)
        self.assign(s, l)
        self.merge(s, l)
        self.max = max(self.max, self.size(l))


def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))


def check_radius(b1, b2, e=1e-5):
    x1, y1, r1 = b1
    x2, y2, r2 = b2
    return distance(x1, y1, x2, y2) <= (r1 + e)


def connect(bombs):
    connected = []; n = len(bombs)
    for i in range(n):
        for j in range(i + 1, n):
            if check_radius(bombs[i], bombs[j]):
                connected.append((i, j))
    return connected


def max_detonate(bombs):
    bombs = sorted(bombs, key=lambda x: x[2], reverse=True)
    n = len(bombs)
    uf = UnionFind(n)
    edges = connect(bombs)
    for u, v in edges:
        uf.union(u, v)
    return uf.max