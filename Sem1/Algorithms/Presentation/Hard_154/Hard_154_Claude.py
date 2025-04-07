#154. Find Minimum in Rotated Sorted Array II
#https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/

import time

class Solution:
    def findMin(self, nums):
        left, right = 0, len(nums) - 1
        
        while left < right:
            mid = left + (right - left) // 2
            
            # If the middle element is greater than the rightmost element,
            # the minimum must be in the right half
            if nums[mid] > nums[right]:
                left = mid + 1
            # If the middle element is less than the rightmost element,
            # the minimum must be in the left half (including mid)
            elif nums[mid] < nums[right]:
                right = mid
            # If they are equal, we can't be sure which half contains the minimum
            # but we can safely eliminate the rightmost element
            else:
                right -= 1
                
        return nums[left]
    
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
