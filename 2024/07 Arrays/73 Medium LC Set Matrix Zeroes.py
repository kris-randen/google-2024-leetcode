"""

73. Set Matrix Zeroes
Solved
Medium
Topics
Companies
Hint
Given an m x n integer matrix matrix, if an element is 0, set its entire row and column to 0's.

You must do it in place.



Example 1:


Input: matrix = [[1,1,1],[1,0,1],[1,1,1]]
Output: [[1,0,1],[0,0,0],[1,0,1]]
Example 2:


Input: matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]


Constraints:

m == matrix.length
n == matrix[0].length
1 <= m, n <= 200
-231 <= matrix[i][j] <= 231 - 1


Follow up:

A straightforward solution using O(mn) space is probably a bad idea.
A simple improvement uses O(m + n) space, but still not the best solution.
Could you devise a constant space solution?
Seen this question in a real interview before?
1/5
Yes
No
Accepted
1.5M
Submissions
2.7M
Acceptance Rate
56.8%

Runtime 96 ms Beats 88.21%
Memory 17.34 MB Beats 84.32%


"""

def zero_rows(rows, n, grid):
    for row in rows: grid[row] = [0] * n

def zero_cols(cols, m, grid):
    for col in cols:
        for i in range(m): grid[i][col] = 0

def zero(rows, cols, m, n, grid):
    zero_rows(rows, n, grid)
    zero_cols(cols, m, grid)

def column(j, grid):
    return map(lambda row: row[j], grid)

def get_zeroes(m, n, grid):
    rows = [row for row in range(m) if not all(grid[row])]
    cols = [col for col in range(n) if not all(column(col, grid))]
    return rows, cols

def set_zeroes(grid):
    m, n = len(grid), len(grid[0])
    rows, cols = get_zeroes(m, n, grid)
    zero(rows, cols, m, n, grid)