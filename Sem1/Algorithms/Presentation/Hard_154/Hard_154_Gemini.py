#154. Find Minimum in Rotated Sorted Array II
#https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/

from typing import List
import time
class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            elif nums[mid] < nums[right]:
                right = mid
            else:
                right -= 1
        return nums[left]
    

sol = Solution()

test_cases = [
    ([-4980, -2712, -2612, -2607, 43, 2228, 2681, 2689, 2804, 3113, 3705, 4816], -4980),
    ([-1819, -1365, -734, 1161, 3974], -1819),
    ([-4412, -3929, -3673, -3658, 23, 663, 1787, 2179, 2895, 3169, 3569, 4692], -4412),
    ([2377, 3944, 4662], 2377),
    ([-4440, -3786, -3156, -2497, -2160, -1581, -1541, -1074, -463, 505, 2038, 2218, 2545, 3863, 4004, 4496, 4691], -4440),
    ([-3574, -3278, -3213, -1463, -1067, -851, -510, -270, 318, 341, 1820, 1910, 2960, 3877, 4503, 4732], -3574),
    ([-4383, -4338, -4042, -3137, -3068, 818, 830, 2518, 3859, 4557], -4383),
    ([-2160, -1623, -1604, -1414, -676, -481, -265, 1280, 3944], -2160),
    ([933, 3357], 933),
    ([-4820, -3449, -2942, -1671, 505, 826, 2029, 2566, 2992, 4473], -4820)
]
total_time = 0.0
result = None

for nums, expected in test_cases:
    start_time = time.perf_counter()
    result = sol.findMin(nums)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time
    assert result == expected, f"Test failed for nums={nums}. Expected {expected}, got {result}"
    print(f"Test passed for nums={nums}. Execution time: {execution_time:.12f} seconds")

print(f"\nAll test cases passed successfully!")
print(f"Total execution time for all test cases: {total_time:.12f} seconds")