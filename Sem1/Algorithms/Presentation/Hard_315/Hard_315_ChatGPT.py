#315. Count of Smaller Numbers After Self
#https://leetcode.com/problems/count-of-smaller-numbers-after-self/description/


from typing import List
import time
class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        def merge_sort(enum):
            mid = len(enum) // 2
            if mid:
                left, right = merge_sort(enum[:mid]), merge_sort(enum[mid:])
                merged = []
                i = j = 0
                while i < len(left) or j < len(right):
                    if j == len(right) or (i < len(left) and left[i][1] <= right[j][1]):
                        smaller[left[i][0]] += j
                        merged.append(left[i])
                        i += 1
                    else:
                        merged.append(right[j])
                        j += 1
                return merged
            return enum

        smaller = [0] * len(nums)
        indexed_nums = list(enumerate(nums))
        merge_sort(indexed_nums)
        return smaller

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