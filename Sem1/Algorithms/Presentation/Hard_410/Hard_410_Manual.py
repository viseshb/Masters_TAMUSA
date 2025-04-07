#410. Split Array Largest Sum
#https://leetcode.com/problems/split-array-largest-sum/description/
from typing import List
import time

class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        def count(nums,mid):
            students=1
            totalstudents=0
            for i in range(0,len(nums)):
                if totalstudents+nums[i]<=mid:
                    totalstudents+=nums[i]
                else:
                    students+=1
                    totalstudents=nums[i]
            return students
        n=len(nums)
        if k>n: return -1
        low=max(nums)
        high=sum(nums)
        while low<=high:
            mid=(low+high)//2
            students=count(nums,mid)
            if students>k:
                low=mid+1
            else:
                high=mid-1
        return low
    
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
