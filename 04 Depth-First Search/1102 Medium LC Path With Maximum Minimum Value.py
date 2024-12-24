"""

1102. Path With Maximum Minimum Value
Medium
Topics
Companies
Hint
Given an m x n integer matrix grid, return the maximum score of a path starting at (0, 0) and ending at (m - 1, n - 1) moving in the 4 cardinal directions.

The score of a path is the minimum value in that path.

For example, the score of the path 8 → 4 → 5 → 9 is 4.
 

Example 1:


Input: grid = [[5,4,5],[1,2,6],[7,4,6]]
Output: 4
Explanation: The path with the maximum score is highlighted in yellow. 
Example 2:


Input: grid = [[2,2,1,2,2,2],[1,2,2,2,1,2]]
Output: 2
Example 3:


Input: grid = [[3,4,6,3,4],[0,2,1,1,7],[8,8,3,2,7],[3,2,4,9,8],[4,1,2,0,0],[4,6,5,4,3]]
Output: 3
 

Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 100
0 <= grid[i][j] <= 109

"""




def maxmin(bd, ps, pt):
    def flat(p):        return p[0] * n + p[1]
    def unflat(v):      return v // n, v % n
    def valid(p):       return 0 <= p[0] < m and 0 <= p[1] < n
    def up(p):          return p[0] - 1, p[1]
    def dn(p):          return p[0] + 1, p[1]
    def lt(p):          return p[0], p[1] - 1
    def rt(p):          return p[0], p[1] + 1
    def adj(p):         return up(p), dn(p), lt(p), rt(p)
    def nbs(p):         return (q for q in adj(p) if valid(q))
    def fbs(v):         return [flat(q) for q in nbs(unflat(v))]
    def graph():        return [fbs(v) for v in range(m * n)]

    def scores(u, t):
        if u == t: return [val(t)]
        visited[u] = True
        for v in g.adj[u]:
            if not visited[v]:
                sc += scores(v, t)
        return [min(val(u), d) for d in sc]

    g = graph()
    m, n = len(bd), len(bd[0])
    s, t = flat(ps), flat(pt)
    return max(scores(s, t))




















