"""The grid instances the project is run against.

Both are 10x10. ``WALL`` is the instance the heuristics were benchmarked on;
``MAZE`` is a harder instance used for the demo.
"""

# A single vertical wall with one opening on row 7. The start and the goal sit
# on the same row, so the search has to walk all the way around the wall.
WALL = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
]
WALL_START = (0, 1)
WALL_END = (0, 9)

# The same wall plus a dead end in the lower left corner, crossed from one
# corner to the other.
MAZE = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
]
MAZE_START = (0, 0)
MAZE_END = (9, 9)

GRIDS = {
    "wall": (WALL, WALL_START, WALL_END),
    "maze": (MAZE, MAZE_START, MAZE_END),
}


def format_grid(grid):
    """Render a grid the way the search prints it, one row per line."""
    return "\n".join(str(row).replace("'", "") for row in grid)
