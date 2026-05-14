"""

2674. Split a Circular Linked List
Medium
Topics
Hint
Given a circular linked list list of positive integers, your task is to split it into 2 circular linked lists so that the first one contains the first half of the nodes in list (exactly ceil(list.length / 2) nodes) in the same order they appeared in list, and the second one contains the rest of the nodes in list in the same order they appeared in list.

Return an array answer of length 2 in which the first element is a circular linked list representing the first half and the second element is a circular linked list representing the second half.

A circular linked list is a normal linked list with the only difference being that the last node's next node, is the first node.


Example 1:

Input: nums = [1,5,7]
Output: [[1,5],[7]]
Explanation: The initial list has 3 nodes so the first half would be the first 2 elements since ceil(3 / 2) = 2 and the rest which is 1 node is in the second half.
Example 2:

Input: nums = [2,6,1,5]
Output: [[2,6],[1,5]]
Explanation: The initial list has 4 nodes so the first half would be the first 2 elements since ceil(4 / 2) = 2 and the rest which is 2 nodes are in the second half.


Constraints:

The number of nodes in list is in the range [2, 105]
0 <= Node.val <= 109
LastNode.next = FirstNode where LastNode is the last node of the list and FirstNode is the first one

Seen this question in a real interview before?
1/6
Yes
No
Accepted
3,372/4.3K
Acceptance Rate
77.6%

"""
from typing import Optional, List


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def nodes(head):
    while head:
        nxt = head.next
        yield head
        head = nxt

def cut(head):
    curr = head.next
    while not curr.next == head:
        curr = curr.next
    curr.next = None

def middle(head):
    slow, fast = head, head.next

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    right = slow.next
    slow.next = None

    return head, right

def get_tail(head):
    tail = None
    for node in nodes(head):
        tail = node
    return tail

def close(head):
    tail = get_tail(head)
    tail.next = head
    return head


class Solution:
    def splitCircularLinkedList(self, head: Optional[ListNode]) -> List[Optional[ListNode]]:
        cut(head)
        left, right = middle(head)
        return [close(left), close(right)]
