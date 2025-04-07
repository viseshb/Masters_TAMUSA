#354. Russian Doll Envelopes
#https://leetcode.com/problems/russian-doll-envelopes/description/

import time
class Solution:
    def maxEnvelopes(self, envelopes):
        if not envelopes:
            return 0
        
        # Sort by width (ascending) and then by height (descending)
        # This handles cases where widths are equal but heights differ
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        
        # Now we find the longest increasing subsequence on heights
        dp = []
        
        for _, h in envelopes:
            # Binary search to find the position to insert current height
            left, right = 0, len(dp)
            while left < right:
                mid = (left + right) // 2
                if dp[mid] < h:
                    left = mid + 1
                else:
                    right = mid
            
            # If we're at the end of dp, append height
            if left == len(dp):
                dp.append(h)
            # Otherwise, replace the element at the found position
            else:
                dp[left] = h
        
        # Length of dp array is the maximum number of envelopes
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