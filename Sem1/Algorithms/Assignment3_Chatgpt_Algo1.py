# import time

# # Global counter for recursive calls
# recursive_calls = 0

# def rod_cutting_recursive(prices, n):
#     global recursive_calls
#     recursive_calls += 1
#     if n == 0:
#         return 0
#     max_revenue = 0
#     for i in range(1, n + 1):
#         max_revenue = max(max_revenue, prices[i - 1] + rod_cutting_recursive(prices, n - i))
#     return max_revenue

# prices = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
# test_lengths = [2, 4, 6, 8, 10]

# print("Recursive Approach (Brute-Force) Rod Cutting using ChatGPT")
# for n in test_lengths:
#     recursive_calls = 0  # reset counter for each test
#     start_time = time.perf_counter()
#     revenue = rod_cutting_recursive(prices, n)
#     end_time = time.perf_counter()
#     print(f"Rod length: {n} | Maximum revenue: {revenue} | Recursive calls: {recursive_calls} | Execution time: {end_time - start_time:.8f} seconds")
import time
import random

# Function to generate a strictly increasing price list for rod lengths 1 to n.
def generate_increasing_prices(n):
    prices = []
    current_price = 0
    for _ in range(n):
        # Increase price by a random integer between 1 and 10
        current_price += random.randint(1, 10)
        prices.append(current_price)
    return prices

# Global counter for recursive calls
recursive_calls = 0

def rod_cutting_recursive(prices, n):
    global recursive_calls
    recursive_calls += 1
    if n == 0:
        return 0
    max_revenue = 0
    for i in range(1, n + 1):
        max_revenue = max(max_revenue, prices[i - 1] + rod_cutting_recursive(prices, n - i))
    return max_revenue

# Simulation parameters for n = 100
n = 100
prices = generate_increasing_prices(n)
print("Algorithm 1: Recursive Approach (Brute-Force) using ChatGPT")
print("Generated Prices (length 1 to 100):")
print(prices)


recursive_calls = 0  # reset counter
start_time = time.perf_counter()
revenue = rod_cutting_recursive(prices, n)
end_time = time.perf_counter()
print(f"Rod length: {n} | Maximum revenue: {revenue} | Recursive calls: {recursive_calls} | Execution time: {end_time - start_time:.8f} seconds")


    
