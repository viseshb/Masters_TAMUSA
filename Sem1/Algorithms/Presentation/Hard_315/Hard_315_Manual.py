#315. Count of Smaller Numbers After Self
#https://leetcode.com/problems/count-of-smaller-numbers-after-self/description/

from bisect import bisect_left
from typing import List
import time


class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:

        arr, ans = sorted(nums), []           #  <-- 1)
        
        for num in nums:
            i = bisect_left(arr,num)          #  <-- 2a)
            ans.append(i)                     #  <-- 2b)
            del arr[i]                        #  <-- 2c)
            
        return ans                            #  <-- 3)
    
nums = [5,2,6,1]
sol = Solution()

# Run multiple iterations
iterations = 10
total_time = 0.0
result = None

for _ in range(iterations):
    start_time = time.perf_counter()
    result = sol.countSmaller(nums)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time
    print(f"Execution time: {execution_time:.12f} seconds")

average_time = total_time / iterations
print("\nResult:", result)
print(f"Average execution time over {iterations} runs: {average_time:.12f} seconds")  