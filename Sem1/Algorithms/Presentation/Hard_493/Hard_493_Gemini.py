#493. Reverse Pairs
#https://leetcode.com/problems/reverse-pairs/description/

from typing import List
import bisect
import time

class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        sorted_nums = []
        count = 0
        for num in reversed(nums):
            count += bisect.bisect_left(sorted_nums, num / 2)
            bisect.insort(sorted_nums, num)
        return count
    
nums = [1,3,2,3,1]

sol = Solution()

# Run multiple iterations
iterations = 10
total_time = 0.0
result = None

for _ in range(iterations):
    start_time = time.perf_counter()
    result = sol.reversePairs(nums)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time
    print(f"Execution time: {execution_time:.12f} seconds")

average_time = total_time / iterations
print("\nResult:", result)
print(f"Average execution time over {iterations} runs: {average_time:.12f} seconds")       