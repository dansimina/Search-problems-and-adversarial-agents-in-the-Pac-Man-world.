# 🚀 Pac-Man AI Project

This repository contains a Python implementation of various **search algorithms** and **adversarial game-playing strategies** for the **Pac-Man** game. The project explores **uninformed search, informed search, and adversarial search** techniques.

---

## 📜 Project Overview

### 🧭 Uninformed Search
The first part of the project implements classic **graph search algorithms** to navigate Pac-Man through the maze.

#### Implemented Algorithms:
- **Depth-First Search (DFS)** - Uses a stack-based approach to explore paths.
- **Breadth-First Search (BFS)** - Explores the shortest path using a queue.
- **Uniform-Cost Search (UCS)** - Finds the lowest-cost path using a priority queue.

Each algorithm helps Pac-Man **reach a fixed food location** in the maze efficiently.

---

### 🔍 Informed Search
This section enhances search efficiency by using **heuristics**.

#### Implemented Algorithms:
- **A* Search** - Uses a cost function **f(n) = g(n) + h(n)** to guide Pac-Man toward the goal efficiently.
- **Corners Problem** - Optimizes Pac-Man's path to **visit all four corners** of the maze.
- **Food Search Heuristic** - Custom heuristic to **minimize travel distance** when collecting all food dots.

These methods significantly **reduce search time** compared to uninformed algorithms.

---

### 🎮 Adversarial Search
Pac-Man is modeled as an **agent playing against ghosts**, requiring strategic decision-making.

#### Implemented AI Strategies:
- **Reflex Agent** - Uses basic evaluation functions to make decisions.
- **Minimax Algorithm** - Implements an optimal **game-playing strategy** by assuming ghosts play optimally.
- **Alpha-Beta Pruning** - Optimized Minimax to **reduce unnecessary computations**, making decision-making faster.

This allows Pac-Man to **plan multiple moves ahead**, avoiding ghosts while maximizing score.

---

## 📌 Notes
- The project uses **Python 3** and requires `pygame` for visualization.
- Implemented algorithms are tested using **provided Pac-Man mazes**.
- The **evaluation function** in the Reflex Agent is designed to balance **food collection** and **ghost avoidance**.

---

## ⚙️ Running the Project
To test different AI agents and search algorithms, run:

```sh
# Run DFS search
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs

# Run BFS search
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs

# Run A* search with Manhattan heuristic
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=aStar,heuristic=manhattanHeuristic

# Run Minimax Pac-Man agent
python pacman.py -p MinimaxAgent -l mediumClassic -a depth=3

# Run Alpha-Beta Pruning agent
python pacman.py -p AlphaBetaAgent -l mediumClassic -a depth=3
