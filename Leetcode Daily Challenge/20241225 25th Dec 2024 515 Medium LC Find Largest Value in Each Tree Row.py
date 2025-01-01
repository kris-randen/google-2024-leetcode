"""

515. Find Largest Value in Each Tree Row
Medium

Given the root of a binary tree, return an array of the largest value in each row of the tree (0-indexed).

 

Example 1:


Input: root = [1,3,2,5,3,null,9]
Output: [1,3,9]
Example 2:

Input: root = [1,2,3]
Output: [1,3]


Performance

Runtime 0 ms Beats 100.00%
Memory 19.94 MB Beats 6.38%

"""



def levels(root):
    if not root: return []
    front, lvls = [[root]], [[root.val]]
    while front:
        nds, nxt = front.pop(), []
        for nd in nds:
            if (lt := nd.left): nxt.append(lt)
            if (rt := nd.right): nxt.append(rt)
        if nxt: 
            front.append(nxt)
            lvls.append([nd.val for nd in nxt])
    return lvls

def rowmax(root):
    return [max(lvl) for lvl in levels(root)]


















