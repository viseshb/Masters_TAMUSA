#493. Reverse Pairs
#https://leetcode.com/problems/reverse-pairs/description/


import time 
class Solution:
    def reversePairs(self, nums):
        if not nums:
            return 0
        
        self.count = 0
        self.temp = []
        self.sort_and_count(nums, 0, len(nums) - 1)
        return self.count
    
    def sort_and_count(self, nums, start, end):
        if start >= end:
            return
        
        mid = start + (end - start) // 2
        self.sort_and_count(nums, start, mid)
        self.sort_and_count(nums, mid + 1, end)
        
        # Count reverse pairs using binary search
        j = mid + 1
        for i in range(start, mid + 1):
            # Use binary search to find the first position where nums[j] * 2 >= nums[i]
            j = self.binary_search(nums, j, end + 1, nums[i] / 2.0)
            self.count += j - (mid + 1)
        
        # Merge the sorted arrays
        self.merge(nums, start, mid, end)
    
    def binary_search(self, nums, left, right, target):
        # Find the first position where nums[pos] > target
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] <= target:
                left = mid + 1
            else:
                right = mid
        return left
    
    def merge(self, nums, start, mid, end):
        # Standard merge operation
        self.temp = [0] * (end - start + 1)
        i, j, k = start, mid + 1, 0
        
        while i <= mid and j <= end:
            if nums[i] <= nums[j]:
                self.temp[k] = nums[i]
                i += 1
            else:
                self.temp[k] = nums[j]
                j += 1
            k += 1
        
        while i <= mid:
            self.temp[k] = nums[i]
            i += 1
            k += 1
        
        while j <= end:
            self.temp[k] = nums[j]
            j += 1
            k += 1
        
        for k in range(len(self.temp)):
            nums[start + k] = self.temp[k]

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