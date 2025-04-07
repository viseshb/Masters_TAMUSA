#793. Preimage Size of Factorial Zeroes Function
#https://leetcode.com/problems/preimage-size-of-factorial-zeroes-function/


import time

class Solution:
    def preimageSizeFZF(self, k: int) -> int:
        left = 0
        right = 5 * (k + 1)
        
        while left <= right:
            mid = left + (right - left) // 2
            n = mid
            count = 0
            
            # Calculate the number of trailing zeros in mid!
            while n:
                n //= 5
                count += n
            
            # Adjust the binary search range based on the count of trailing zeros
            if count < k:
                left = mid + 1
            elif count > k:
                right = mid - 1
            else:
                # If count == k, it means there are exactly 5 numbers that will
                # produce the same number of trailing zeros
                return 5
        
        # If no such number is found, return 0
        return 0
    
k= 3
sol = Solution()

# Run multiple iterations
iterations = 10
total_time = 0.0
result = None

for _ in range(iterations):
    start_time = time.perf_counter()
    result = sol.preimageSizeFZF(k)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time
    print(f"Execution time: {execution_time:.12f} seconds")

average_time = total_time / iterations
print("\nResult:", result)
print(f"Average execution time over {iterations} runs: {average_time:.12f} seconds")      