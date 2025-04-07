#354. Russian Doll Envelopes
#https://leetcode.com/problems/russian-doll-envelopes/description/

from typing import List
import time 
class Solution:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        def binary_search(dp: List[int], target: int) -> int:
            low, high = 0, len(dp) - 1
            while low <= high:
                mid = (low + high) // 2
                if dp[mid] < target:
                    low = mid + 1
                else:
                    high = mid - 1
            return low  # the first index where dp[i] >= target

        # Sort by width ascending and height descending
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        
        # Extract only heights
        heights = [h for _, h in envelopes]

        dp = []
        for h in heights:
            idx = binary_search(dp, h)
            if idx == len(dp):
                dp.append(h)
            else:
                dp[idx] = h
        return len(dp)

envelopes = [[5,4],[6,4],[6,7],[2,3]]
sol = Solution()

# Run multiple iterations
iterations = 10
total_time = 0.0
result = None

for _ in range(iterations):
    start_time = time.perf_counter()
    result = sol.maxEnvelopes(envelopes)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time
    print(f"Execution time: {execution_time:.12f} seconds")

average_time = total_time / iterations
print("\nResult:", result)
print(f"Average execution time over {iterations} runs: {average_time:.12f} seconds")   