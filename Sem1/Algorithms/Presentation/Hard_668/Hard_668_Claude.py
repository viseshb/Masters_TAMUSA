#668. Kth Smallest Number in Multiplication Table
#https://leetcode.com/problems/kth-smallest-number-in-multiplication-table/

import time

class Solution:
    def findKthNumber(self, m, n, k):
        # Use binary search to find the kth smallest number
        left, right = 1, m * n
        
        while left < right:
            mid = left + (right - left) // 2
            count = self.count_less_or_equal(mid, m, n)
            
            if count < k:
                left = mid + 1
            else:
                right = mid
        
        return left
    
    def count_less_or_equal(self, target, m, n):
        # Count numbers less than or equal to target in the multiplication table
        count = 0
        for i in range(1, m + 1):
            # For each row, count how many numbers are <= target
            count += min(target // i, n)
        return count
    

m = 3
n =3
k =5
sol = Solution()

# Run multiple iterations
iterations = 10
total_time = 0.0
result = None

for _ in range(iterations):
    start_time = time.perf_counter()
    result = sol.findKthNumber(m,n,k)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time
    print(f"Execution time: {execution_time:.12f} seconds")

average_time = total_time / iterations
print("\nResult:", result)
print(f"Average execution time over {iterations} runs: {average_time:.12f} seconds")  