"""Compare the three heuristics on both move sets and print the result table.

This reproduces the figures reported for this project: every cell is the
number of nodes A* took off the open list before reaching the goal.
"""

import argparse
import copy

from astar import ALL_MOVES, HEURISTICS, ORTHOGONAL_MOVES, astar
from grids import GRIDS

HEURISTIC_ORDER = ["squared", "euclidean", "manhattan"]
MOVE_SETS = [("4 directions", ORTHOGONAL_MOVES), ("8 directions", ALL_MOVES)]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--grid",
        choices=sorted(GRIDS),
        default="wall",
        help="grid instance to benchmark (default: wall)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    grid, start, end = GRIDS[args.grid]

    header = "{:<14}".format("moves") + "".join(
        "{:>22}".format(name) for name in HEURISTIC_ORDER
    )
    print("Grid '{}', from {} to {}".format(args.grid, start, end))
    print(header)
    print("-" * len(header))

    for label, moves in MOVE_SETS:
        cells = []
        for name in HEURISTIC_ORDER:
            # Each run needs a clean grid, since the search marks the one it
            # is given.
            path, expanded = astar(
                copy.deepcopy(grid),
                start,
                end,
                heuristic=HEURISTICS[name],
                moves=moves,
            )
            length = len(path) if path is not None else 0
            cells.append("{:>22}".format("{} nodes / len {}".format(expanded, length)))
        print("{:<14}".format(label) + "".join(cells))


if __name__ == "__main__":
    main()
