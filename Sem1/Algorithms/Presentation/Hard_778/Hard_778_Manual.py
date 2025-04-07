#778. Swim in Rising Water
#https://leetcode.com/problems/swim-in-rising-water/

from typing import List
import time
class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])

        if n == m == 1:
            return grid[0][0]
        
        def get_nexts(i, j, visited):
            for x, y in ((i - 1, j),
                         (i + 1, j),
                         (i, j - 1),
                         (i, j + 1)):
                if (
                    0 <= x < n
                    and 0 <= y < m
                    and (x, y) not in visited
                ):
                    yield (x, y)

        def check(value):
            q = [(0, 0)]
            visited = {(0, 0)}
            while q:
                i, j = q.pop()
                for x, y in get_nexts(i, j, visited):
                    if grid[x][y] > value:
                        continue
                    if x == n - 1 and y == m - 1:
                        return True
                    q.append((x, y))
                    visited.add((x, y))
            return False
        
        left = max(grid[0][0], grid[-1][-1])
        right = max(max(line) for line in grid)

        if check(left):
            return left
        
        while right - left > 1:
            middle = (left + right) // 2
            if check(middle):
                right = middle
            else:
                left = middle
        
        return right
    
grid =[[0,2],[1,3]]
sol = Solution()

# Run multiple iterations
iterations = 10
total_time = 0.0
result = None

for _ in range(iterations):
    start_time = time.perf_counter()
    result = sol.swimInWater(grid)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time
    print(f"Execution time: {execution_time:.12f} seconds")

average_time = total_time / iterations
print("\nResult:", result)
print(f"Average execution time over {iterations} runs: {average_time:.12f} seconds")  
   