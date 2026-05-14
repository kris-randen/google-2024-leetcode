"""

1836. Remove Duplicates From an Unsorted Linked List
Medium

Given the head of a linked list, find all the values that appear more than once in the list and delete the nodes that have any of those values.

Return the linked list after the deletions.



Example 1:


Input: head = [1,2,3,2]
Output: [1,3]
Explanation: 2 appears twice in the linked list, so all 2's should be deleted. After deleting all 2's, we are left with [1,3].
Example 2:


Input: head = [2,1,1,2]
Output: []
Explanation: 2 and 1 both appear twice. All the elements should be deleted.
Example 3:


Input: head = [3,2,2,1,3,2,4]
Output: [1,4]
Explanation: 3 appears twice and 2 appears three times. After deleting all 3's and 2's, we are left with [1,4].


Constraints:

The number of nodes in the list is in the range [1, 105]
1 <= Node.val <= 105

Seen this question in a real interview before?
1/6
Yes
No
Accepted
40,080/53K
Acceptance Rate
75.7%

"""
from collections import Counter
from functools import reduce


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def detach_front(a):
    rest = a.next
    a.next = None
    return a, rest

def attach_after(tail, b):
    tail.next = b
    return b

def nodes(a):
    while a:
        next = a.next
        yield a
        a = next

def values(a):
    return (node.val for node in nodes(a))

def duplicates(a):
    vals = values(a)
    counter = Counter(vals)
    return {val for val in counter if counter[val] > 1}

def partition(a):
    dummy = tail = ListNode()
    dupes = duplicates(a)

    while a:
        node, a = detach_front(a)
        if node.val not in dupes:
            tail = attach_after(tail, node)

    return dummy.next

class Solution:
    def deleteDuplicatesUnsorted(self, head: ListNode) -> ListNode:
        return partition(head)
