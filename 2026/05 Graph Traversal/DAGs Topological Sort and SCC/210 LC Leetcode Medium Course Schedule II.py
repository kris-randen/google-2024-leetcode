"""

210. Course Schedule II
Solved
Medium

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.



Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0. So the correct course order is [0,1].
Example 2:

Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,2,1,3]
Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].
Example 3:

Input: numCourses = 1, prerequisites = []
Output: [0]


Constraints:

1 <= numCourses <= 2000
0 <= prerequisites.length <= numCourses * (numCourses - 1)
prerequisites[i].length == 2
0 <= ai, bi < numCourses
ai != bi
All the pairs [ai, bi] are distinct.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,712,906/3.1M
Acceptance Rate
55.5%

"""

from collections import deque
from typing import List, DefaultDict

def graph(V: int, edges: List[tuple[int, int]]):
    g = {v: [] for v in range(V)}

    for course, pre in edges:
        g[pre].append(course)

    return g

UNSEEN = 0
VISITING = 1
DONE = 2

def has_cycle(g):
    state = [UNSEEN] * len(g)

    def dfs(u) -> bool:
        state[u] = VISITING

        for v in g[u]:
            if state[v] == VISITING:
                return True

            if state[v] == UNSEEN and dfs(v):
                return True

        state[u] = DONE
        return False

    return any(dfs(v) for v in g if state[v] == UNSEEN)

def topological_sort(g):
    postorder = deque()
    seen = set()

    def dfs(u):
        seen.add(u)

        for v in g[u]:
            if v not in seen:
                dfs(v)

        postorder.append(u)

    for v in g:
        if v not in seen:
            dfs(v)

    return reversed(postorder)

def topological_sort_or_empty(g):
    state = [UNSEEN] * len(g)
    postorder = deque()

    def dfs(u) -> bool:
        state[u] = VISITING

        for v in g[u]:
            if state[v] == VISITING:
                return True

            if state[v] == UNSEEN and dfs(v):
                return True

        state[u] = DONE
        postorder.append(u)
        return False

    for v in g:
        if state[v] == UNSEEN and dfs(v):
            return []

    return reversed(postorder)


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        return list(topological_sort_or_empty(graph(numCourses, prerequisites)))