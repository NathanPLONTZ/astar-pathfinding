"""Run A* on one grid and print the path it found, step by step."""

import argparse
import copy

from astar import ALL_MOVES, HEURISTICS, ORTHOGONAL_MOVES, astar
from grids import GRIDS, format_grid


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--grid",
        choices=sorted(GRIDS),
        default="maze",
        help="grid instance to search (default: maze)",
    )
    parser.add_argument(
        "--heuristic",
        choices=sorted(HEURISTICS),
        default="squared",
        help="heuristic used to estimate the remaining cost (default: squared)",
    )
    parser.add_argument(
        "--moves",
        type=int,
        choices=(4, 8),
        default=8,
        help="4 for orthogonal moves only, 8 to allow diagonals (default: 8)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="print only the number of expanded nodes and the path length",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    grid, start, end = GRIDS[args.grid]
    moves = ALL_MOVES if args.moves == 8 else ORTHOGONAL_MOVES

    # The search marks the grid it is given, so hand it a copy and leave the
    # instance in grids.py untouched.
    path, expanded = astar(
        copy.deepcopy(grid),
        start,
        end,
        heuristic=HEURISTICS[args.heuristic],
        moves=moves,
    )

    print("Nodes expanded: {}".format(expanded))

    if path is None:
        print("No path found between {} and {}.".format(start, end))
        return

    print("Path length: {}".format(len(path)))

    if args.quiet:
        return

    for step, node in enumerate(path):
        print("Node {} (f: {})".format(step, node.f))
        print(format_grid(node.grid))
        print("--------------------")


if __name__ == "__main__":
    main()
