#410. Split Array Largest Sum
#https://leetcode.com/problems/split-array-largest-sum/description/


import time
from typing import List

class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        def is_valid(max_sum):
            count = 1
            current_sum = 0
            for num in nums:
                current_sum += num
                if current_sum > max_sum:
                    count += 1
                    current_sum = num
            return count <= k

        left, right = max(nums), sum(nums)
        while left < right:
            mid = (left + right) // 2
            if is_valid(mid):
                right = mid
            else:
                left = mid + 1
        return left
    
nums = [7,2,5,10,8]
k = 2
sol = Solution()

# Run multiple iterations
iterations = 10
total_time = 0.0
result = None

for _ in range(iterations):
    start_time = time.perf_counter()
    result = sol.splitArray(nums, k)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time
    print(f"Execution time: {execution_time:.12f} seconds")

average_time = total_time / iterations
print("\nResult:", result)
print(f"Average execution time over {iterations} runs: {average_time:.12f} seconds")     