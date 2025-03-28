# import time

# prices = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
# n_values = [2, 4, 6, 8, 10]

# def recursive_rod_cut(prices, n):
#     calls = [0]
#     def _recursive_rod_cut(prices, n, calls):
#         calls[0] += 1
#         if n == 0:
#             return 0
#         max_revenue = -float('inf')
#         for i in range(1, n + 1):
#             max_revenue = max(max_revenue, prices[i - 1] + _recursive_rod_cut(prices, n - i, calls))
#         return max_revenue

#     start_time = time.perf_counter()
#     revenue = _recursive_rod_cut(prices, n, calls)
#     end_time = time.perf_counter()
#     execution_time = end_time - start_time
#     return revenue, calls[0], execution_time

# print("Recursive Approach (Brute-Force) Rod Cutting Gemini 2.0 Flash:")
# for n in n_values:
#     revenue, calls, execution_time = recursive_rod_cut(prices, n)
#     print(f"Rod length: {n} | Maximum revenue: {revenue} | Recursive calls: {calls} | Execution time: {execution_time:.8f} seconds")
import time
import random

def generate_increasing_prices(length):
    """Generates a list of increasing prices for rod lengths."""
    prices = []
    current_price = 1
    for i in range(1, length + 1):
        prices.append(current_price)
        current_price += random.randint(1, 5)  # Increase price by a random amount
    return prices

rod_length = 100
prices = generate_increasing_prices(rod_length)

# Algorithm 1: Recursive Rod Cut
def recursive_rod_cut(prices, n):
    calls = [0]
    def _recursive_rod_cut(prices, n, calls):
        calls[0] += 1
        if n == 0:
            return 0
        max_revenue = -float('inf')
        for i in range(1, n + 1):
            max_revenue = max(max_revenue, prices[i - 1] + _recursive_rod_cut(prices, n - i, calls))
        return max_revenue

    start_time = time.perf_counter()
    revenue = _recursive_rod_cut(prices, n, calls)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return revenue, calls[0], execution_time

print("Recursive Approach (Brute-Force) Rod Cutting:")
revenue, calls, execution_time = recursive_rod_cut(prices, rod_length)
print(f"Rod length: {rod_length} | Maximum revenue: {revenue} | Recursive calls: {calls} | Execution time: {execution_time:.8f} seconds")
