
import time
import random

def knapsack_01_dp(weights, values, W):
    n = len(values)
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    start_time = time.perf_counter()

    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    selected_items = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)
            w -= weights[i-1]

    end_time = time.perf_counter()
    exec_time = end_time - start_time

    return dp[n][W], list(reversed(selected_items)), exec_time

# --- TEST CASES ---
test_cases = [
    {
        "name": "Test Case 1",
        "weights": [10, 20, 30],
        "values": [60, 100, 120],
        "capacity": 50
    },
    {
        "name": "Test Case 2",
        "weights": [1, 2, 3, 5],
        "values": [6, 11, 12, 14],
        "capacity": 10
    },
    {
        "name": "Random 100 Items",
        "weights": [random.randint(1, 150) for _ in range(100)],
        "values": [],
        "capacity": 500
    }
]

# Generate increasing values for weights in test case 3
test_cases[2]["values"] = [w + random.randint(1, 10) * 3 for w in test_cases[2]["weights"]]

for test in test_cases:
    max_val, items, runtime = knapsack_01_dp(test["weights"], test["values"], test["capacity"])
    print(f"\n{test['name']} (0/1 Knapsack DP)")
    print(f"Max Value: {max_val}")
    print(f"Selected Items Indexes: {items}")
    print(f"Execution Time: {runtime:.12f} seconds")
