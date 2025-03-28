import time

prices = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
n_values = [2, 4, 6, 8, 10]

# Code 3: Bottom-up cut-rod algorithm.
def bottom_up_cut_rod(prices, n):
    revenue = [0] * (n + 1)
    cuts = [0] * (n + 1)
    iterations = 0

    start_time = time.perf_counter()
    for j in range(1, n + 1):
        max_revenue = -float('inf')
        for i in range(1, j + 1):
            iterations += 1
            if max_revenue < prices[i - 1] + revenue[j - i]:
                max_revenue = prices[i - 1] + revenue[j - i]
                cuts[j] = i
        revenue[j] = max_revenue
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    def get_cuts(cuts, n):
        cut_list = []
        while n > 0:
            cut_list.append(cuts[n])
            n = n - cuts[n]
        return cut_list

    return revenue[n], iterations, execution_time

print("Bottom-Up Rod Cutting using Gemini 2.0 Flash")
for n in n_values:
    revenue, iterations, execution_time = bottom_up_cut_rod(prices, n)
    print(f"Rod length: {n} | Maximum revenue: {revenue} | Iterations: {iterations} | Execution time: {execution_time:.8f} seconds")