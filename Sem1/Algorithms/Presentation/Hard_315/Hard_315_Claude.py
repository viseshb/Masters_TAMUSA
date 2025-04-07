#315. Count of Smaller Numbers After Self
#https://leetcode.com/problems/count-of-smaller-numbers-after-self/description/

import time

class Solution:
    def countSmaller(self, nums):
        # Handle empty array case
        if not nums:
            return []
        
        # Create a list to store counts and pairs of (value, original index)
        counts = [0] * len(nums)
        pairs = [(nums[i], i) for i in range(len(nums))]
        
        # Merge sort with counting
        def merge_sort(pairs):
            if len(pairs) <= 1:
                return pairs
            
            # Divide array in half
            mid = len(pairs) // 2
            left = merge_sort(pairs[:mid])
            right = merge_sort(pairs[mid:])
            
            # Merge arrays while counting smaller elements
            merged = []
            right_count = 0
            i, j = 0, 0
            
            while i < len(left) and j < len(right):
                if left[i][0] > right[j][0]:
                    # Found a smaller element on right
                    merged.append(right[j])
                    right_count += 1
                    j += 1
                else:
                    # Current left element is >= right element
                    # All counted right elements are smaller than current left
                    counts[left[i][1]] += right_count
                    merged.append(left[i])
                    i += 1
            
            # Handle remaining elements
            while i < len(left):
                counts[left[i][1]] += right_count
                merged.append(left[i])
                i += 1
                
            while j < len(right):
                merged.append(right[j])
                j += 1
                
            return merged
        
        merge_sort(pairs)
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