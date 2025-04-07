#668. Kth Smallest Number in Multiplication Table
#https://leetcode.com/problems/kth-smallest-number-in-multiplication-table/

from typing import List
import time
class Solution:
    def findKthNumber(self, m: int, n: int, k: int) -> int:
        def countLessEqual(x: int) -> int:
            count = 0
            for i in range(1, m + 1):
                count += min(x // i, n)
            return count

        low, high = 1, m * n
        while low < high:
            mid = (low + high) // 2
            if countLessEqual(mid) < k:
                low = mid + 1
            else:
                high = mid
        return low


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