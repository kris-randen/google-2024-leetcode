"""

1136. Parallel Courses
Medium

You are given an integer n, which indicates that there are n courses labeled from 1 to n. You are also given an array relations where relations[i] = [prevCoursei, nextCoursei], representing a prerequisite relationship between course prevCoursei and course nextCoursei: course prevCoursei has to be taken before course nextCoursei.

In one semester, you can take any number of courses as long as you have taken all the prerequisites in the previous semester for the courses you are taking.

Return the minimum number of semesters needed to take all courses. If there is no way to take all the courses, return -1.

 

Example 1:


Input: n = 3, relations = [[1,3],[2,3]]
Output: 2
Explanation: The figure above represents the given graph.
In the first semester, you can take courses 1 and 2.
In the second semester, you can take course 3.
Example 2:


Input: n = 3, relations = [[1,2],[2,3],[3,1]]
Output: -1
Explanation: No course can be studied because they are prerequisites of each other.
 

Constraints:

1 <= n <= 5000
1 <= relations.length <= 5000
relations[i].length == 2
1 <= prevCoursei, nextCoursei <= n
prevCoursei != nextCoursei
All the pairs [prevCoursei, nextCoursei] are unique.

Performance


"""


def sems(n, es):
    def cycle(g):
        def dfs(u):
            m[u] = -1
            for v in g[u]:
                if m[v] == 1: continue
                if m[v] == -1: return True
                if dfs(v): return True
            m[u] = 1
            return False

        m = {v: 0 for v in range(1, n + 1)}

        for v in g:
            if m[v] == 1: continue
            if dfs(v): return True

        return False

    def weight(g):
        s, t = 0, n + 1
        dg = {v: set() for v in range(n + 2)}

        for u in range(1, n + 1):
            dg[0].add((u, 0))
            dg[u].add((n + 1, 0))
            for v in g[u]:
                dg[u].add((v, -1))

        return dg

    def order(g):
        def dfs(u):
            m[u] = 1
            for v, _ in g[u]:
                if not m[v]: dfs(v)
            top.appendleft(u)

        top, m = deque(), ([0] * (n := len(g)))
        for v in g:
            if not m[v]: dfs(v)
        
        return list(top)

    def longest(dg, s=0, t=n + 1):
        dist = {v: float('inf') for v in dg}
        dist[s] = 0; top = order(dg)

        for u in top:
            for v, w in dg[u]:
                if dist[v] > (duv := dist[u] + w):
                    dist[v] = duv

        return -dist[t] + 1

    g = {v: set() for v in range(1, n + 1)}
    for u, v in es:
        g[u].add(v)

    return -1 if cycle(g) else longest(weight(g))

class Solution:
    def minimumSemesters(self, n: int, es: List[List[int]]) -> int:
        return sems(n, es)


        























