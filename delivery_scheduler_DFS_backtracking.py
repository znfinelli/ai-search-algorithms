"""
Constraint Satisfaction: Robot Delivery Scheduler
Algorithm: Depth-First Search (DFS) with Backtracking

Description:
    Solves a scheduling problem where a robot must visit a set of locations
    (deliveries) within specific deadlines. It compares two approaches:
    1. Standard DFS Backtracking
    2. Ordered DFS (Heuristic: Earliest Deadline & Shortest Distance)
"""

import math

def euclid_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def dfs_backtracking(deliveries, visited, path_indices, arrival_times, evaluations, current_pos, current_time, depth, limit_reached):
    """
    Standard DFS that tries branches in index order.
    """
    if evaluations >= 500000:
        if not limit_reached[0]:
            print('\n[!] 500,000 evaluations reached (cutoff).')
            limit_reached[0] = True
        return False, path_indices, arrival_times, evaluations
    
    # Base Case: All deliveries made
    if depth == len(deliveries):  
        return True, path_indices, arrival_times, evaluations
    
    for i in range(len(deliveries)):
        if i not in visited:
            evaluations += 1
            
            # Heuristic cutoff check again to catch deep recursion
            if evaluations >= 500000:
                 return False, path_indices, arrival_times, evaluations
            
            x, y, deadline = deliveries[i]
            travel_time = euclid_distance(current_pos[0], current_pos[1], x, y)
            arrival_time = current_time + travel_time
            
            # Constraint Check: Can we meet the deadline?
            if arrival_time <= deadline:
                # Forward Step
                visited.add(i)
                path_indices.append(i + 1)
                arrival_times.append(arrival_time)
                
                # Recursive Step
                found, path_indices, arrival_times, evaluations = dfs_backtracking(
                    deliveries, visited, path_indices, arrival_times, 
                    evaluations, (x, y), arrival_time, depth + 1, limit_reached
                )
                
                if found:
                    return True, path_indices, arrival_times, evaluations
                
                # Backtracking Step
                visited.remove(i)
                path_indices.pop()
                arrival_times.pop()
    
    return False, path_indices, arrival_times, evaluations

def dfs_backtracking_ordered(deliveries, visited, path_indices, arrival_times, evaluations, current_pos, current_time, depth, limit_reached):
    """
    Optimized DFS that orders children by a Heuristic (Deadline, Distance).
    """
    if evaluations >= 500000:
        return False, path_indices, arrival_times, evaluations
    
    if depth == len(deliveries):  
        return True, path_indices, arrival_times, evaluations
    
    # Heuristic: Sort remaining tasks by (Deadline ASC, Distance ASC)
    sorted_locations = sorted(
        [i for i in range(len(deliveries)) if i not in visited],
        key=lambda i: (
            deliveries[i][2], # Primary: Deadline
            euclid_distance(current_pos[0], current_pos[1], deliveries[i][0], deliveries[i][1]) # Secondary: Dist
        )
    )
    
    for i in sorted_locations:
        evaluations += 1
        if evaluations >= 500000:
            return False, path_indices, arrival_times, evaluations
            
        x, y, deadline = deliveries[i]
        travel_time = euclid_distance(current_pos[0], current_pos[1], x, y)
        arrival_time = current_time + travel_time
        
        if arrival_time <= deadline:
            visited.add(i)
            path_indices.append(i + 1)
            arrival_times.append(arrival_time)
            
            found, path_indices, arrival_times, evaluations = dfs_backtracking_ordered(
                deliveries, visited, path_indices, arrival_times, 
                evaluations, (x, y), arrival_time, depth + 1, limit_reached
            )
            
            if found:
                return True, path_indices, arrival_times, evaluations
            
            visited.remove(i)
            path_indices.pop()
            arrival_times.pop()
    
    return False, path_indices, arrival_times, evaluations

def solve_schedule(start_pos, deliveries, use_ordered=False):
    path_indices = []
    arrival_times = []
    evaluations = 0
    visited = set()
    limit_reached = [False] 
    
    if use_ordered:
        print("Running Optimized Search (Heuristic Ordered)...")
        found, path_indices, arrival_times, evaluations = dfs_backtracking_ordered(
            deliveries, visited, path_indices, arrival_times, evaluations, start_pos, 0, 0, limit_reached
        )
    else:
        print("Running Uninformed Search (Standard DFS)...")
        found, path_indices, arrival_times, evaluations = dfs_backtracking(
            deliveries, visited, path_indices, arrival_times, evaluations, start_pos, 0, 0, limit_reached
        )
    
    if found:
        print(f'Success! Path: Start → ' + ' → '.join(map(str, path_indices)))
        print(f'Total Evaluations: {evaluations}')
    else:
        print('No valid path found within constraints.')
        print(f'Evaluations: {evaluations}')

if __name__ == '__main__':
    print("=== Constraint Satisfaction Demo: Robot Scheduler ===")
    
    # Sample Data (Normally loaded from file)
    # Robot Start: (0, 0)
    # Delivery: (x, y, deadline)
    robot_start = (0.0, 0.0)
    sample_deliveries = [
        (2.0, 2.0, 5.0),   # Nearby, tight deadline
        (10.0, 10.0, 50.0), # Far away, loose deadline
        (1.0, 5.0, 12.0)    # Mid-range
    ]
    
    print(f"\nScenario: {len(sample_deliveries)} deliveries.")
    solve_schedule(robot_start, sample_deliveries, use_ordered=True)
