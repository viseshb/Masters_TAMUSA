#778. Swim in Rising Water
#https://leetcode.com/problems/swim-in-rising-water/


import time
from typing import List

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)

        def can_reach(time):
            visited = [[False] * n for _ in range(n)]
            queue = [(0, 0)]
            visited[0][0] = True

            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

            while queue:
                x, y = queue.pop(0)

                if x == n - 1 and y == n - 1:
                    return True

                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] <= time:
                        visited[nx][ny] = True
                        queue.append((nx, ny))

            return False

        left, right = max(max(row) for row in grid), n * n
        while left < right:
            mid = (left + right) // 2
            if can_reach(mid):
                right = mid
            else:
                left = mid + 1

        return left
    


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