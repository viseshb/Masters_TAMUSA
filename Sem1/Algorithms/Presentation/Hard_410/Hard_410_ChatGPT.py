#410. Split Array Largest Sum
#https://leetcode.com/problems/split-array-largest-sum/description/


from typing import List
import time 

class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        def canSplit(max_sum: int) -> bool:
            count, curr_sum = 1, 0
            for num in nums:
                if curr_sum + num > max_sum:
                    count += 1
                    curr_sum = num
                    if count > k:
                        return False
                else:
                    curr_sum += num
            return True

        low, high = max(nums), sum(nums)
        result = high

        while low <= high:
            mid = (low + high) // 2
            if canSplit(mid):
                result = mid
                high = mid - 1
            else:
                low = mid + 1

        return result

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