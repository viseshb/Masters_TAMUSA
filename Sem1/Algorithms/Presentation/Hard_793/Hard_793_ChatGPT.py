#793. Preimage Size of Factorial Zeroes Function
#https://leetcode.com/problems/preimage-size-of-factorial-zeroes-function/


from typing import *
import time
class Solution:
    def preimageSizeFZF(self, k: int) -> int:
        def countTrailingZeroes(x: int) -> int:
            count = 0
            while x > 0:
                x //= 5
                count += x
            return count

        def binarySearch(target: int) -> int:
            low, high = 0, 5 * (target + 1)
            while low < high:
                mid = (low + high) // 2
                if countTrailingZeroes(mid) < target:
                    low = mid + 1
                else:
                    high = mid
            return low

        # The number of x such that f(x) = k is binarySearch(k + 1) - binarySearch(k)
        return 5 if countTrailingZeroes(binarySearch(k)) == k else 0


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