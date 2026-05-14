
"""
Yes. The clean way to rebuild the arsenal is as a **layered toolkit**:

```text
Level 0: testing/traversal primitives
Level 1: pointer atoms
Level 2: navigation primitives
Level 3: transformation primitives
Level 4: full problem recipes
```

The important correction from our discussion is this:

```text
middle is not one primitive.
There are at least two useful middle primitives:

left_middle  -> useful for splitting/cutting
right_middle -> useful for LeetCode “middle of list” behavior
```

---

# Level 0 — Testing / Traversal Primitives


```python

from functools import reduce
from typing import Callable, Iterable, Iterator, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

    def __iter__(self) -> Iterator["ListNode"]:
        node = self

        while node is not None:
            nxt = node.next      # save before yielding, safe for mutation
            yield node
            node = nxt
```

```python
def nodes(head: Optional[ListNode]) -> Iterator[ListNode]:
    return iter(head) if head else iter(())


def values(head: Optional[ListNode]) -> Iterator[int]:
    return (node.val for node in nodes(head))


def unlink(head: Optional[ListNode]) -> list[int]:
    return list(values(head))
```

For building linked lists:

```python
def chain_nodes(ns: Iterable[ListNode]) -> Optional[ListNode]:
    it = iter(ns)
    head = next(it, None)

    if head is None:
        return None

    def connect(prev: ListNode, curr: ListNode) -> ListNode:
        prev.next = curr
        return curr

    tail = reduce(connect, it, head)
    tail.next = None

    return head


def link(vs: Iterable[int]) -> Optional[ListNode]:
    return chain_nodes(ListNode(v) for v in vs)
```

These are mainly for testing and construction.

---

# Level 1 — Pointer Atoms

These are the real “lego bricks.”

```python
def detach_front(head: ListNode) -> tuple[ListNode, Optional[ListNode]]:
    rest = head.next
    head.next = None
    return head, rest
```

```python
def append_after(tail: ListNode, node: ListNode) -> ListNode:
    tail.next = node
    return node
```

```python
def delete_after(prev: ListNode) -> Optional[ListNode]:
    target = prev.next

    if target is None:
        return None

    prev.next = target.next
    target.next = None

    return target
```

```python
def cut_after(prev: ListNode) -> Optional[ListNode]:
    right = prev.next
    prev.next = None
    return right
```

These four cover most linked-list pointer surgery:

```text
detach
append
delete
cut
```

---

# Level 2 — Navigation Primitives

## 1. Length

```python
def length(head: Optional[ListNode]) -> int:
    return sum(1 for _ in nodes(head))
```

## 2. Tail

```python
def tail(head: Optional[ListNode]) -> Optional[ListNode]:
    last = None

    for node in nodes(head):
        last = node

    return last
```

## 3. Advance by k

```python
def advance(node: Optional[ListNode], k: int) -> Optional[ListNode]:
    for _ in range(k):
        if node is None:
            return None
        node = node.next

    return node
```

## 4. Left Middle

Useful for splitting.

```python
def left_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    if head is None:
        return None

    slow = head
    fast = head.next

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow
```

## 5. Right Middle

Useful for LeetCode 876-style middle.

```python
def right_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow
```

Behavior:

```text
[1]             left = 1, right = 1
[1, 2]          left = 1, right = 2
[1, 2, 3]       left = 2, right = 2
[1, 2, 3, 4]    left = 2, right = 3
[1, 2, 3, 4, 5] left = 3, right = 3
```

---

# Level 3 — Transformation Primitives

## 1. Reverse Whole List

```python
def reverse(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None

    for node in nodes(head):
        node.next = prev
        prev = node

    return prev
```

Used by:

```text
206. Reverse Linked List
234. Palindrome Linked List
143. Reorder List
2130. Maximum Twin Sum
2487. Remove Nodes From Linked List
2816. Double Number Represented as Linked List
```

---

## 2. Reverse Prefix

This is more powerful than `reverse`.

```python
def reverse_prefix(
    head: ListNode,
    k: int
) -> tuple[ListNode, ListNode, Optional[ListNode]]:
    prev = None
    curr = head
    tail = head

    for _ in range(k):
        if curr is None:
            raise ValueError("List has fewer than k nodes.")

        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    return prev, tail, curr
```

It returns:

```text
rev_head -> new head of reversed block
rev_tail -> old head, now tail of reversed block
after    -> node after the reversed block
```

This powers:

```text
92. Reverse Linked List II
24. Swap Nodes in Pairs
25. Reverse Nodes in k-Group
2074. Reverse Nodes in Even Length Groups
```

---

## 3. Split at Middle

Now this properly composes with `left_middle`.

```python
def split(head: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    if head is None or head.next is None:
        return head, None

    cut = left_middle(head)
    right = cut_after(cut)

    return head, right
```

Examples:

```text
[1, 2, 3, 4]    -> [1, 2], [3, 4]
[1, 2, 3, 4, 5] -> [1, 2, 3], [4, 5]
```

Used by:

```text
143. Reorder List
148. Sort List
234. Palindrome Linked List
2130. Maximum Twin Sum
109. Sorted List to BST
```

---

## 4. Merge Sorted Lists

```python
def merge_sorted(
    a: Optional[ListNode],
    b: Optional[ListNode]
) -> Optional[ListNode]:
    dummy = tail = ListNode()

    while a and b:
        if a.val <= b.val:
            node, a = detach_front(a)
        else:
            node, b = detach_front(b)

        tail = append_after(tail, node)

    tail.next = a or b

    return dummy.next
```

Used by:

```text
21. Merge Two Sorted Lists
23. Merge k Sorted Lists
148. Sort List
```

---

## 5. Weave Two Lists

```python
def weave(
    a: Optional[ListNode],
    b: Optional[ListNode]
) -> Optional[ListNode]:
    dummy = tail = ListNode()

    while a or b:
        if a:
            node, a = detach_front(a)
            tail = append_after(tail, node)

        if b:
            node, b = detach_front(b)
            tail = append_after(tail, node)

    return dummy.next
```

Used by:

```text
143. Reorder List
```

Pattern:

```text
L0 -> L1 -> L2 -> L3
R0 -> R1 -> R2

weave = L0 -> R0 -> L1 -> R1 -> L2 -> R2 -> L3
```

---

## 6. Partition by Predicate

```python
def partition_by(
    head: Optional[ListNode],
    pred: Callable[[ListNode], bool]
) -> tuple[Optional[ListNode], Optional[ListNode]]:
    true_dummy = true_tail = ListNode()
    false_dummy = false_tail = ListNode()

    while head:
        node, head = detach_front(head)

        if pred(node):
            true_tail = append_after(true_tail, node)
        else:
            false_tail = append_after(false_tail, node)

    return true_dummy.next, false_dummy.next
```

For LeetCode 86:

```python
def partition(head: Optional[ListNode], x: int) -> Optional[ListNode]:
    less, greater_equal = partition_by(head, lambda node: node.val < x)

    if less is None:
        return greater_equal

    tail(less).next = greater_equal
    return less
```

Used by:

```text
86. Partition List
328. Odd Even Linked List
1836. Remove Duplicates From Unsorted List
3217. Delete Nodes Present in Array
```

---

# Level 4 — Complete Solution Recipes

Now the main point: these primitives compose into full solutions.

---

## Recipe 1 — Reverse List

```python
def solve_reverse_list(head):
    return reverse(head)
```

Problems:

```text
206. Reverse Linked List
```

---

## Recipe 2 — Middle of List

```python
def solve_middle_of_list(head):
    return right_middle(head)
```

Problems:

```text
876. Middle of the Linked List
```

---

## Recipe 3 — Remove Nth From End

Composition:

```text
dummy + gap pointer + delete_after
```

```python
def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    dummy = ListNode(0, head)

    left = dummy
    right = dummy

    for _ in range(n + 1):
        right = right.next

    while right:
        left = left.next
        right = right.next

    delete_after(left)

    return dummy.next
```

Problems:

```text
19. Remove Nth Node From End of List
```

---

## Recipe 4 — Split List

Composition:

```text
left_middle + cut_after
```

```python
def solve_split(head):
    return split(head)
```

Problems:

```text
725. Split Linked List in Parts
148. Sort List
143. Reorder List
234. Palindrome Linked List
2130. Maximum Twin Sum
```

---

## Recipe 5 — Merge Two Sorted Lists

Composition:

```text
detach_front + append_after + dummy tail builder
```

```python
def solve_merge_two_sorted_lists(a, b):
    return merge_sorted(a, b)
```

Problems:

```text
21. Merge Two Sorted Lists
23. Merge k Sorted Lists
148. Sort List
```

---

## Recipe 6 — Reverse Between

Composition:

```text
dummy + advance to before-left + reverse_prefix + reconnect
```

```python
def reverse_between(
    head: Optional[ListNode],
    left: int,
    right: int
) -> Optional[ListNode]:
    if head is None or left == right:
        return head

    dummy = ListNode(0, head)
    before = advance(dummy, left - 1)

    rev_head, rev_tail, after = reverse_prefix(
        before.next,
        right - left + 1
    )

    before.next = rev_head
    rev_tail.next = after

    return dummy.next
```

Problems:

```text
92. Reverse Linked List II
```

Also useful for:

```text
25. Reverse Nodes in k-Group
2074. Reverse Nodes in Even Length Groups
```

---

## Recipe 7 — Reverse K Group

Composition:

```text
has_k_nodes + reverse_prefix + reconnect
```

```python
def has_k_nodes(head: Optional[ListNode], k: int) -> bool:
    return advance(head, k - 1) is not None
```

```python
def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if k <= 1:
        return head

    dummy = ListNode(0, head)
    group_prev = dummy

    while has_k_nodes(group_prev.next, k):
        start = group_prev.next

        rev_head, rev_tail, after = reverse_prefix(start, k)

        group_prev.next = rev_head
        rev_tail.next = after

        group_prev = rev_tail

    return dummy.next
```

Problems:

```text
24. Swap Nodes in Pairs        # k = 2 version
25. Reverse Nodes in k-Group
2074. Reverse Nodes in Even Length Groups
```

---

## Recipe 8 — Partition List

Composition:

```text
partition_by + concatenate buckets
```

```python
def partition_list(head: Optional[ListNode], x: int) -> Optional[ListNode]:
    less, greater_equal = partition_by(head, lambda node: node.val < x)

    if less is None:
        return greater_equal

    tail(less).next = greater_equal
    return less
```

Problems:

```text
86. Partition List
328. Odd Even Linked List
```

---

## Recipe 9 — Reorder List

Composition:

```text
split + reverse second half + weave
```

```python
def reorder_list(head: Optional[ListNode]) -> Optional[ListNode]:
    if head is None or head.next is None:
        return head

    left, right = split(head)
    right = reverse(right)

    return weave(left, right)
```

Problems:

```text
143. Reorder List
```

Same skeleton also helps:

```text
234. Palindrome Linked List
2130. Maximum Twin Sum
```

For twin sum:

```python
def pairwise_twin_sum(head: Optional[ListNode]) -> int:
    left, right = split(head)
    right = reverse(right)

    best = 0

    while right:
        best = max(best, left.val + right.val)
        left = left.next
        right = right.next

    return best
```

---

## Recipe 10 — Merge Sort List

Composition:

```text
split + recursively sort halves + merge_sorted
```

```python
def sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
    if head is None or head.next is None:
        return head

    left, right = split(head)

    return merge_sorted(
        sort_list(left),
        sort_list(right)
    )
```

Problems:

```text
148. Sort List
```

This is one of the cleanest examples where primitives compose beautifully.

---

# Problem Family Map

| Family             | Composition                            | Problems                    |
| ------------------ | -------------------------------------- | --------------------------- |
| Basic reversal     | `reverse`                              | 206                         |
| Segment reversal   | `advance + reverse_prefix + reconnect` | 92, 24, 25, 2074            |
| Deletion           | `dummy + prev + delete_after`          | 19, 82, 83, 203, 2095, 3217 |
| Splitting          | `left_middle + cut_after`              | 143, 148, 234, 2130         |
| Merge sorted       | `detach_front + append_after`          | 21, 23, 148                 |
| Reorder/weave      | `split + reverse + weave`              | 143                         |
| Palindrome/twin    | `split + reverse + compare`            | 234, 2130                   |
| Partitioning       | `partition_by + concatenate`           | 86, 328                     |
| Arithmetic         | `reverse/stack + carry + dummy`        | 2, 369, 445, 2816           |
| Hash-based         | `map/set + pointer surgery`            | 138, 817, 1171, 1836, 3217  |
| Cycle/intersection | `fast/slow or two-pointer sync`        | 141, 142, 160               |
| Design structures  | `hash map + doubly linked list`        | 146, 460, 432, 716, 2296    |

---

# Highest-Utility Practice Order

I would practice in this order:

```text
1. reverse
2. left_middle / right_middle
3. split
4. delete_after with dummy
5. remove_nth_from_end
6. reverse_prefix
7. reverse_between
8. reverse_k_group
9. merge_sorted
10. split + merge sort
11. split + reverse + weave
12. partition_by
```

This gives you the fastest path to solving most linked-list mediums.

The key meta-pattern is:

```text
Do not memorize full solutions.

Memorize these transformations:

find cut point
cut
reverse block
delete after prev
detach front
append to tail
merge
weave
partition into buckets
reconnect
```

Most linked-list problems are just different compositions of those moves.

"""
from functools import reduce
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __iter__(self):
        node = self

        while node:
            nxt = node.nxt
            yield node
            node = nxt

# Level 0 | Testing and Traversal Primitives

def nodes(head):
    return iter(head) if head else iter(())

def values(head):
    return (node.val for node in nodes(head))

def unlink(head):
    return list(values(head))

def cons(node, nxt):
    node.next = nxt
    return node

def chain(ns):
    return reduce(
        lambda nxt, node: cons(node, nxt),
        reversed(ns),
        None
    )

def link(vs):
    return chain((ListNode(v) for v in vs))


# Level 1 | Pointer Atoms

def detach_front(head):
    rest = head.next
    head.next = None
    return head, rest

def attach_after(tail, node):
    tail.next = node
    return node

def delete_after(prev):
    target = prev.next

    if target is None:
        return target

    prev.next = target.next
    target.next = None

    return target

def cut_after(prev):
    rest = prev.next
    prev.next = None
    return rest


# Level 2 | Navigational Primitives

def length(head):
    return sum(1 for _ in nodes(head))

def tail(head):
    last = None

    for node in nodes(head):
        last = node

    return last

def advance_by_k(head, k):
    node = head

    for _ in range(k):
        if node is None:
            return None
        node = node.next

    return node


def left_middle(head):
    if head is None:
        return None

    slow, fast = head, head.next

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow

def right_middle(head):
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow

# Iterative using nodes
def reverse(head):
    prev, curr = None, head

    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    return prev

# def reverse_prefix(head, k):
#     prev, curr, tail = None, head, head
#
#     for _ in range(k):
#         if curr is None:
#             raise ValueError("List has less than k nodes")
#
#         nxt = curr.next
#         curr.next = prev
#         prev = curr
#         curr = nxt
#
#     return prev, tail, curr

def reverse_rec(head):
    def rec(node):
        if node is None or node.next is None: return node, node

        new_head, new_tail = rec(node.next)
        new_tail.next = node
        node.next = None

        return new_head, node

    return rec(head)[0]


def weave(a, b):
    dummy = tail = ListNode()

    while a or b:
        if a:
            node, a = detach_front(a)
            tail = attach_after(tail, node)
        if b:
            node, b = detach_front(b)
            tail = attach_after(tail, node)

    return dummy.next


def merge_sorted(a, b):
    dummy = tail = ListNode()

    while a and b:
        if a.val <= b.val:
            node, a = detach_front(a)
        else:
            node, b = detach_front(b)
        tail = attach_after(tail, node)

    tail.next = a or b
    return dummy.next


def partition_by_predicate(a, pred):
    true_dummy = true_tail = ListNode()
    false_dummy = false_tail = ListNode()

    while a:
        node, a = detach_front(a)
        if pred(node):
            true_tail = attach_after(true_tail, node)
        else:
            false_tail = attach_after(false_tail, node)

    return true_dummy.next, true_tail, false_dummy.next, false_tail

def partition(a, x):
    less, tail_less, greater, tail_greater = partition_by_predicate(a, lambda a: a.val < x)

    if less is None:
       return greater

    tail_less.next = greater
    return less


def delete_nth(a, n):
    dummy = left = right = ListNode(0, a)

    for _ in range(n + 1):
        right = right.next

    while right:
        left = left.next
        right = right.next

    delete_after(left)
    return dummy.next


"""

## Recipe 6 — Reverse Between

Composition:

```text
dummy + advance to before-left + reverse_prefix + reconnect
```

```python
def reverse_between(
    head: Optional[ListNode],
    left: int,
    right: int
) -> Optional[ListNode]:
    if head is None or left == right:
        return head

    dummy = ListNode(0, head)
    before = advance(dummy, left - 1)

    rev_head, rev_tail, after = reverse_prefix(
        before.next,
        right - left + 1
    )

    before.next = rev_head
    rev_tail.next = after

    return dummy.next
```

Problems:

```text
92. Reverse Linked List II
```

Also useful for:

```text
25. Reverse Nodes in k-Group
2074. Reverse Nodes in Even Length Groups
```

---

## Recipe 7 — Reverse K Group

Composition:

```text
has_k_nodes + reverse_prefix + reconnect
```

```python
def has_k_nodes(head: Optional[ListNode], k: int) -> bool:
    return advance(head, k - 1) is not None
```

```python
def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if k <= 1:
        return head

    dummy = ListNode(0, head)
    group_prev = dummy

    while has_k_nodes(group_prev.next, k):
        start = group_prev.next

        rev_head, rev_tail, after = reverse_prefix(start, k)

        group_prev.next = rev_head
        rev_tail.next = after

        group_prev = rev_tail

    return dummy.next
```

Problems:

```text
24. Swap Nodes in Pairs        # k = 2 version
25. Reverse Nodes in k-Group
2074. Reverse Nodes in Even Length Groups
```

"""

def reverse_prefix(a, k):
    prev, curr, tail = None, a, a

    for _ in range(k):
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next

    return prev, tail, curr

def reverse_between(
        head: Optional[ListNode],
        left: int,
        right: int
) -> Optional[ListNode]:
    # advance to the node i - 1, reverse j - i + 1 nodes, connect fragments
    if head is None or left == right:
        return head

    dummy = ListNode(0, head)
    before = advance_by_k(dummy, left - 1)

    rev_head, rev_tail, after = reverse_prefix(
        before.next,
        right - left + 1
    )

    before.next = rev_head
    rev_tail.next = after

    return dummy.next