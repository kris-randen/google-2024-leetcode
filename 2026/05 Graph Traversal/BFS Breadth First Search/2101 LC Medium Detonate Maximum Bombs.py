"""

2101. Detonate the Maximum Bombs
Solved
Medium

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

"""

from math import sqrt
from typing import List, Counter


def graph(n: int, edges: List[tuple[int, int]]) -> List[List[int]]:
    g = [[] for _ in range(n)]

    for u, v in edges:
        g[u].append(v)

    return g

def reachable(g: List[List[int]], src: int) -> int:
    seen = [False] * len(g)

    def dfs(v: int):
        seen[v] = True
        for w in g[v]:
            if not seen[w]:
                dfs(w)

    dfs(src)
    reach = sum(seen)
    return reach

class Graph:
    def __init__(
            self,
            n: int,
            edges: List[tuple[int, int]],
            g: List[List[int]]
    ):
        self.n = n
        self.edges = edges
        self.g = g

def dist(p, q):
    xp, yp, _ = p
    xq, yq, _ = q

    return sqrt((abs(xp - xq) ** 2) + (abs(yp - yq) ** 2))

def in_range(a, b):
    return dist(a, b) <= a[2]

def map_bombs(bombs: List[List[int]]):
    n = len(bombs)
    edges = []

    for i in range(n):
        for j in range(n):
            if not i == j and in_range(bombs[i], bombs[j]):
                edges.append((i, j))

    g = graph(n, edges)
    return Graph(
        n,
        edges,
        g
    )

class Solution:
    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        bomb_map = map_bombs(bombs)
        return max(reachable(bomb_map.g, v) for v in range(len(bombs)))