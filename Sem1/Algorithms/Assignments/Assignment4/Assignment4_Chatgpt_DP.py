# import time

# def knapsack_01(weights, values, W):
#     n = len(weights)
#     dp = [[0] * (W + 1) for _ in range(n + 1)]

#     for i in range(1, n + 1):
#         for w in range(W + 1):
#             if weights[i-1] <= w:
#                 dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
#             else:
#                 dp[i][w] = dp[i-1][w]

#     res = dp[n][W]
#     w = W
#     items = []
#     for i in range(n, 0, -1):
#         if res <= 0:
#             break
#         if res != dp[i-1][w]:
#             items.append(i-1)
#             res -= values[i-1]
#             w -= weights[i-1]

#     return dp[n][W], items

# # Problem 1
# w1, v1, cap1 = [10, 20, 30], [60, 100, 120], 50
# start_time = time.perf_counter()
# val1, items1 = knapsack_01(w1, v1, cap1)
# print("=== 0/1 Knapsack - Problem 1 ===")
# print("Maximum Value:", val1)
# for i in items1:
#     print(f"Item {i}: weight={w1[i]}, value={v1[i]}")

# # Problem 2
# w2, v2, cap2 = [1, 2, 3, 5], [6, 11, 12, 14], 10
# val2, items2 = knapsack_01(w2, v2, cap2)
# end_time = time.perf_counter()
# print("\n=== 0/1 Knapsack - Problem 2 ===")
# print("Maximum Value:", val2)
# for i in items2:
#     print(f"Item {i}: weight={w2[i]}, value={v2[i]}")

# print(f"Execution time using ChatGPT (Dynamic Programming Approach) : {end_time - start_time:.8f} seconds")     
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
import random
import time

# Generate 100 items with weights sorted and values strictly increasing

weights = sorted(random.randint(1, 150) for _ in range(100))

values = []
prev_value = 0
for w in weights:
    min_value = max(prev_value + 1, w + 1)
    value = min_value + random.randint(0, 100)
    values.append(value)
    prev_value = value

def knapsack_01(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    res = dp[n][W]
    w = W
    items = []
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res != dp[i - 1][w]:
            items.append(i - 1)
            res -= values[i - 1]
            w -= weights[i - 1]

    return dp[n][W], items

if __name__ == "__main__":
    capacity = 500  
    start_time = time.perf_counter()
    max_val, selected = knapsack_01(weights, values, capacity)
    end_time = time.perf_counter()

    print("=== 0/1 Knapsack (DP) — Fixed Capacity ===")
    print("Maximum Value:", max_val)
    
    total_weight = sum(weights[i] for i in selected)
    print("Total Weight Used:", total_weight)

    print("Selected Items (index, weight, value):")
    for i in selected:
        print(f"Item {i}: weight={weights[i]}, value={values[i]}")
    print(f"Execution time using ChatGPT (Dynamic Programming Approach) : {end_time - start_time:.8f} seconds")    
