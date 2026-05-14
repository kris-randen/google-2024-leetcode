"""

3217. Delete Nodes From Linked List Present in Array
Medium

You are given an array of integers nums and the head of a linked list. Return the head of the modified linked list after removing all nodes from the linked list that have a value that exists in nums.



Example 1:

Input: nums = [1,2,3], head = [1,2,3,4,5]

Output: [4,5]

Explanation:



Remove the nodes with values 1, 2, and 3.

Example 2:

Input: nums = [1], head = [1,2,1,2,1,2]

Output: [2,2,2]

Explanation:



Remove the nodes with value 1.

Example 3:

Input: nums = [5], head = [1,2,3,4]

Output: [1,2,3,4]

Explanation:



No node has value 5.



Constraints:

1 <= nums.length <= 105
1 <= nums[i] <= 105
All elements in nums are unique.
The number of nodes in the given list is in the range [1, 105].
1 <= Node.val <= 105
The input is generated such that there is at least one node in the linked list that has a value not present in nums.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
339,154/488.4K
Acceptance Rate
69.4%

"""
from typing import List, Optional


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

def partition_by_predicate(a, pred):
    dummy = tail = ListNode()

    while a:
        node, a = detach_front(a)
        if pred(node):
            tail = attach_after(tail, node)

    return dummy.next


class Solution:
    def modifiedList(self, nums: List[int], head: Optional[ListNode]) -> Optional[ListNode]:
        seen = set(nums)
        return partition_by_predicate(head, lambda a: a.val not in seen)
