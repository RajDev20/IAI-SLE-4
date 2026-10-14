"""
SLE-4 - ADR Evidence Code (02AML204 - Introduction to Artificial Intelligence)
PRN: 25UAM112 | Name: Rajdeep Mahadev Kamble | Division: B

System : 8-Puzzle Solver (same system as SLE-2 profiling and SLE-3 C4 model)
Decision recorded in the ADR:
    Use Breadth-First Search (FIFO frontier + explored set) as the solving
    strategy instead of Depth-First Search.

Structure follows the SLE-3 C4 Container / Code levels:
    Input Module     -> make_start_state(), START_STATE, GOAL_STATE
    Puzzle Model     -> PuzzleProblem, get_successors(), is_goal()
    Search Engine    -> bfs(), dfs(), reconstruct_path()   (Frontier + Explored Set)
    Profiler Module  -> profile_run(), cprofile_calls()
    Output Module    -> print_results_table(), scaling_experiment()

Run:  python sle4_8puzzle_adr.py
Optional flame graph (same tool as SLE-2):  py-spy record -o flame.svg -- python sle4_8puzzle_adr.py
"""

import cProfile
import pstats
import random
import time
from collections import deque

# ----------------------------------------------------------------------------
# INPUT MODULE  (SLE-3: Input Module)
# State = tuple of 9 ints read row by row, 0 = blank tile.
# START_STATE / GOAL_STATE are exactly the states used in SLE-2.
# ----------------------------------------------------------------------------
GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

START_STATE = (2, 0, 4,
               5, 6, 3,
               1, 7, 8)

# Move order used in SLE-2 (blank moves Up, Left, Right, Down). Keeping the
# same order is what makes the numbers below identical to the SLE-2 table.
MOVE_ORDER = ("U", "L", "R", "D")
MOVE_DELTA = {"U": -3, "D": 3, "L": -1, "R": 1}


def make_start_state(goal=GOAL_STATE, moves=25, seed=None):
    """Random walk from the goal -> always a solvable start state."""
    rng = random.Random(seed)
    state, prev = goal, None
    for _ in range(moves):
        options = [s for _, s in get_successors(state) if s != prev]
        prev, state = state, rng.choice(options)
    return state


# ----------------------------------------------------------------------------
# PUZZLE MODEL  (SLE-3: Puzzle Model) - shared by BFS and DFS
# ----------------------------------------------------------------------------
class Node:
    """Stores a puzzle state, its parent node and the move that led to it."""
    __slots__ = ("state", "parent", "move")

    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move


class PuzzleProblem:
    """Holds the start and goal state of the puzzle."""

    def __init__(self, start=START_STATE, goal=GOAL_STATE):
        self.start = start
        self.goal = goal


def get_successors(state):
    """Return [(move, new_state), ...] for every legal blank-tile move."""
    blank = state.index(0)
    row, col = divmod(blank, 3)
    result = []
    for m in MOVE_ORDER:
        if m == "U" and row == 0:
            continue
        if m == "D" and row == 2:
            continue
        if m == "L" and col == 0:
            continue
        if m == "R" and col == 2:
            continue
        target = blank + MOVE_DELTA[m]
        new = list(state)
        new[blank], new[target] = new[target], new[blank]
        result.append((m, tuple(new)))
    return result


def is_goal(state, goal):
    """True when the state equals the goal arrangement."""
    return state == goal


# ----------------------------------------------------------------------------
# SEARCH ENGINE  (SLE-3: Frontier, Node Expander, Explored Set, Goal Test,
#                 Path Reconstructor, Node Counter)
# BFS and DFS are IDENTICAL except for how the frontier is popped:
#     BFS -> popleft()  (FIFO queue)      DFS -> pop()  (LIFO stack)
# ----------------------------------------------------------------------------
def reconstruct_path(node):
    """Walk parent links from the goal node back to the start."""
    moves = []
    while node.parent is not None:
        moves.append(node.move)
        node = node.parent
    moves.reverse()
    return moves


def _search(problem, use_queue):
    frontier = deque([Node(problem.start)])
    explored = {problem.start}      # Explored Set: states already generated
    nodes_expanded = 0              # Node Counter: incremented on every pop
    peak_frontier = 1
    while frontier:
        node = frontier.popleft() if use_queue else frontier.pop()
        nodes_expanded += 1
        if is_goal(node.state, problem.goal):
            return reconstruct_path(node), nodes_expanded, peak_frontier, len(explored)
        for move, child in get_successors(node.state):
            if child not in explored:
                explored.add(child)
                frontier.append(Node(child, node, move))
        peak_frontier = max(peak_frontier, len(frontier))
    return None, nodes_expanded, peak_frontier, len(explored)


def bfs(problem):
    """FIFO frontier. Returns (shortest path, nodes expanded, peak frontier, explored size)."""
    return _search(problem, use_queue=True)


def dfs(problem):
    """LIFO frontier + explored set. Returns (a path, nodes expanded, peak frontier, explored size)."""
    return _search(problem, use_queue=False)


# ----------------------------------------------------------------------------
# PROFILER MODULE  (SLE-3: Profiler Module) - outside the search code
# ----------------------------------------------------------------------------
def profile_run(algo, problem, runs=5):
    """Time `algo` `runs` times with perf_counter; return averaged metrics."""
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        path, nodes, peak, explored = algo(problem)
        times.append((time.perf_counter() - t0) * 1000.0)
    return {
        "avg_ms": sum(times) / len(times),
        "nodes": nodes,
        "moves": len(path),
        "peak_frontier": peak,
        "explored": explored,
    }


def cprofile_calls(algo, problem):
    """Total function calls reported by cProfile for one run."""
    pr = cProfile.Profile()
    pr.enable()
    algo(problem)
    pr.disable()
    return pstats.Stats(pr).total_calls


# ----------------------------------------------------------------------------
# OUTPUT MODULE  (SLE-3: Output Module)
# ----------------------------------------------------------------------------
def print_results_table(problem):
    bfs_r = profile_run(bfs, problem)
    dfs_r = profile_run(dfs, problem)
    bfs_r["calls"] = cprofile_calls(bfs, problem)
    dfs_r["calls"] = cprofile_calls(dfs, problem)

    print("=" * 66)
    print("8-PUZZLE: BFS vs DFS (same start/goal as SLE-2, 5 timed runs)")
    print("=" * 66)
    print(f"{'Metric':<30}{'BFS':>16}{'DFS':>16}")
    print("-" * 66)
    print(f"{'Avg. time (ms)':<30}{bfs_r['avg_ms']:>16.2f}{dfs_r['avg_ms']:>16.2f}")
    print(f"{'Nodes expanded':<30}{bfs_r['nodes']:>16,}{dfs_r['nodes']:>16,}")
    print(f"{'Solution length (moves)':<30}{bfs_r['moves']:>16,}{dfs_r['moves']:>16,}")
    print(f"{'Function calls (cProfile)':<30}{bfs_r['calls']:>16,}{dfs_r['calls']:>16,}")
    print(f"{'Peak frontier size':<30}{bfs_r['peak_frontier']:>16,}{dfs_r['peak_frontier']:>16,}")
    print(f"{'States stored (explored set)':<30}{bfs_r['explored']:>16,}{dfs_r['explored']:>16,}")
    print("-" * 66)
    print(f"Node ratio  DFS/BFS : {dfs_r['nodes'] / bfs_r['nodes']:.1f}x")
    print(f"Time ratio  DFS/BFS : {dfs_r['avg_ms'] / bfs_r['avg_ms']:.1f}x")
    path, *_ = bfs(problem)
    print("BFS optimal path    :", " ".join(path))
    return bfs_r, dfs_r


def states_at_depths(goal, depths):
    """One start state for each exact solution depth (BFS layers from the goal)."""
    seen, layer, found, d = {goal}, [goal], {}, 0
    while layer and len(found) < len(depths):
        if d in depths:
            found[d] = layer[len(layer) // 2]
        nxt = []
        for st in layer:
            for _, ch in get_successors(st):
                if ch not in seen:
                    seen.add(ch)
                    nxt.append(ch)
        layer, d = nxt, d + 1
    return found


def scaling_experiment(depths=(8, 12, 16, 20, 24, 28)):
    """
    Viva question: 'What happens if the problem size becomes larger?'
    Solve start states at increasing solution depth d with BFS and show how
    nodes expanded and the BFS frontier (memory) grow.
    """
    print()
    print("=" * 66)
    print("SCALING: BFS on deeper 8-puzzle instances (exact solution depth)")
    print("=" * 66)
    print(f"{'Depth d':>8}{'Moves':>8}{'Nodes exp.':>14}{'Peak frontier':>16}{'Time (ms)':>12}")
    print("-" * 66)
    starts = states_at_depths(GOAL_STATE, set(depths))
    for d in depths:
        t0 = time.perf_counter()
        path, nodes, peak, _ = bfs(PuzzleProblem(starts[d], GOAL_STATE))
        ms = (time.perf_counter() - t0) * 1000.0
        print(f"{d:>8}{len(path):>8}{nodes:>14,}{peak:>16,}{ms:>12.2f}")
    print("-" * 66)
    print("Total reachable states of the 8-puzzle = 181,440 (9!/2)")


if __name__ == "__main__":
    problem = PuzzleProblem(START_STATE, GOAL_STATE)
    print_results_table(problem)
    scaling_experiment()
