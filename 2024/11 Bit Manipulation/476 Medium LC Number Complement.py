"""

476. Number Complement
Solved
Easy
Topics
Companies
The complement of an integer is the integer you get when you flip all the 0's to 1's and all the 1's to 0's in its binary representation.

For example, The integer 5 is "101" in binary and its complement is "010" which is the integer 2.
Given an integer num, return its complement.



Example 1:

Input: num = 5
Output: 2
Explanation: The binary representation of 5 is 101 (no leading zero bits), and its complement is 010. So you need to output 2.
Example 2:

Input: num = 1
Output: 0
Explanation: The binary representation of 1 is 1 (no leading zero bits), and its complement is 0. So you need to output 0.


Constraints:

1 <= num < 231

"""

import re
from fractions import Fraction
from functools import reduce

if __name__ == '__main__':
    expression = '1/3-1/2'
    expression3 = '-1/2+1/2'
    expression1 = '-1/2+1/2-2/3-5/7'
    expression2 = '-1/2+1/2+1/3'
    tokens = re.findall(r'([+-])?(\d+/\d+)', expression)
    print(tokens)
    fractions = [(-Fraction(f[1]) if f[0] == '-' else Fraction(f[1])) for f in tokens]
    print(fractions)
    val = reduce(lambda acc, f: acc + f, fractions)
    print(val == 0)


    def score(bs):
        B = [0] * ((n := len(bs)) + 1)
        B[n - 1] = max(0, bs[n - 1])
        for i in reversed(range(n - 1)):
            print(f'i {i}')
            B[i] = max(
                B[i + 1],
                B[i + 1] + bs[i],
                B[i + 2] + bs[i] * bs[i + 1]
            )
            print(f'B[{i}] {B[i]}')
        return B[0]

    # bs = [1, 1, 9, 9, 2, -5, 5]
    bs = []
    print(score(bs))
