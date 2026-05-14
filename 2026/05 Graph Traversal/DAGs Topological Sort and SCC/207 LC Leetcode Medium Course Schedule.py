"""

207. Course Schedule
Solved
Medium

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return true if you can finish all courses. Otherwise, return false.



Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0. So it is possible.
Example 2:

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.


Constraints:

1 <= numCourses <= 2000
0 <= prerequisites.length <= 5000
prerequisites[i].length == 2
0 <= ai, bi < numCourses
All the pairs prerequisites[i] are unique.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
2,600,584/5.1M
Acceptance Rate
51.4%

"""

from collections import defaultdict
from typing import List

Graph = List[List[int]]

def graph(V: int, edges: tuple[int, int]):
    g = defaultdict(list)

    for u, v in reversed(edges):
        g[u].append(v)

    return g

UNSEEN   = 0
VISITING = 1
SEEN     = 2

def has_cycle(g: Graph) -> bool:
    state = [UNSEEN] * len(g)

    def dfs(u) -> bool:
        state[u] = VISITING

        for v in g[u]:
            if state[v] == VISITING:
                return True

            if state[v] == UNSEEN and dfs(v):
                return True

        state[u] = SEEN

        return False

    return any(dfs(v) for v in g if state[v] == UNSEEN)



class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        return not has_cycle(graph(numCourses, prerequisites))