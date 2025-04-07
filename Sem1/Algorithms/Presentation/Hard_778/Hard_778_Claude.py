#778. Swim in Rising Water
#https://leetcode.com/problems/swim-in-rising-water/
import time
class Solution:
    def swimInWater(self, grid):
        n = len(grid)
        
        # Helper function to check if we can reach bottom-right within time t
        def can_reach_destination(t):
            if grid[0][0] > t:  # If starting position is underwater
                return False
            
            visited = set([(0, 0)])
            queue = [(0, 0)]
            
            # Directions: up, right, down, left
            directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            
            while queue:
                x, y = queue.pop(0)
                
                if x == n - 1 and y == n - 1:  # Reached destination
                    return True
                
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    
                    # Check if valid cell and not visited yet
                    if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in visited:
                        # Check if the cell is not underwater at time t
                        if grid[nx][ny] <= t:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
            
            return False
        
        # Binary search to find the minimum time
        left = grid[0][0]  # Minimum possible time (starting elevation)
        right = max(max(row) for row in grid)  # Maximum possible time (highest elevation)
        
        while left < right:
            mid = (left + right) // 2
            if can_reach_destination(mid):
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