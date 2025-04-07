#862. Shortest Subarray with Sum at Least K
#https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/


import time
from typing import List
from collections import deque

class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        prefix_sums = [0] * (n + 1)
        
        for i in range(n):
            prefix_sums[i + 1] = prefix_sums[i] + nums[i]
        
        def check(length: int) -> bool:
            min_prefix = prefix_sums[0]
            for i in range(length, len(prefix_sums)):
                if prefix_sums[i] - prefix_sums[i - length] >= k:
                    return True
            return False
        
        left, right = 1, n
        result = -1

        while left <= right:
            mid = (left + right) // 2
            if check(mid):
                result = mid
                right = mid - 1
            else:
                left = mid + 1
        
        return result
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