import random
import time

def fractional_knapsack(capacity, weights, values):
    """
    Solves the Fractional Knapsack problem using a greedy approach.
    """

    # Calculate value-to-weight ratios
    ratios = [(values[i] / weights[i], i) for i in range(len(values))]

    # Sort items in descending order of their value-to-weight ratio
    ratios.sort(key=lambda x: x[0], reverse=True)

    max_value = 0
    load = 0
    selected_items = []  # To store (item index, fraction taken)

    for ratio, index in ratios:
        if weights[index] <= capacity - load:
            # Take the whole item
            max_value += values[index]
            load += weights[index]
            selected_items.append((index, 1))
        else:
            # Take a fraction of the item
            fraction = (capacity - load) / weights[index]
            max_value += values[index] * fraction
            load = capacity
            selected_items.append((index, fraction))
            break  # Knapsack is full

    return max_value, selected_items


def measure_execution_time(func, *args, number=10):
    """
    Measures the execution time of a function using time.perf_counter().
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


# Run tests for Fractional Knapsack
print("--- Fractional Knapsack Tests ---")
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
        fractional_knapsack, capacity, weights, values, number=10
    )
    print(f"Execution Time: {execution_time:.6f} seconds")

    # Run the knapsack algorithm and print results
    max_value, selected_items = fractional_knapsack(capacity, weights, values)
    print(f"Maximum value: {max_value}")
    print("Selected items:", end=" ")  # Print "Selected items:" once, at the beginning
    for index, fraction in selected_items:
        print(f"Item {index + 1}: {fraction}", end="  ")  # Print items side-by-side
    print()  # Print a newline at the end of the list