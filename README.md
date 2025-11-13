# AI Search Algorithms Portfolio

**Author:** Zoë Finelli  
**Course:** A.B. Cognitive Science - ARTI4500  
**Date:** 19 April 2025

---

#AI Search Algorithms Portfolio

This repository contains implementations of fundamental search algorithms used in Artificial Intelligence. These scripts demonstrate how agents navigate state spaces, solve constraint satisfaction problems, and make optimal decisions in adversarial environments.

## 1. Adversarial Search (`dominoes_minimax.py`)
An AI agent designed to play a Dominoes-style tiling game.
* **Algorithm:** Minimax with Alpha-Beta Pruning.
* **Key Concept:** The agent constructs a game tree to look ahead at future states, maximizing its own utility while minimizing the opponent's potential moves. Alpha-Beta pruning is used to eliminate irrelevant branches, significantly improving search depth.

## 2. Constraint Satisfaction (`delivery_scheduler_DFS_backtracking.py`)
A scheduling system for a robot that must visit multiple locations within strict time deadlines.
* **Algorithm:** Depth-First Search (DFS) with Backtracking.
* **Key Concept:** Compares a standard uninformed search against a heuristic-based search. The heuristic sorts tasks by "Earliest Deadline" and "Shortest Distance," demonstrating how domain knowledge can drastically reduce the number of evaluations required to find a valid schedule.

## 3. Heuristic Pathfinding (`astar_pathfinder.py`)
A navigation system for finding optimal paths in a grid with obstacles.
* **Algorithm:** A* (A-Star) Search.
* **Key Concept:** Uses a Euclidean distance heuristic to guide the search towards the goal, balancing actual travel cost ($g$) with estimated remaining cost ($h$). This implementation supports 8-directional movement on a grid.

## Usage

Each script is self-contained and includes a `__main__` block with a demonstration scenario. You can run them directly from the terminal:

```bash
# Run the Dominoes AI
python dominoes_minimax.py

# Run the Robot Scheduler
python robot_delivery_scheduler.py

# Run the A* Pathfinder
python astar_pathfinder.py
```

## Dependencies
* Python 3.10+
* Standard Library Only (No pip install required)

