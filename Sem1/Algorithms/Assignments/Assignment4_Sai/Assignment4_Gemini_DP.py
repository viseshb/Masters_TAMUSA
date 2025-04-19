import random
import time

def knapsack_01_dp(capacity, weights, values):
   

    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] > w:
                dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = max(
                    dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]]
                )

    return dp[n][capacity], dp


def get_selected_items_01(capacity, weights, values, dp):
    """
    Finds the items included in the knapsack.

    Args:
        capacity: The maximum weight capacity of the knapsack.
        weights: A list of the weights of the items.
        values: A list of the values of the items.
        dp: The DP table calculated by knapsack_01_dp.

    Returns:
        A list of the indices of the selected items.
    """

    n = len(values)
    w = capacity
    selected_items = []

    for i in range(n, 0, -1):
        if i > 0 and dp[i][w] != dp[i - 1][w]:  # Check if item was included
            selected_items.append(i - 1)
            w -= weights[i - 1]

    return selected_items


def measure_execution_time(func, *args, number=10):
    """
    Measures the execution time of a function using time.perf_counter().

    Args:
        func: The function to measure.
        *args: The arguments to pass to the function.
        number: The number of times to execute the function.

    Returns:
        The average execution time in seconds.
    """
    start_time = time.perf_counter()
    for _ in range(number):
        func(*args)
    end_time = time.perf_counter()
    return (end_time - start_time) / number


# Test cases
test_cases = [
    {
        "name": "Test Case 1",
        "weights": [10, 20, 30],
        "values": [60, 100, 120],
        "capacity": 50,
    },
    {
        "name": "Test Case 2",
        "weights": [1, 2, 3, 5],
        "values": [6, 11, 12, 14],
        "capacity": 10,
    },
    {
        "name": "Random 100 Items",
        "weights": [random.randint(1, 150) for _ in range(100)],
        "values": [],
        "capacity": 500,
    },
]


# Run tests for 0/1 Knapsack
print("--- 0/1 Knapsack Tests ---")
for test_case in test_cases:
    print(f"\n--- {test_case['name']} ---")

    # Generate values for the 100-item test case
    if not test_case["values"]:
        test_case["values"] = [
            w * 3 + random.randint(-5, 20) for w in test_case["weights"]
        ]
        test_case["values"] = [max(1, min(v, 500)) for v in test_case["values"]]

    capacity = test_case["capacity"]
    weights = test_case["weights"]
    values = test_case["values"]

    # Measure execution time
    execution_time = measure_execution_time(
        knapsack_01_dp, capacity, weights, values, number=10
    )
    print(f"Execution Time: {execution_time:.6f} seconds")

    # Run the knapsack algorithm and print results
    max_value, dp_table = knapsack_01_dp(capacity, weights, values)
    print(f"Maximum value: {max_value}")

    selected_items_indices = get_selected_items_01(
        capacity, weights, values, dp_table
    )
    selected_items = [f"Item {i + 1}" for i in selected_items_indices]
    print(f"Selected items: {selected_items}")