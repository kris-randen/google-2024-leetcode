"""

113. Path Sum II
Medium
Topics
Companies
Given the root of a binary tree and an integer targetSum, return all root-to-leaf paths where the sum of the node values in the path equals targetSum. Each path should be returned as a list of the node values, not node references.

A root-to-leaf path is a path starting from the root and ending at any leaf node. A leaf is a node with no children.



Example 1:


Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
Output: [[5,4,11,2],[5,8,4,5]]
Explanation: There are two paths whose sum equals targetSum:
5 + 4 + 11 + 2 = 22
5 + 8 + 4 + 5 = 22
Example 2:


Input: root = [1,2,3], targetSum = 5
Output: []
Example 3:

Input: root = [1,2], targetSum = 0
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 5000].
-1000 <= Node.val <= 1000
-1000 <= targetSum <= 1000
Seen this question in a real interview before?
1/5
Yes
No
Accepted
879K
Submissions

"""

"""
Solution Strategy

At each node inherit prefix path and a target sum = s.

Possible scenarios:

1. The Node (val = p) is a leaf (has no children)
  a. p == s. Then success: we return prefix + [p]
  b. p != s. The failure: we return None
  This ends up being the base case.
  
2. The Node is not a leaf:
  a. 


Don't inherit a path sum prefix. Instead collect the path while
returning from a successful path.

Now each child will return a list of suffix paths. Prefix the
node value to each suffix path and return.

0. So in the base case where node is None
a. If s == 0 return [[]]
b. If s != 0 return []

1. When not None:
   l_ps = path_sum(node.left)
   r_ps = path_sum(node.right)
   
   nps = []
   for path in l_ps + r_ps:
     nps.append([p] + path)
     
   return nps
   
"""

class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def leaf(node):
    return not node.left and not node.right

def path_sum(node, t):
    if not node: return []
    if leaf(node): return [[t]] if t == node.val else []
    left = path_sum(node.left, t - node.val)
    right = path_sum(node.right, t - node.val)
    return list(map(lambda path: [node.val] + path, left + right))

if __name__ == '__main__':
    vs = [2, 3, 5]
    print(vs + [])
    print("-".join(["2", ""]))
