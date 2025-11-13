"""
Pathfinding: Grid Navigation
Algorithm: A* (A-Star) Search

Description:
    Implements the A* search algorithm to find the shortest path on a grid
    containing obstacles. It utilizes a Euclidean distance heuristic and
    a priority queue to efficiently explore the search space.
"""

import heapq
import math

def heuristic(start, end):
    """Euclidean distance heuristic for A*."""
    return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)

def get_neighbors(position, grid):
    """Returns valid neighbors (including diagonals) for a given position."""
    row, col = position
    # 8-directional movement
    directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (-1,-1), (1,-1)]
    neighbors = []
    
    for row_dir, col_dir in directions:
        new_row, new_col = row + row_dir, col + col_dir
        
        # Check bounds
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            # Check obstacles (False = Walkable, True = Obstacle)
            if not grid[new_row][new_col]:
                neighbors.append((new_row, new_col))
    
    return neighbors

def find_shortest_path(start, goal, grid):
    # Validation: Check if start or end are obstacles
    if grid[start[0]][start[1]] or grid[goal[0]][goal[1]]:
        return None  

    # Priority Queue stores: (F-Score, G-Score, CurrentNode, ParentNode)
    queue = []
    heapq.heappush(queue, (heuristic(start, goal), 0, start, None))
    
    g_vals = {start: 0}
    parents = {start: None}
    visited_nodes = set()
    
    while queue:
        _, g, current_node, _ = heapq.heappop(queue)
        
        if current_node == goal:
            # Reconstruct path backwards
            path = []
            while current_node:
                path.append(current_node)
                current_node = parents[current_node]
            return path[::-1] # Reverse to get Start -> Goal
        
        if current_node in visited_nodes:
            continue
        
        visited_nodes.add(current_node)
        
        for neighbor in get_neighbors(current_node, grid):
            if neighbor in visited_nodes:
                continue
            
            # Cost to move to neighbor is always 1 (simplified cost)
            tentative_g = g + 1  
            
            if neighbor not in g_vals or tentative_g < g_vals[neighbor]:
                g_vals[neighbor] = tentative_g
                f_val = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(queue, (f_val, tentative_g, neighbor, current_node))
                parents[neighbor] = current_node
    
    return None 

if __name__ == '__main__':
    print("=== Heuristic Search Demo: A* Pathfinding ===")
    
    # 0 = Empty, 1 = Wall
    # 10x10 Grid with a wall in the middle
    grid = [[False] * 10 for _ in range(10)]
    
    # Build a wall at row 5
    for i in range(8):
        grid[i][5] = True 
        
    start_pos = (0, 0)
    end_pos = (0, 8)
    
    print(f"Start: {start_pos}, Goal: {end_pos}")
    print("Calculating path around obstacle...")
    
    path = find_shortest_path(start_pos, end_pos, grid)
    
    if path:
        print(f"Path found ({len(path)} steps):")
        print(path)
    else:
        print("No path found.")
