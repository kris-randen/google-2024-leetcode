"""
Part 8 — Stock Dynamic Programming Series

Scope:
    121. Best Time to Buy and Sell Stock
    122. Best Time to Buy and Sell Stock II
    123. Best Time to Buy and Sell Stock III
    188. Best Time to Buy and Sell Stock IV
    309. Best Time to Buy and Sell Stock with Cooldown
    714. Best Time to Buy and Sell Stock with Transaction Fee

Core mental model:
    Stock DP is finite-state DP over days.

    The minimum state is:
        hold = best profit after today while holding one stock
        cash = best profit after today while holding no stock

    Variants add constraints:
        one transaction
        unlimited transactions
        at most two transactions
        at most k transactions
        cooldown
        transaction fee

SRTBOT:
    S — Subproblems
    R — buy / sell / hold / rest transitions
    T — increasing day order
    B — before any day: cash = 0, hold = -infinity
    O — final answer is a non-holding state
    T — days × number_of_states






# Part 8 — Stock Series

Python file:

[Download Part 8 — Stock Series Python file](sandbox:/mnt/data/dp_part8_stock_series.py)

## What Part 8 covers

```text id="s7w2vo"
Stock DP
    -> 121. Stock I
    -> 122. Stock II
    -> 123. Stock III
    -> 188. Stock IV
    -> 309. Stock with Cooldown
    -> 714. Stock with Transaction Fee
```

## Core mental model

Stock DP is a **finite-state machine over days**.

The basic state is:

```text id="f4c5eq"
hold = best profit after today while holding one stock
cash = best profit after today while holding no stock
```

Transitions:

```text id="eahtg4"
hold -> hold      # keep holding
cash -> hold      # buy
hold -> cash      # sell
cash -> cash      # rest
```

Final answer:

```text id="9jjstr"
cash / non-holding state
```

You usually do **not** return `hold`, because holding at the end means unrealized profit.

---

## Series evolution ladder

### 121. Stock I — one transaction

State:

```text id="npr5wa"
best_buy = best -price seen so far
best = best profit after selling once
```

Reduction:

```text id="y3vsk7"
one buy state
+ one sell state
```

---

### 122. Stock II — unlimited transactions

State:

```text id="1uimse"
hold
cash
```

Recurrence:

```text id="qcxmej"
hold = max(old_hold, old_cash - price)
cash = max(old_cash, old_hold + price)
```

Greedy collapse:

```text id="7diebs"
sum all positive price differences
```

This greedy works only because there is no fee, cooldown, or transaction limit.

---

### 123. Stock III — at most two transactions

State:

```text id="c5wk5f"
buy1
sell1
buy2
sell2
```

Recurrence:

```text id="e27kjj"
buy1  = max(buy1, -price)
sell1 = max(sell1, buy1 + price)
buy2  = max(buy2, sell1 - price)
sell2 = max(sell2, buy2 + price)
```

This is not two independent Stock I problems. The states are ordered.

---

### 188. Stock IV — at most k transactions

State:

```text id="59kmcb"
buy[t]
sell[t]
```

Recurrence:

```text id="x6df5d"
buy[t]  = max(buy[t], sell[t - 1] - price)
sell[t] = max(sell[t], buy[t] + price)
```

Optimization:

```text id="0fjplr"
if k >= n // 2:
    reduce to unlimited transactions
```

---

### 309. Stock with Cooldown

Need explicit cooldown state:

```text id="jk1w5s"
hold = holding stock
sold = sold today
rest = not holding and not just sold
```

Recurrence:

```text id="29q1ze"
hold = max(old_hold, old_rest - price)
sold = old_hold + price
rest = max(old_rest, old_sold)
```

Why this works:

```text id="0e4t8i"
You can buy only from rest, not from sold-yesterday.
```

---

### 714. Stock with Fee

Same `hold/cash` state as unlimited transactions, but subtract fee once per completed transaction.

Fee-on-sell version:

```text id="xwrq0g"
hold = max(old_hold, old_cash - price)
cash = max(old_cash, old_hold + price - fee)
```

Fee-on-buy version is also valid, but do not charge both.

---

## Composition chains

```text id="dmn2cr"
day scan
+ best previous buy state
+ sell candidate
-> Stock I
```

```text id="8j03zq"
day scan
+ hold/cash states
+ buy/sell/rest transitions
-> Stock II
```

```text id="6nukaw"
hold/cash state
+ transaction fee on sell
-> Stock with Fee
```

```text id="x29ug0"
hold/sold/rest states
+ buy only from rest
-> Stock with Cooldown
```

```text id="pxu8uj"
hold/cash state
+ transaction count dimension
-> Stock IV
```

## Most important traps

```text id="56h62k"
1. Returning hold at the end.
2. Charging fee on both buy and sell.
3. Updating states in-place without preserving old values when needed.
4. Confusing transaction count before buy vs after sell.
5. Treating Stock III as two independent one-transaction problems.
6. Forgetting k >= n//2 collapses to unlimited transactions.
7. Applying greedy positive-delta summation to cooldown/fee/k-limited variants.
```

Next natural step: **Part 9 — Stone Game Series**.


"""

from __future__ import annotations

from math import inf


NEG = -10**18


# =============================================================================
# Level 0 — Stock State Utilities
# =============================================================================


def neg_inf() -> int:
    """
    Sentinel for impossible profit states.

    Example:
        Before seeing any price, holding stock is impossible.
        So hold = -infinity.
    """
    return NEG


def final_non_holding(*states: int) -> int:
    """
    Terminal stock invariant:
        The answer should be a non-holding state.

    Holding stock at the end means profit is unrealized.
    """
    return max(states)


# =============================================================================
# Level 1 — One Transaction
# =============================================================================


def max_profit_one_transaction(prices: list[int]) -> int:
    """
    LeetCode:
        121. Best Time to Buy and Sell Stock

    S:
        best_buy = best value of -price seen so far.
        best = best profit after selling once.

    R:
        Buy candidate:
            best_buy = max(best_buy, -price)

        Sell candidate:
            best = max(best, best_buy + price)

    T:
        scan prices left to right.

    B:
        best_buy = -inf
        best = 0

    O:
        best

    Complexity:
        O(n) time, O(1) space.

    This is the one-transaction compression of hold/cash.
    """
    best_buy = neg_inf()
    best = 0

    for price in prices:
        best_buy = max(best_buy, -price)
        best = max(best, best_buy + price)

    return best


def max_profit_one_transaction_min_price(prices: list[int]) -> int:
    """
    Equivalent greedy-looking form.

    State:
        min_price = minimum price seen so far.
        best = best sell profit so far.

    This is still DP-like state compression:
        min_price stores the best previous buy state.
    """
    min_price = inf
    best = 0

    for price in prices:
        min_price = min(min_price, price)
        best = max(best, price - min_price)

    return int(best)


# =============================================================================
# Level 2 — Unlimited Transactions
# =============================================================================


def max_profit_unlimited_transactions_state_machine(prices: list[int]) -> int:
    """
    LeetCode:
        122. Best Time to Buy and Sell Stock II

    S:
        hold = best profit after today while holding stock.
        cash = best profit after today while not holding stock.

    R:
        hold' = max(old_hold, old_cash - price)
            keep holding or buy today.

        cash' = max(old_cash, old_hold + price)
            keep cash or sell today.

    T:
        increasing day.

    B:
        hold = -inf
        cash = 0

    O:
        cash

    Complexity:
        O(n) time, O(1) space.
    """
    hold = neg_inf()
    cash = 0

    for price in prices:
        old_hold = hold
        old_cash = cash

        hold = max(old_hold, old_cash - price)
        cash = max(old_cash, old_hold + price)

    return cash


def max_profit_unlimited_transactions_greedy(prices: list[int]) -> int:
    """
    Greedy reduction for Stock II.

    Because transactions are unlimited and there is no fee/cooldown,
    every positive upward edge can be harvested independently.

    This is the DP-vs-Greedy boundary:
        The state-machine DP collapses to sum of positive deltas.
    """
    return sum(
        max(0, prices[i] - prices[i - 1])
        for i in range(1, len(prices))
    )


# =============================================================================
# Level 3 — Transaction Fee
# =============================================================================


def max_profit_with_fee_sell_fee(prices: list[int], fee: int) -> int:
    """
    LeetCode:
        714. Best Time to Buy and Sell Stock with Transaction Fee

    State:
        hold, cash as in unlimited transactions.

    Difference:
        Selling pays transaction fee.

    R:
        hold' = max(old_hold, old_cash - price)
        cash' = max(old_cash, old_hold + price - fee)

    Fee can be charged on sell or buy, but not both.
    """
    hold = neg_inf()
    cash = 0

    for price in prices:
        old_hold = hold
        old_cash = cash

        hold = max(old_hold, old_cash - price)
        cash = max(old_cash, old_hold + price - fee)

    return cash


def max_profit_with_fee_buy_fee(prices: list[int], fee: int) -> int:
    """
    Equivalent version that charges the fee when buying.

    R:
        hold' = max(old_hold, old_cash - price - fee)
        cash' = max(old_cash, old_hold + price)
    """
    hold = neg_inf()
    cash = 0

    for price in prices:
        old_hold = hold
        old_cash = cash

        hold = max(old_hold, old_cash - price - fee)
        cash = max(old_cash, old_hold + price)

    return cash


# =============================================================================
# Level 4 — Cooldown
# =============================================================================


def max_profit_with_cooldown(prices: list[int]) -> int:
    """
    LeetCode:
        309. Best Time to Buy and Sell Stock with Cooldown

    Constraint:
        After selling, you cannot buy on the next day.

    States:
        hold = holding a stock after today
        sold = sold today
        rest = not holding, and not sold today

    R:
        hold' = max(old_hold, old_rest - price)
            You can buy only from rest, not from sold.

        sold' = old_hold + price
            You sell today.

        rest' = max(old_rest, old_sold)
            You do nothing, or cooldown expires.

    O:
        max(sold, rest)

    Trap:
        Returning hold is invalid.
    """
    hold = neg_inf()
    sold = neg_inf()
    rest = 0

    for price in prices:
        old_hold = hold
        old_sold = sold
        old_rest = rest

        hold = max(old_hold, old_rest - price)
        sold = old_hold + price
        rest = max(old_rest, old_sold)

    return final_non_holding(sold, rest)


def max_profit_with_cooldown_shifted(prices: list[int]) -> int:
    """
    Alternative compressed recurrence.

    cash[i] = max profit not holding after day i.
    hold[i] = max profit holding after day i.

    Cooldown means buying today must come from cash[i-2].

    This version is less explicit than hold/sold/rest but useful to recognize.
    """
    hold = neg_inf()
    cash = 0
    prev_cash = 0  # cash from i-2 after the update dance

    for price in prices:
        old_cash = cash

        cash = max(cash, hold + price)
        hold = max(hold, prev_cash - price)

        prev_cash = old_cash

    return cash


# =============================================================================
# Level 5 — At Most Two Transactions
# =============================================================================


def max_profit_two_transactions(prices: list[int]) -> int:
    """
    LeetCode:
        123. Best Time to Buy and Sell Stock III

    State-machine form:
        buy1  = best profit after first buy
        sell1 = best profit after first sell
        buy2  = best profit after second buy
        sell2 = best profit after second sell

    R:
        buy1  = max(buy1, -price)
        sell1 = max(sell1, buy1 + price)
        buy2  = max(buy2, sell1 - price)
        sell2 = max(sell2, buy2 + price)

    O:
        sell2

    Trap:
        These are ordered states, not independent transactions.
    """
    buy1 = neg_inf()
    sell1 = 0
    buy2 = neg_inf()
    sell2 = 0

    for price in prices:
        buy1 = max(buy1, -price)
        sell1 = max(sell1, buy1 + price)
        buy2 = max(buy2, sell1 - price)
        sell2 = max(sell2, buy2 + price)

    return sell2


def max_profit_two_transactions_prefix_suffix(prices: list[int]) -> int:
    """
    Alternative decomposition for at most two transactions.

    left[i]  = best one-transaction profit in prices[:i+1]
    right[i] = best one-transaction profit in prices[i:]

    answer = max(left[i] + right[i+1])

    This is useful for understanding, but state-machine is more general.
    """
    n = len(prices)

    if n == 0:
        return 0

    left = [0] * n
    min_price = prices[0]

    for i in range(1, n):
        min_price = min(min_price, prices[i])
        left[i] = max(left[i - 1], prices[i] - min_price)

    right = [0] * n
    max_price = prices[-1]

    for i in range(n - 2, -1, -1):
        max_price = max(max_price, prices[i])
        right[i] = max(right[i + 1], max_price - prices[i])

    best = 0

    for i in range(n):
        second = right[i + 1] if i + 1 < n else 0
        best = max(best, left[i] + second)

    return best


# =============================================================================
# Level 6 — At Most K Transactions
# =============================================================================


def max_profit_k_transactions(prices: list[int], k: int) -> int:
    """
    LeetCode:
        188. Best Time to Buy and Sell Stock IV

    S:
        buy[t] = best profit after t-th buy, holding stock.
        sell[t] = best profit after t-th sell, not holding stock.

    t is 1-indexed.

    R:
        buy[t] = max(buy[t], sell[t-1] - price)
        sell[t] = max(sell[t], buy[t] + price)

    T:
        increasing day.
        transaction states in increasing t.

    B:
        sell[0] = 0
        buy[*] = -inf

    O:
        sell[k]

    Complexity:
        O(nk)

    Optimization:
        If k >= n//2, reduce to unlimited transactions.
    """
    n = len(prices)

    if k <= 0 or n <= 1:
        return 0

    if k >= n // 2:
        return max_profit_unlimited_transactions_greedy(prices)

    buy = [neg_inf()] * (k + 1)
    sell = [0] * (k + 1)

    for price in prices:
        for t in range(1, k + 1):
            buy[t] = max(buy[t], sell[t - 1] - price)
            sell[t] = max(sell[t], buy[t] + price)

    return sell[k]


def max_profit_k_transactions_table(prices: list[int], k: int) -> int:
    """
    Table form for learning.

    dp[t][i] = max profit using at most t transactions by day i.

    Recurrence:
        dp[t][i] = max(
            dp[t][i - 1],
            prices[i] + max(dp[t - 1][j - 1] - prices[j]) for j <= i
        )

    Optimize the inner max with best_buy.

    Complexity:
        O(k*n)
    """
    n = len(prices)

    if k <= 0 or n <= 1:
        return 0

    if k >= n // 2:
        return max_profit_unlimited_transactions_greedy(prices)

    dp = [[0] * n for _ in range(k + 1)]

    for t in range(1, k + 1):
        best_buy = -prices[0]

        for i in range(1, n):
            dp[t][i] = max(dp[t][i - 1], prices[i] + best_buy)
            best_buy = max(best_buy, dp[t - 1][i - 1] - prices[i])

    return dp[k][n - 1]


# =============================================================================
# Level 7 — Unified Stock State Machine
# =============================================================================


def max_profit_stock(
    prices: list[int],
    *,
    max_transactions: int | None = None,
    fee: int = 0,
    cooldown: bool = False,
) -> int:
    """
    Unified dispatcher for the common LeetCode stock variants.

    This is intentionally not the shortest code.
    It shows how variants map to different state machines.

    Supported combinations:
        unlimited transactions
        unlimited + fee
        unlimited + cooldown
        at most k transactions without fee/cooldown

    For interview use, prefer the specialized functions.
    """
    if max_transactions is None and not cooldown:
        if fee:
            return max_profit_with_fee_sell_fee(prices, fee)

        return max_profit_unlimited_transactions_state_machine(prices)

    if max_transactions is None and cooldown:
        if fee:
            raise ValueError("This toolkit keeps fee+cooldown separate for clarity.")

        return max_profit_with_cooldown(prices)

    if max_transactions is not None:
        if fee or cooldown:
            raise ValueError("This toolkit keeps k+fee/cooldown variants separate for clarity.")

        return max_profit_k_transactions(prices, max_transactions)

    raise ValueError("Unsupported stock configuration.")


# =============================================================================
# Level 8 — Series Ladder
# =============================================================================


STOCK_SERIES_LADDER = {
    "121_stock_i": {
        "state": "best_buy, best",
        "constraint": "at most one transaction",
        "skeleton": "one buy state + one sell state",
    },
    "122_stock_ii": {
        "state": "hold, cash",
        "constraint": "unlimited transactions",
        "skeleton": "two-state machine",
    },
    "123_stock_iii": {
        "state": "buy1, sell1, buy2, sell2",
        "constraint": "at most two transactions",
        "skeleton": "four ordered states",
    },
    "188_stock_iv": {
        "state": "buy[t], sell[t]",
        "constraint": "at most k transactions",
        "skeleton": "transaction-indexed state machine",
    },
    "309_stock_cooldown": {
        "state": "hold, sold, rest",
        "constraint": "cooldown after selling",
        "skeleton": "explicit cooldown state",
    },
    "714_stock_fee": {
        "state": "hold, cash",
        "constraint": "transaction fee",
        "skeleton": "two-state machine with fee on buy or sell",
    },
}


STOCK_DP_DIAGNOSTIC_CHECKLIST = [
    "How many transactions are allowed?",
    "Can multiple transactions overlap? Usually no, so only one stock may be held.",
    "What does holding state mean after day i?",
    "What does non-holding state mean after day i?",
    "Is there a fee? Charge it on buy or sell, but not both.",
    "Is there cooldown? If yes, buying cannot come directly from sold-yesterday.",
    "Is transaction count incremented on buy or sell? Be consistent.",
    "Can k >= n//2 collapse to unlimited transactions?",
    "Which terminal states are valid? Usually non-holding only.",
    "Are in-place updates using old states correctly?",
]


# =============================================================================
# Part 8 Problem Map
# =============================================================================


PART_8_PROBLEM_MAP = {
    "one_transaction": [
        121,
    ],
    "unlimited_transactions": [
        122,
    ],
    "two_transactions": [
        123,
    ],
    "k_transactions": [
        188,
    ],
    "cooldown": [
        309,
    ],
    "transaction_fee": [
        714,
    ],
}


if __name__ == "__main__":
    assert max_profit_one_transaction([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit_one_transaction([7, 6, 4, 3, 1]) == 0
    assert max_profit_one_transaction_min_price([7, 1, 5, 3, 6, 4]) == 5

    assert max_profit_unlimited_transactions_state_machine([7, 1, 5, 3, 6, 4]) == 7
    assert max_profit_unlimited_transactions_greedy([7, 1, 5, 3, 6, 4]) == 7

    assert max_profit_with_fee_sell_fee([1, 3, 2, 8, 4, 9], 2) == 8
    assert max_profit_with_fee_buy_fee([1, 3, 2, 8, 4, 9], 2) == 8

    assert max_profit_with_cooldown([1, 2, 3, 0, 2]) == 3
    assert max_profit_with_cooldown_shifted([1, 2, 3, 0, 2]) == 3

    assert max_profit_two_transactions([3, 3, 5, 0, 0, 3, 1, 4]) == 6
    assert max_profit_two_transactions_prefix_suffix([3, 3, 5, 0, 0, 3, 1, 4]) == 6

    assert max_profit_k_transactions([2, 4, 1], 2) == 2
    assert max_profit_k_transactions([3, 2, 6, 5, 0, 3], 2) == 7
    assert max_profit_k_transactions_table([3, 2, 6, 5, 0, 3], 2) == 7

    assert max_profit_stock([7, 1, 5, 3, 6, 4]) == 7
    assert max_profit_stock([1, 3, 2, 8, 4, 9], fee=2) == 8
    assert max_profit_stock([1, 2, 3, 0, 2], cooldown=True) == 3
    assert max_profit_stock([3, 2, 6, 5, 0, 3], max_transactions=2) == 7
