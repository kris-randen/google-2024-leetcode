"""

Yes. That primitive block is useful for **most 2D grid traversal problems where the grid is an implicit unweighted graph**.

It directly covers this family:

```text
cell = graph node
DIRS4 / DIRS8 = edges
in_bounds = graph boundary
grid value check = passability
DFS/BFS = traversal
seen or mutation = visited state
```

It is especially useful for:

```text
connected components
flood fill
island counting
area counting
boundary-connected regions
escape/reachability problems
multi-source BFS
nearest-distance problems
```

It is **less sufficient by itself** when the problem needs weighted shortest path, stateful traversal, or path optimization. Then you still reuse `Cell`, `DIRS4`, `in_bounds`, and `neighbors`, but the traversal becomes Dijkstra, 0-1 BFS, BFS with extra state, or backtracking.

High-value medium problems to practice next:

| Problem                      | Why it is high value                                                                                                                                                                                     | Primitive transfer                                                 |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **695. Max Area of Island**  | Closest extension of Number of Islands. Instead of counting components, return the size of the largest component. LeetCode defines island area as the number of `1` cells in the island. ([LeetCode][1]) | `cells + is_land + valid_neighbors + recursive DFS returning area` |
| **130. Surrounded Regions**  | Teaches the critical “start from boundary, mark safe, then flip the rest” pattern. The task is to replace surrounded `O`s with `X`s in-place. ([LeetCode][2])                                            | `boundary cells + DFS/BFS from border O + mutation`                |
| **1020. Number of Enclaves** | Same boundary-reachability idea, but with land cells. The goal is to count land cells that cannot walk off the grid boundary. ([LeetCode][3])                                                            | `boundary land DFS + count remaining land`                         |
| **994. Rotting Oranges**     | Introduces **multi-source BFS**. All rotten oranges spread simultaneously to 4-directionally adjacent fresh oranges, and the answer is elapsed minutes. ([LeetCode][4])                                  | `DIRS4 + queue + level BFS + minute counter`                       |
| **542. 01 Matrix**           | Another multi-source BFS classic. Start BFS from all zero cells and compute nearest-zero distance for every cell. ([LeetCode][5])                                                                        | `all zero cells as BFS seeds + distance grid`                      |

Practice order I’d use:

```text
1. 695. Max Area of Island
2. 130. Surrounded Regions
3. 1020. Number of Enclaves
4. 994. Rotting Oranges
5. 542. 01 Matrix
```

The first three are mainly **DFS/component/boundary** practice. The last two force the next important primitive: **multi-source BFS**.

For your current grid primitive, `695` is the cleanest next problem. It is basically:

```python
def area(p):
    mark p visited
    return 1 + sum(area(q) for valid unvisited land neighbors)
```

So it reuses the exact mental model from `Number of Islands`, but makes DFS return useful information instead of just sinking the component.

[1]: https://leetcode.com/problems/max-area-of-island/?utm_source=chatgpt.com "Max Area of Island"
[2]: https://leetcode.com/problems/surrounded-regions/?utm_source=chatgpt.com "Surrounded Regions"
[3]: https://leetcode.com/problems/number-of-enclaves/?utm_source=chatgpt.com "Number of Enclaves"
[4]: https://leetcode.com/problems/rotting-oranges/?utm_source=chatgpt.com "Rotting Oranges"
[5]: https://leetcode.com/problems/01-matrix/?utm_source=chatgpt.com "01 Matrix"


"""