#862. Shortest Subarray with Sum at Least K
#https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/
import time
from typing import List

from typing import *
import collections

class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        result = n + 1  # Initialize to a value larger than any possible answer
        
        # Create prefix sum array
        prefix_sum = [0]
        for num in nums:
            prefix_sum.append(prefix_sum[-1] + num)
        
        # Use a monotonic queue to keep track of potential starting points
        monoq = collections.deque()
        
        for end, curr_sum in enumerate(prefix_sum):
            # Find the shortest subarray that ends at position 'end'
            while monoq and curr_sum - prefix_sum[monoq[0]] >= k:
                result = min(result, end - monoq.popleft())
            
            # Maintain monotonic increasing queue of indices
            # If current sum is smaller than the last sum in queue, we remove the last
            # This ensures we always choose the best starting point
            while monoq and prefix_sum[monoq[-1]] >= curr_sum:
                monoq.pop()
            
            monoq.append(end)
        
        return result if result <= n else -1

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
