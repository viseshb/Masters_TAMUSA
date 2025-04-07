#862. Shortest Subarray with Sum at Least K
#https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/

import time

from typing import List

class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        left, right = 1, n
        result = float('inf')

        while left <= right:
            mid = (left + right) // 2
            found = False
            for i in range(n - mid + 1):
                sub_sum = sum(nums[i:i + mid])
                if sub_sum >= k:
                    result = min(result, mid)
                    found = True
                    break

            if found:
                right = mid - 1
            else:
                left = mid + 1

        return result if result != float('inf') else -1
    

nums =[1,2]
k = 4
sol = Solution()

# Run multiple iterations
iterations = 10
total_time = 0.0
result = None

for _ in range(iterations):
    start_time = time.perf_counter()
    result = sol.shortestSubarray(nums, k)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time
    print(f"Execution time: {execution_time:.12f} seconds")

average_time = total_time / iterations
print("\nResult:", result)
print(f"Average execution time over {iterations} runs: {average_time:.12f} seconds")     
