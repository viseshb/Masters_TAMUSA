import time

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

prices = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
test_lengths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("Algorithm 1: Recursive Approach (Brute-Force) Rod Cutting")
for n in test_lengths:
    recursive_calls = 0  # reset counter for each test
    start_time = time.perf_counter()
    revenue = rod_cutting_recursive(prices, n)
    end_time = time.perf_counter()
    print(f"Rod length: {n} | Maximum revenue: {revenue} | Recursive calls: {recursive_calls} | Execution time: {end_time - start_time:.6f} seconds")
