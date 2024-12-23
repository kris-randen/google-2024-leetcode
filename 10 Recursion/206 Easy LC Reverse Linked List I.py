"""

206. Reverse Linked List
Easy

Given the head of a singly linked list, reverse the list, and return the reversed list.



Example 1:


Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]
Example 2:


Input: head = [1,2]
Output: [2,1]
Example 3:

Input: head = []
Output: []

"""

class ListNode:
    def __init__(self, val=0, node=None):
        self.val = val
        self.next = node

def reverse(node):
    if not node or not node.next: return node, node
    head, toe = reverse(node.next)
    toe.next = node
    return head, node

