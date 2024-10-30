"""

347. Top K Frequent Elements
Medium
Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.



Example 1:

Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
Example 2:

Input: nums = [1], k = 1
Output: [1]


Constraints:

1 <= nums.length <= 105
-104 <= nums[i] <= 104
k is in the range [1, the number of unique elements in the array].
It is guaranteed that the answer is unique.


Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's size.

"""

from heapq import *
from collections import Counter


def topKFreq(vs, k):
    return [v[0] for v in Counter(vs).most_common(k)]


def topk(vs, k):
    us = [-v for v in vs]; heapify(us); ms = []
    for _ in range(k): m = heappop(us); ms.append(-m)
    return ms


def vfilter(cs, vs):
    return [k for k, v in cs.items() if v in vs]


def topKF(vs, k):
    cs = Counter(vs)
    return vfilter(cs, topk(cs.values(), k))