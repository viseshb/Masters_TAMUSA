#315. Count of Smaller Numbers After Self
#https://leetcode.com/problems/count-of-smaller-numbers-after-self/description/



from typing import List
import time 

class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        def sort_and_count(enum):
            if len(enum) <= 1:
                return enum
            mid = len(enum) // 2
            left = sort_and_count(enum[:mid])
            right = sort_and_count(enum[mid:])
            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i][1] <= right[j][1]:
                    merged.append(left[i])
                    counts[left[i][0]] += j
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            while i < len(left):
                merged.append(left[i])
                counts[left[i][0]] += j
                i += 1
            while j < len(right):
                merged.append(right[j])
                j += 1
            return merged

        counts = [0] * len(nums)
        sort_and_count(list(enumerate(nums)))
        return counts
    
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