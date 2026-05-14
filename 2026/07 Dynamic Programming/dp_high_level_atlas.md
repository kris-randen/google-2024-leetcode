# Dynamic Programming Toolkit — Part 1 High-Level Atlas

This document is the first-stage map. It treats DP as a subproblem-DAG discipline:
state space -> recurrence edges -> topological order -> base cases -> answer extraction -> complexity.

## Core family map

| Family | Core state shape | Core recurrence | Evaluation order | Main traps |
|---|---|---|---|---|
| 1D Prefix/Suffix DP | dp[i] | constant previous states | increasing/decreasing i | off-by-one base cases |
| House Robber | dp[i] / dfs(node)->(skip,take) | take vs skip | prefix or postorder | path/cycle/tree variants differ |
| Kadane | local ending-at-i + global | extend or restart | left-to-right | subarray vs subsequence |
| Stock | day x holding x constraint | buy/sell/hold/rest | increasing day | transaction count convention |
| Grid | dp[r][c] / dp[step][...] | neighbors / synchronized walkers | row-major or reverse | cyclic movement is not table DP |
| Two Sequence | dp[i][j] | match/mismatch/skip/edit | row-major or suffix reverse | prefix vs suffix convention |
| Knapsack | dp[i][w] / dp[w] | include/exclude/reuse | item-major | reverse vs forward loop |
| Coin Change | dp[amount] | add coin | item-first or amount-first | combinations vs permutations |
| Interval | dp[l][r] | boundary or split k | increasing length | using prefix/suffix when interval is needed |
| Game | dp[state] / dp[l][r] | current move vs opponent | interval length / memo | absolute score vs score difference |
| LIS | dp[i] / tails | previous compatible item | sorted/increasing index | sort key and strictness |
| Bitmask | dp[mask] | add/remove one bit | popcount / mask order | exponential state blowup |
| Digit | dp[pos][tight][started][...] | choose next digit | left-to-right | leading zeros / tight flag |
| Tree | dfs(node)->tuple | combine children | postorder / reroot | parent constraints need state expansion |
| Graph DP | dp[v]/dp[state] | relax edges | topo/Bellman/Dijkstra | graph may not be DAG |
| Probability | dp[state] | weighted sum | state order | precision and absorbing states |
| Monotonic Deque DP | dp[i] + window best | max/min previous in window | left-to-right | stale candidates / wrong monotonic invariant |

## First expansion order

1. Core SRTBOT mechanics
2. 1D DP and House Robber
3. Grid DP
4. Two-sequence DP
5. Knapsack and Coin Change
6. Interval DP and Stone Games
7. Stock state machines
8. LIS and sequence optimization
9. Bitmask, Digit, Tree, Graph DP
10. Advanced optimizations
