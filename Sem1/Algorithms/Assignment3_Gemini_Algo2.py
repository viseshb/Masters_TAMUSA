# Code 2: Memoized (top-down) implementation of the Rod Cutting problem.
import time
prices = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
n_values = [2, 4, 6, 8, 10]

def memoized_rod_cut(prices, n):
    memo = [-float('inf')] * (n + 1)
    calls = [0]
    def _memoized_rod_cut_aux(prices, n, memo, calls):
        calls[0] += 1
        if n == 0:
            return 0
        if memo[n] >= 0:
            return memo[n]
        max_revenue = -float('inf')
        for i in range(1, n + 1):
            max_revenue = max(max_revenue, prices[i - 1] + _memoized_rod_cut_aux(prices, n - i, memo, calls))
        memo[n] = max_revenue
        return max_revenue

    start_time = time.perf_counter()
    revenue = _memoized_rod_cut_aux(prices, n, memo, calls)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return revenue, calls[0], execution_time

print("Memoized Cut Rod using Gemini 2.0 Flash:")
for n in n_values:
    revenue, calls, execution_time = memoized_rod_cut(prices, n)
    print(f"Rod length: {n} | Maximum revenue: {revenue} | Recursive calls: {calls} | Execution time: {execution_time:.8f} seconds")