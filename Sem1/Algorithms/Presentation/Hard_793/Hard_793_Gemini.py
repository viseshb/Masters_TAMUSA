#793. Preimage Size of Factorial Zeroes Function
#https://leetcode.com/problems/preimage-size-of-factorial-zeroes-function/


import time
class Solution:
    def preimageSizeFZF(self, k: int) -> int:
        def trailingZeroes(n):
            count = 0
            while n > 0:
                n //= 5
                count += n
            return count

        def find_bound(target):
            left, right = 0, 5 * (target + 1)
            while left < right:
                mid = (left + right) // 2
                if trailingZeroes(mid) < target + 1:
                    left = mid + 1
                else:
                    right = mid
            return left

        upper = find_bound(k)
        lower = find_bound(k - 1)
        return upper - lower
    
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
