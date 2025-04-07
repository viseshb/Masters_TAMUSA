#154. Find Minimum in Rotated Sorted Array II
#https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/

from typing import List
import time

class Solution:
    def findMin(self, nums: List[int]) -> int:
        s , e = 0 , len (nums) - 1 
        while s < e :
            m = s + (e - s ) // 2 
            if nums[m] == nums[s] and nums[m] == nums[e] :
                s += 1
                e -= 1
            elif nums[m] <= nums[e] :  e = m 
            else  :      s = m + 1 
        return nums [s] 
    
nums = [1,3,5]
sol = Solution()

# Run multiple iterations
iterations = 10
total_time = 0.0
result = None

for _ in range(iterations):
    start_time = time.perf_counter()
    result = sol.findMin(nums)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time
    print(f"Execution time: {execution_time:.12f} seconds")

average_time = total_time / iterations
print("\nResult:", result)
print(f"Average execution time over {iterations} runs: {average_time:.12f} seconds")