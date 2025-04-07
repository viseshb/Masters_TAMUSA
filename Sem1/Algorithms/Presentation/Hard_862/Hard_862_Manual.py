#862. Shortest Subarray with Sum at Least K
#https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/

from bisect import bisect_right
from cmath import inf
import time
from typing import List
class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        loc = {0: -1}
        stack = [0] # increasing stack
        ans, prefix = inf, 0
        for i, x in enumerate(nums): 
            prefix += x
            ii = bisect_right(stack, prefix - k)
            if ii: ans = min(ans, i - loc[stack[ii-1]])
            loc[prefix] = i
            while stack and stack[-1] >= prefix: stack.pop()
            stack.append(prefix)
        return ans if ans < inf else -1
    

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