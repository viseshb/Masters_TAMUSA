import time

def fractional_knapsack(items, max_weight):   
    # Calculate value-to-weight ratio for each item
    value_per_weight = [(item[0], item[2] / item[1], item[1], item[2]) for item in items]

    # Sort items in descending order of value-to-weight ratio
    value_per_weight.sort(key=lambda x: x[1], reverse=True)

    total_value = 0
    knapsack_items = []
    remaining_weight = max_weight

    for item_name, _, item_weight, item_value in value_per_weight:
        if item_weight <= remaining_weight:
            # Take the whole item
            total_value += item_value
            remaining_weight -= item_weight
            knapsack_items.append((item_name, 1))
        else:
            # Take a fraction of the item
            fraction = remaining_weight / item_weight
            total_value += item_value * fraction
            knapsack_items.append((item_name, fraction))
            break  # Knapsack is full

    return total_value, knapsack_items


# Test Cases for Fractional Knapsack
items1 = [("A", 10, 60), ("B", 20, 100), ("C", 30, 120)]
max_weight1 = 50

items2 = [("A", 1, 6), ("B", 2, 11), ("C", 3, 12), ("D", 5, 14)]
max_weight2 = 10

# Run test cases and print results
start_time = time.perf_counter()
max_value1, selected_items1 = fractional_knapsack(items1, max_weight1)
print("Fractional Knapsack Test Case 1:")
print("Maximum value:", max_value1)
print("Included items:", selected_items1)

max_value2, selected_items2 = fractional_knapsack(items2, max_weight2)
end_time = time.perf_counter()
print("\nFractional Knapsack Test Case 2:")
print("Maximum value:", max_value2)
print("Included items:", selected_items2)
print(f"Execution time using ChatGPT (Greedy Approach): {end_time - start_time:.8f} seconds")

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
# import random
# import time

# def fractional_knapsack_large(items, max_weight):
#     """
#     Solves the Fractional Knapsack problem using a greedy strategy for a larger number of items.

#     Args:
#         items: A list of tuples, where each tuple is (item_name, weight, value).
#         max_weight: The maximum weight the knapsack can hold.

#     Returns:
#         A tuple containing:
#             - The maximum total value that can be put in the knapsack.
#             - A list of tuples, where each tuple is (item_name, fraction_taken, weight, value).
#             - The execution time of the algorithm.
#     """

#     value_per_weight = [(item[0], item[2] / item[1], item[1], item[2]) for item in items]
#     value_per_weight.sort(key=lambda x: x[1], reverse=True)

#     total_value = 0
#     knapsack_items = []
#     remaining_weight = max_weight

    

#     for item_name, _, item_weight, item_value in value_per_weight:
#         if item_weight <= remaining_weight:
#             total_value += item_value
#             remaining_weight -= item_weight
#             knapsack_items.append((item_name, 1, item_weight, item_value))
#         else:
#             fraction = remaining_weight / item_weight
#             total_value += item_value * fraction
#             knapsack_items.append((item_name, fraction, item_weight, item_value))
#             break

   

#     return total_value, knapsack_items


# # Generate 100 items with strictly increasing weights and values
# def generate_items_fractional(n=100, max_weight=150, max_value=500):
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
# items_large_fractional = generate_items_fractional()
# max_weight_large_fractional = 500

# # Run and print results for Fractional Knapsack
# start_time = time.perf_counter() # Moved start time here
# max_value_fractional, selected_items_fractional = fractional_knapsack_large(
#     items_large_fractional, max_weight_large_fractional
# )
# end_time = time.perf_counter() # Moved end time here
# print("\nFractional Knapsack with 100 items:")
# print("Maximum value:", max_value_fractional)
# print("Items added to knapsack:")
# for item in selected_items_fractional:
#     print(f"Item {item[0]}: {item[1]:.2f} of (weight={item[2]}, value={item[3]})")
# print(f"Execution time using ChatGPT (Greedy Approach): {end_time - start_time:.8f} seconds")