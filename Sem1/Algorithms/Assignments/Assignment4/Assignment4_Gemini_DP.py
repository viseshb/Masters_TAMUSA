import time

def knapsack_01_dp(items, max_weight): 
    n = len(items)
    # Initialize a table to store the maximum values for different weights and items
    dp_table = [[0 for _ in range(max_weight + 1)] for _ in range(n + 1)]

    # Build the dp_table in a bottom-up manner
    for i in range(1, n + 1):
        for w in range(1, max_weight + 1):
            if items[i - 1][1] > w:  # If the current item's weight is greater than the current weight
                dp_table[i][w] = dp_table[i - 1][w]
            else:  # Otherwise, take the maximum of including or not including the item
                dp_table[i][w] = max(dp_table[i - 1][w], items[i - 1][2] + dp_table[i - 1][w - items[i - 1][1]])

    # Backtrack to find the items included in the knapsack
    included_items = []
    w = max_weight
    for i in range(n, 0, -1):
        if dp_table[i][w] != dp_table[i - 1][w]:
            included_items.append(items[i - 1][0])
            w -= items[i - 1][1]

    return dp_table[n][max_weight], included_items


# Test Cases for 0/1 Knapsack
items1 = [("A", 10, 60), ("B", 20, 100), ("C", 30, 120)]
max_weight1 = 50

items2 = [("A", 1, 6), ("B", 2, 11), ("C", 3, 12), ("D", 5, 14)]
max_weight2 = 10

# Run test cases and print results
start_time = time.perf_counter()
max_value1, selected_items1 = knapsack_01_dp(items1, max_weight1)
print("0/1 Knapsack Test Case 1:")
print("Maximum value:", max_value1)
print("Included items:", selected_items1)

max_value2, selected_items2 = knapsack_01_dp(items2, max_weight2)
end_time = time.perf_counter()
print("\n0/1 Knapsack Test Case 2:")
print("Maximum value:", max_value2)
print("Included items:", selected_items2)

print(f"Execution time using Gemini (Dynamic Programming Approach): {end_time - start_time:.8f} seconds")
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
# import random
# import time

# def knapsack_01_dp_large(items, max_weight):
#     """
#     Solves the 0/1 Knapsack problem using dynamic programming for a larger number of items.

#     Args:
#         items: A list of tuples, where each tuple is (item_name, weight, value).
#         max_weight: The maximum weight the knapsack can hold.

#     Returns:
#         A tuple containing:
#             - The maximum total value that can be put in the knapsack.
#             - A list of tuples, where each tuple is (item_name, weight, value).
#             - The execution time of the algorithm.
#     """

#     n = len(items)
#     dp_table = [[0 for _ in range(max_weight + 1)] for _ in range(n + 1)]

    

#     for i in range(1, n + 1):
#         for w in range(1, max_weight + 1):
#             if items[i - 1][1] > w:
#                 dp_table[i][w] = dp_table[i - 1][w]
#             else:
#                 dp_table[i][w] = max(dp_table[i - 1][w], items[i - 1][2] + dp_table[i - 1][w - items[i - 1][1]])

#     included_items = []
#     w = max_weight
#     for i in range(n, 0, -1):
#         if dp_table[i][w] != dp_table[i - 1][w]:
#             included_items.append(items[i - 1])
#             w -= items[i - 1][1]

    

#     return dp_table[n][max_weight], included_items


# # Generate 100 items with strictly increasing weights and values
# def generate_items_01(n=100, max_weight=150, max_value=500):
#     items = []
#     weights = sorted(random.sample(range(1, max_weight + 1), n))  # Unique sorted weights
#     values = []
#     current_value = random.randint(1, max_value // (2 * n))  # Start with a small random value
#     for i in range(n):
#         current_value += random.randint(1, max_value // n)  # Ensure value increases
#         values.append(current_value)

#     for i in range(n):
#         items.append((f"Item{i + 1}", weights[i], values[i]))
#     return items


# # Test Case with 100 items
# items_large_01 = generate_items_01()
# max_weight_large_01 = 500

# # Run and print results for 0/1 Knapsack
# start_time = time.perf_counter() # Moved start time here
# max_value_01, selected_items_01 = knapsack_01_dp_large(items_large_01, max_weight_large_01)
# end_time = time.perf_counter() # Moved end time here
# print("0/1 Knapsack with 100 items:")
# print("Maximum value:", max_value_01)
# print("Items added to knapsack:")
# for item in selected_items_01:
#     print(f"Item {item[0]}: 1.00 of (weight={item[1]}, value={item[2]})")
# print(f"Execution time using Gemini (Dynamic Programming Approach): {end_time - start_time:.8f} seconds")