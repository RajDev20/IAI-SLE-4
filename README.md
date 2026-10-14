# IAI-SLE-4

# 8-Puzzle Solver – BFS vs DFS

## Project Information
- **Course:** 02AML204 – Introduction to Artificial Intelligence
- **Project:** 8-Puzzle Solver
- **SLE:** SLE-4 – Architecture Decision Record (ADR)
- **Name:** Rajdeep Mahadev Kamble
- **PRN:** 25UAM112
- **Division:** B

## Introduction
The 8-Puzzle is a 3×3 sliding-tile puzzle in which the blank tile can move up, down, left, or right. The goal is to arrange the tiles in the required order.

This project compares Breadth-First Search (BFS) and Depth-First Search (DFS) to determine which algorithm performs better.

## Objectives
- Implement BFS and DFS for the 8-Puzzle.
- Compare execution time, expanded nodes, and solution length.
- Profile the algorithms using Python tools.
- Select a suitable search algorithm based on experimental results.

## Algorithms Used

### 1. Breadth-First Search (BFS)
BFS explores states level by level using a FIFO queue. It finds the shortest solution path when all moves have equal cost.

### 2. Depth-First Search (DFS)
DFS explores one branch deeply before backtracking. It uses a LIFO stack and does not guarantee the shortest path.

## Performance Comparison

| Metric | BFS | DFS |
|---|---:|---:|
| Average execution time | 2.92 ms | 57.71 ms |
| Nodes expanded | 2,498 | 36,813 |
| Solution length | 13 moves | 32,669 moves |
| Function calls | 22,337 | 380,743 |

*Results are from the SLE-2 experiment on the same puzzle.*

## Architecture Decision
BFS was selected as the main solving algorithm because it found the optimal 13-move solution and performed better in the measured experiment. DFS was retained as a comparison algorithm.

## Tools Used
- Python
- `time.perf_counter()`
- `cProfile`
- GitHub
- py-spy and flame graph concepts

**Note:** The SLE-4 report states that py-spy could not be installed in the original environment because internet access was unavailable.

## How to Run
1. Install Python 3.
2. Download or clone the project repository.
3. Open the project folder in VS Code.
4. Open the terminal and run:

   `python sle4_8puzzle_adr.py`

On Windows, you can also use:

   `py sle4_8puzzle_adr.py`

## Future Improvements
- Implement A* search using Manhattan distance.
- Compare memory usage for BFS and DFS.
- Test different starting puzzle states.
- Improve performance for larger puzzles.

## AI Contribution
AI helped draft the ADR, prepare the solver code, and organize the scaling experiment.

## My Contribution
I selected BFS based on my previous SLE-2 and SLE-3 work, checked the results against my earlier report, verified the code names, ran the script, and prepared for the viva.

## Author
**Rajdeep Mahadev Kamble**

GitHub: https://github.com/RajDev20
