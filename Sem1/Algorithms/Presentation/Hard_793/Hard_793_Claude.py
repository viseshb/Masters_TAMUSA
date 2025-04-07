#793. Preimage Size of Factorial Zeroes Function
#https://leetcode.com/problems/preimage-size-of-factorial-zeroes-function/

import time
class Solution:
    def preimageSizeFZF(self, k):
        # Function to count trailing zeros in n!
        def trailingZeros(n):
            count = 0
            divisor = 5
            while divisor <= n:
                count += n // divisor
                divisor *= 5
            return count
        
        # Binary search to find the smallest number with at least k trailing zeros
        def search(k):
            left, right = 0, 5 * k + 1  # Upper bound is sufficient
            
            while left < right:
                mid = (left + right) // 2
                zeros = trailingZeros(mid)
                
                if zeros < k:
                    left = mid + 1
                else:
                    right = mid
            
            return left
        
        # Find first number with k trailing zeros and first with k+1 trailing zeros
        first_with_k = search(k)
        first_with_k_plus_1 = search(k + 1)
        
        # Count of numbers with exactly k trailing zeros
        return first_with_k_plus_1 - first_with_k
    

k= 3
sol = Solution()

# Run multiple iterations
iterations = 10
total_time = 0.0
result = None

for _ in range(iterations):
    start_time = time.perf_counter()
    result = sol.preimageSizeFZF(k)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time
    print(f"Execution time: {execution_time:.12f} seconds")

average_time = total_time / iterations
print("\nResult:", result)
print(f"Average execution time over {iterations} runs: {average_time:.12f} seconds")     