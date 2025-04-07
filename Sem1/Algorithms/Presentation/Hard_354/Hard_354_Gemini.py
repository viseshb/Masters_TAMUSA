#354. Russian Doll Envelopes
#https://leetcode.com/problems/russian-doll-envelopes/description/


from typing import List
import time 
class Solution:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        heights = [h for w, h in envelopes]
        dp = []

        def binary_search(target):
            left, right = 0, len(dp) - 1
            while left <= right:
                mid = (left + right) // 2
                if dp[mid] == target:
                    return mid
                elif dp[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return left

        for height in heights:
            idx = binary_search(height)
            if idx == len(dp):
                dp.append(height)
            else:
                dp[idx] = height
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