"""

24. Swap Nodes in Pairs
Solved
Medium
Topics
Companies
Given a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)


Example 1:


Input: head = [1,2,3,4]
Output: [2,1,4,3]
Example 2:

Input: head = []
Output: []
Example 3:

Input: head = [1]
Output: [1]


Constraints:

The number of nodes in the list is in the range [0, 100].
0 <= Node.val <= 100
Seen this question in a real interview before?
1/5
Yes
No
Accepted
1.4M
Submissions
2.2M
Acceptance Rate
65.0%

Runtime 30 ms Beats 87.85%
Memory 16.50 MB Beats 17.64%

"""

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, succ=None):
        self.val = val
        self.next = succ

def swap(node):
    if not node or not node.next: return node
    succ = node.next
    succsucc = succ.next
    succ.next = node
    node.next = swap(succsucc)
    return succ

if __name__ == '__main__':
    vs = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    t = 30
    print(len(vs))
    print(sum(vs))