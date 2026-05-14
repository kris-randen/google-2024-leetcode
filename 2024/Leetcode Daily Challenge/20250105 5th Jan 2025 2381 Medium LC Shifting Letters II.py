"""

2381. Shifting Letters II
Medium

You are given a string s of lowercase English letters and a 2D integer array shifts where shifts[i] = [starti, endi, directioni]. For every i, shift the characters in s from the index starti to the index endi (inclusive) forward if directioni = 1, or shift the characters backward if directioni = 0.

Shifting a character forward means replacing it with the next letter in the alphabet (wrapping around so that 'z' becomes 'a'). Similarly, shifting a character backward means replacing it with the previous letter in the alphabet (wrapping around so that 'a' becomes 'z').

Return the final string after all such shifts to s are applied.

 

Example 1:

Input: s = "abc", shifts = [[0,1,0],[1,2,1],[0,2,1]]
Output: "ace"
Explanation: Firstly, shift the characters from index 0 to index 1 backward. Now s = "zac".
Secondly, shift the characters from index 1 to index 2 forward. Now s = "zbd".
Finally, shift the characters from index 0 to index 2 forward. Now s = "ace".
Example 2:

Input: s = "dztz", shifts = [[0,0,0],[1,1,1]]
Output: "catz"
Explanation: Firstly, shift the characters from index 0 to index 0 backward. Now s = "cztz".
Finally, shift the characters from index 1 to index 1 forward. Now s = "catz".
 

Constraints:

1 <= s.length, shifts.length <= 5 * 104
shifts[i].length == 3
0 <= starti <= endi < s.length
0 <= directioni <= 1
s consists of lowercase English letters.

Performance shiftedd
Time Limit Exceeded (Possibly because I'm not aggregagting all shifts and doing them one by one)

Performance shifted
Runtime 63 ms Beats 55.32%
Memory 41.26 MB Beats 42.25%

"""


def shiftedd(s, sfs):
    MOD = 26

    def strtouni(cs):   return [ord(c) - ord('a') for c in cs]
    def unitostr(vs):   return ''.join([chr(v + ord('a')) for v in vs])
    def shiftc(c, d):   return (c + (1 if d == 1 else -1))  % MOD
    
    def shifti(vs, i, d):   
        vs[i] = shiftc(vs[i], d)

    def shiftis(vs, si, ei, d):
        for i in range(si, ei + 1):
            shifti(vs, i, d)

    def shifts(vs, sfs):
        for si, ei, d in sfs:
            shiftis(vs, si, ei, d)
        return vs

    return unitostr(
                    shifts(
                            strtouni(s), sfs
                          )
                   )

from itertools import accumulate as acc

def shifted(s, sfs):
    def strtouni(cs):   return [ord(c) - ord('a') for c in cs]
    def unitostr(vs):   return ''.join([chr(v + ord('a')) for v in vs])
    def shiftc(c, p):   return (c + p)  % 26

    def diffs(sfs):
        df = [0] * (n := len(s))
        for si, ei, d in sfs:
            df[si] += 1 if d == 1 else -1
            if ei + 1 < n: 
                df[ei + 1] -= 1 if d == 1 else -1
        return df

    def shifts(sfs):
        return list(acc(diffs(sfs)))

    def shifti(vs, i, p):
        vs[i] = shiftc(vs[i], p)

    def shiftall(vs, ps):
        for i, p in enumerate(ps):
            shifti(vs, i, p)
        return vs

    return unitostr(
                    shiftall(
                            strtouni(s), shifts(sfs)
                            )
                    )

class Solution:
    def shiftingLetters(self, s: str, sfs: List[List[int]]) -> str:
        return shiftedd(s, sfs)

























