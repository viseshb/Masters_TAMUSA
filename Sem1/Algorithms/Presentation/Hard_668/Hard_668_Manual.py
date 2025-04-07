#668. Kth Smallest Number in Multiplication Table
#https://leetcode.com/problems/kth-smallest-number-in-multiplication-table/

import time

class Solution:
    def findKthNumber(self, m: int, n: int, k: int) -> int:
        lo, hi = 1, m*n
        while lo < hi:
            mid, count = (lo+hi)//2, 0
            # check how many numbers are smaller than mid
            for i in range(1, m+1):
                count += n if n<mid//i else mid//i
            if count>=k:  # target <= mid
                hi = mid
            else:  # target > mid
                lo = mid+1
        return lo
    

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
