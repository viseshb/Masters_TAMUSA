
import time
import random

def fractional_knapsack(weights, values, W):
    n = len(values)
    ratio = [(values[i] / weights[i], weights[i], values[i], i) for i in range(n)]
    ratio.sort(reverse=True)

    max_value = 0.0
    selected_items = []
    start_time = time.perf_counter()

    for r, wt, val, idx in ratio:
        if W == 0:
            break
        if wt <= W:
            max_value += val
            selected_items.append((idx, 1))  # full item
            W -= wt
        else:
            fraction = W / wt
            max_value += val * fraction
            selected_items.append((idx, fraction))  # partial item
            break

    end_time = time.perf_counter()
    exec_time = end_time - start_time

    return max_value, selected_items, exec_time

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
    max_val, items, runtime = fractional_knapsack(test["weights"], test["values"], test["capacity"])
    print(f"\n{test['name']} (Fractional Knapsack Greedy)")
    print(f"Max Value: {max_val:.2f}")
    print(f"Selected Items (index, fraction): {items}")
    print(f"Execution Time: {runtime:.12f} seconds")
