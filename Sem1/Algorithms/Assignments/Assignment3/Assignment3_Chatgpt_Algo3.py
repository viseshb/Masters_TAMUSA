# import time

# def rod_cutting_bottom_up(prices, n):
#     iterations = 0  # local counter for loop iterations
#     dp = [0] * (n + 1)
#     for j in range(1, n + 1):
#         max_revenue = 0
#         for i in range(1, j + 1):
#             iterations += 1
#             max_revenue = max(max_revenue, prices[i - 1] + dp[j - i])
#         dp[j] = max_revenue
#     return dp[n], iterations

# prices = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
# test_lengths =[2, 4, 6, 8, 10] 

# print("Bottom-Up Rod Cutting using ChatGPT")
# for n in test_lengths:
#     start_time = time.perf_counter()
#     revenue, iterations = rod_cutting_bottom_up(prices, n)
#     end_time = time.perf_counter()
#     print(f"Rod length: {n} | Maximum revenue: {revenue} | Iterations: {iterations} | Execution time: {end_time - start_time:.8f} seconds")
import time
import random

# Function to generate a strictly increasing price list for rod lengths 1 to n.
def generate_increasing_prices(n):
    prices = []
    current_price = 0
    for _ in range(n):
        current_price += random.randint(1, 10)
        prices.append(current_price)
    return prices

def rod_cutting_bottom_up(prices, n):
    iterations = 0  # local counter for inner loop iterations
    dp = [0] * (n + 1)
    for j in range(1, n + 1):
        max_revenue = 0
        for i in range(1, j + 1):
            iterations += 1
            max_revenue = max(max_revenue, prices[i - 1] + dp[j - i])
        dp[j] = max_revenue
    return dp[n], iterations

# Simulation parameters for n = 100
n = 100
prices = generate_increasing_prices(n)
print("\nAlgorithm 3: Bottom-Up DP using ChatGPT")
print("Generated Prices (length 1 to 100):")
print(prices)

start_time = time.perf_counter()
revenue, iterations = rod_cutting_bottom_up(prices, n)
end_time = time.perf_counter()
print(f"Rod length: {n} | Maximum revenue: {revenue} | Iterations: {iterations} | Execution time: {end_time - start_time:.8f} seconds")
