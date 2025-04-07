#778. Swim in Rising Water
#https://leetcode.com/problems/swim-in-rising-water/


from typing import List
import heapq
import time
class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)

        def canReach(t: int) -> bool:
            if grid[0][0] > t:
                return False
            visited = [[False] * n for _ in range(n)]
            stack = [(0, 0)]
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            while stack:
                i, j = stack.pop()
                if (i, j) == (n - 1, n - 1):
                    return True
                for dx, dy in directions:
                    x, y = i + dx, j + dy
                    if 0 <= x < n and 0 <= y < n and not visited[x][y] and grid[x][y] <= t:
                        visited[x][y] = True
                        stack.append((x, y))
            return False

        low, high = grid[0][0], max(max(row) for row in grid)
        while low < high:
            mid = (low + high) // 2
            if canReach(mid):
                high = mid
            else:
                low = mid + 1
        return low
    

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
