#493. Reverse Pairs
#https://leetcode.com/problems/reverse-pairs/description/
from typing import List
import time
import bisect
import math

class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        done, ans = [], 0
        for n in nums:
            if done and n * 2 < done[-1]:
                ans += self.binarySearch(n, done, 0, len(done) - 1)
            bisect.insort(done, n)
        return ans

    def binarySearch(self, n: int, done: List[int], lo: int, hi: int) -> int:
        if lo >= hi:
            if hi > n * 2:
                return len(done) - hi
            return len(done) - lo
        
        m = math.floor(lo + (hi - lo) / 2)
        if done[m] > n * 2:
            return self.binarySearch(n, done, lo, m) 
        else:
            return self.binarySearch(n, done, m + 1, hi) 
        
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

