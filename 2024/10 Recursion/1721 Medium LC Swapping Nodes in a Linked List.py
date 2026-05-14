"""

1721. Swapping Nodes in a Linked List
Medium
Topics
Companies
Hint
You are given the head of a linked list, and an integer k.

Return the head of the linked list after swapping the values of the kth node from the beginning and the kth node from the end (the list is 1-indexed).



Example 1:


Input: head = [1,2,3,4,5], k = 2
Output: [1,4,3,2,5]
Example 2:

Input: head = [7,9,6,6,7,8,3,0,9,5], k = 5
Output: [7,9,6,6,8,7,3,0,9,5]


Constraints:

The number of nodes in the list is n.
1 <= k <= n <= 105
0 <= Node.val <= 100
Seen this question in a real interview before?
1/5
Yes
No
Accepted
347.5K
Submissions
510.8K
Acceptance Rate
68.0%

Runtime 397 ms Beats 31.91%
Memory 50.29 MB Beats 9.09%

"""

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, succ=None):
        self.val = val
        self.next = succ

    def __str__(self):
        return f'val = {self.val}, next = {self.next}'

    def __repr__(self):
        return self.__str__()

def length(node):
    if not node: return 0
    return 1 + length(node.next)

def get_kth(node, k):
    if k == 1 or not node: return node
    return get_kth(node.next, k - 1)

def swap_kth(node, k):
    if not node or not node.next: return node
    kth_front = get_kth(node, k)
    kth_back = get_kth(node, length(node) - k + 1)
    kth_front.val, kth_back.val = kth_back.val, kth_front.val
    return node

def list_to_linked(vs):
    if not vs: return None
    node = ListNode(vs[0])
    node.next = list_to_linked(vs[1:])
    return node

if __name__ == '__main__':
    vs = [1, 2, 3, 4, 5]
    head = list_to_linked(vs)
    print(f'head = {head}')
    chead = copy(head)
    print(f'chead = {chead}')
    rhead = reverse(chead)
    print(f'rhead = {rhead}')
    third = get_kth(head, 3)
    print(third)