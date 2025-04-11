import time

def knapsack_fractional(weights, values, W):
    index = list(range(len(weights)))
    ratio = [v/w for v, w in zip(values, weights)]
    index.sort(key=lambda i: ratio[i], reverse=True)

    max_value = 0
    items = []

    for i in index:
        if weights[i] <= W:
            W -= weights[i]
            max_value += values[i]
            items.append((i, 1))
        else:
            frac = W / weights[i]
            max_value += values[i] * frac
            items.append((i, frac))
            break

    return max_value, items

# Problem 1
w1, v1, cap1 = [10, 20, 30], [60, 100, 120], 50
start_time = time.perf_counter()
val1, items1 = knapsack_fractional(w1, v1, cap1)
print("\n=== Fractional Knapsack - Problem 1 ===")
print("Maximum Value:", val1)
for i, frac in items1:
    print(f"Item {i}: {frac:.2f} of (weight={w1[i]}, value={v1[i]})")

# Problem 2
w2, v2, cap2 = [1, 2, 3, 5], [6, 11, 12, 14], 10
val2, items2 = knapsack_fractional(w2, v2, cap2)
end_time = time.perf_counter()
print("\n=== Fractional Knapsack - Problem 2 ===")
print("Maximum Value:", val2)
for i, frac in items2:
    print(f"Item {i}: {frac:.2f} of (weight={w2[i]}, value={v2[i]})")
print(f"Execution time using ChatGPT (Greedy Approach): {end_time - start_time:.8f} seconds")     
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
# import random
# import time
# # Generate 100 items with weights sorted and values strictly increasing
# random.seed(42)
# weights = sorted(random.randint(1, 150) for _ in range(100))

# values = []
# prev_value = 0
# for w in weights:
#     min_value = max(prev_value + 1, w + 1)
#     value = min_value + random.randint(0, 100)
#     values.append(value)
#     prev_value = value

# def knapsack_fractional(weights, values, W):
#     index = list(range(len(weights)))
#     ratio = [v / w for v, w in zip(values, weights)]
#     index.sort(key=lambda i: ratio[i], reverse=True)

#     max_value = 0
#     items = []

#     for i in index:
#         if weights[i] <= W:
#             W -= weights[i]
#             max_value += values[i]
#             items.append((i, 1))
#         else:
#             frac = W / weights[i]
#             max_value += values[i] * frac
#             items.append((i, frac))
#             break

#     return max_value, items

# if __name__ == "__main__":
#     capacity = 500
#     start_time = time.perf_counter()
#     max_val, selected = knapsack_fractional(weights, values, capacity)
#     end_time = time.perf_counter()

#     print("=== Fractional Knapsack (Greedy) ===")
#     print("Maximum Value:", round(max_val, 2))
#     print("Selected Items (index, fraction, weight, value):")
#     for i, frac in selected:
#         print(f"Item {i}: {frac:.2f} of (weight={weights[i]}, value={values[i]})")
#     print(f"Execution time using ChatGPT (Greedy Approach): {end_time - start_time:.8f} seconds") 