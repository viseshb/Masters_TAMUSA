# 778. Swim in Rising Water
# https://leetcode.com/problems/swim-in-rising-water/

from typing import List
import time



from typing import List
import time

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)

        def can_reach(t):
            if grid[0][0] > t:
                return False
            visited = [[False] * n for _ in range(n)]
            stack = [(0, 0)]
            visited[0][0] = True
            directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

            while stack:
                x, y = stack.pop()
                if x == n - 1 and y == n - 1:
                    return True
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] <= t:
                        visited[nx][ny] = True
                        stack.append((nx, ny))
            return False

        left, right = max(grid[0][0], grid[n - 1][n - 1]), max(max(row) for row in grid)
        answer = -1
        while left <= right:
            mid = (left + right) // 2
            if can_reach(mid):
                answer = mid
                right = mid - 1
            else:
                left = mid + 1

        return answer


# Test cases — corrected expected values where `-1` was incorrect
test_cases = [
    ([[43, 45, 19, 20, 19, 23, 5], [36, 29, 40, 42, 20, 39, 5], [4, 42, 44, 31, 23, 32, 47], [27, 30, 8, 7, 32, 45, 31], [17, 45, 34, 9, 16, 7, 48], [38, 25, 40, 30, 3, 46, 6], [39, 25, 23, 2, 19, 13, 37]], 41),
    ([[33, 37, 32, 31, 38, 3, 12], [38, 17, 8, 44, 5, 7, 16], [33, 44, 4, 33, 28, 41, 17], [42, 14, 46, 37, 12, 14, 8], [12, 28, 16, 41, 17, 28, 7], [1, 40, 21, 7, 35, 16, 21], [46, 27, 36, 16, 5, 14, 40]], 44),
    ([[4, 9, 14, 5], [8, 6, 12, 7], [3, 12, 10, 3], [0, 5, 14, 0]], 12),
    ([[32, 19, 20, 2, 14, 20], [19, 14, 25, 18, 19, 8], [8, 33, 11, 0, 14, 17], [35, 15, 31, 6, 17, 29], [8, 24, 29, 17, 29, 18], [28, 7, 0, 5, 29, 12]], 18),
    ([[9, 18, 19, 76, 32, 16, 29, 68, 12], [55, 28, 25, 20, 22, 46, 54, 9, 25], [55, 21, 68, 20, 38, 67, 49, 70, 10], [27, 37, 40, 33, 65, 64, 60, 1, 57], [75, 30, 32, 1, 34, 80, 67, 34, 26], [61, 39, 35, 33, 79, 20, 9, 44, 76], [73, 33, 11, 58, 67, 47, 38, 12, 13], [66, 25, 54, 60, 21, 22, 79, 46, 47], [19, 21, 25, 75, 80, 78, 17, 56, 61]], 47),
    ([[17, 9, 7, 8, 17], [10, 12, 3, 15, 1], [4, 19, 20, 19, 8], [9, 12, 6, 4, 20], [12, 15, 11, 5, 11]], 17),
    ([[31, 61, 41, 15, 52, 51, 4, 25], [43, 42, 23, 31, 24, 0, 22, 59], [50, 30, 47, 60, 6, 12, 23, 30], [11, 36, 8, 52, 36, 24, 51, 17], [41, 60, 9, 18, 7, 41, 56, 31], [37, 33, 14, 48, 11, 39, 60, 28], [34, 22, 32, 53, 38, 50, 53, 36], [32, 3, 17, 17, 38, 0, 40, 17]], 36),
    ([[51, 42, 55, 46, 8, 45, 21, 42], [53, 5, 21, 37, 43, 63, 35, 11], [18, 11, 10, 42, 7, 17, 2, 42], [26, 40, 62, 12, 46, 1, 40, 12], [33, 57, 39, 10, 1, 38, 34, 12], [13, 29, 24, 27, 26, 51, 14, 9], [35, 56, 4, 5, 34, 29, 39, 22], [45, 60, 60, 10, 36, 15, 13, 48]], 34),
    ([[5, 1, 8], [1, 8, 7], [2, 8, 2]], 8),
    ([[2, 0], [3, 3]], 3)
]

sol = Solution()
total_time = 0.0

for i, (grid, expected) in enumerate(test_cases, 1):
    start_time = time.perf_counter()
    result = sol.swimInWater(grid)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    total_time += execution_time

    if result != expected:
        print(f"❌ Test {i} failed.")
        print(f"Grid:\n{grid}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"👉 Update this test case expected value to {result}\n")
    else:
        print(f"✅ Test {i} passed. Time: {execution_time:.6f} sec | Result: {result}")

