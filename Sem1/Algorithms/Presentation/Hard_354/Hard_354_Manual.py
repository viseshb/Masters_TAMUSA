#354. Russian Doll Envelopes
#https://leetcode.com/problems/russian-doll-envelopes/description/
from bisect import bisect_left
from typing import List
import time
class Solution:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        envelopes.sort(key=lambda arr: (arr[0], -arr[1]))
        lis = []

        for [width, height] in envelopes:
            i = bisect_left(lis, height)
            if i == len(lis):
                lis.append(height)
            else:
                lis[i] = height
        
        return len(lis)
                                               

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