"""A* search on a 2D grid.

The grid is a list of rows where ``0`` is a walkable cell, ``1`` is an
obstacle and ``"X"`` marks a cell the search has already expanded.

The module exposes the three heuristics compared in this project, the two
move sets (4- and 8-connected) and the :func:`astar` search itself.
"""

import copy
import math

# Move sets. The 8-connected set keeps the orthogonal moves first, so both
# variants expand neighbours in the same relative order.
ORTHOGONAL_MOVES = [(1, 0), (0, -1), (0, 1), (-1, 0)]
DIAGONAL_MOVES = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
ALL_MOVES = ORTHOGONAL_MOVES + DIAGONAL_MOVES

FREE = 0
OBSTACLE = 1
VISITED = "X"


def squared_distance(position, goal):
    """Squared Euclidean distance: (x1-x2)^2 + (y1-y2)^2.

    Not admissible: it overestimates the real cost, so A* loses its
    optimality guarantee and behaves more like a greedy best-first search.
    """
    return ((position[0] - goal[0]) ** 2) + ((position[1] - goal[1]) ** 2)


def euclidean_distance(position, goal):
    """Euclidean distance: sqrt((x1-x2)^2 + (y1-y2)^2)."""
    return math.sqrt(((position[0] - goal[0]) ** 2) + ((position[1] - goal[1]) ** 2))


def manhattan_distance(position, goal):
    """Manhattan distance: |x1-x2| + |y1-y2|."""
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


HEURISTICS = {
    "squared": squared_distance,
    "euclidean": euclidean_distance,
    "manhattan": manhattan_distance,
}


class Node:
    """A cell reached by the search.

    Attributes:
        parent: the node this one was expanded from, or ``None`` for the start.
        position: the ``(row, column)`` coordinates of the cell.
        grid: the state of the grid as seen from this node, with every cell
            expanded along the way marked ``"X"``.
        g: cost accumulated from the start node.
        h: heuristic estimate of the cost left to reach the goal.
        f: ``g + h``, the value the open list is sorted on.
    """

    def __init__(self, parent=None, position=None, grid=None):
        self.parent = parent
        self.position = position
        self.grid = grid

        self.g = 0
        self.h = 0
        self.f = 0

    def cost(self):
        """Cost of stepping from this node to any of its neighbours."""
        return self.g + 1

    def __eq__(self, other):
        """Two nodes are the same as soon as they sit on the same cell."""
        return self.position == other.position


def astar(grid, start, end, heuristic=squared_distance, moves=ALL_MOVES):
    """Search a path from ``start`` to ``end`` across ``grid``.

    Args:
        grid: the 2D grid to search, as described in the module docstring.
        start: the ``(row, column)`` the search starts from.
        end: the ``(row, column)`` the search has to reach.
        heuristic: one of the heuristics above, called as ``heuristic(position, goal)``.
        moves: the offsets a single step is allowed to apply.

    Returns:
        A ``(path, expanded)`` tuple, where ``path`` lists the nodes from
        start to end and ``expanded`` counts the nodes taken off the open
        list. ``path`` is ``None`` when no path exists.
    """
    start_node = Node(None, start, grid)
    end_node = Node(None, end)

    open_list = [start_node]
    closed_list = []
    expanded = 0

    # Keep going until the open list runs dry.
    while len(open_list) > 0:
        expanded = expanded + 1

        # Pick the node with the lowest f in the open list.
        current_node = open_list[0]
        current_index = 0
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        # Move it from the open list to the closed list.
        open_list.pop(current_index)
        closed_list.append(current_node)

        current_node.grid[current_node.position[0]][current_node.position[1]] = VISITED

        # The goal is reached: walk the parents back up to build the path.
        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1], expanded

        # Generate the reachable neighbours of the current node.
        children = []
        for move in moves:
            position = (
                current_node.position[0] + move[0],
                current_node.position[1] + move[1],
            )

            # Stay inside the grid.
            if (
                position[0] > (len(grid) - 1)
                or position[0] < 0
                or position[1] > (len(grid[len(grid) - 1]) - 1)
                or position[1] < 0
            ):
                continue

            # Skip obstacles and cells already walked through.
            if grid[position[0]][position[1]] != FREE:
                continue

            children.append(
                Node(current_node, position, copy.deepcopy(current_node.grid))
            )

        for child in children:
            skip = False

            # Drop the child when it is already part of the current path.
            node = current_node
            while node is not None:
                if child == node:
                    skip = True
                node = node.parent

            if skip:
                continue

            child.g = current_node.cost()
            child.h = heuristic(child.position, end_node.position)
            child.f = child.g + child.h

            # Already closed: keep whichever of the two has the lower g.
            for index, closed_node in enumerate(closed_list):
                if child == closed_node and child.g >= closed_node.g:
                    skip = True
                if child == closed_node and child.g < closed_node.g:
                    closed_list.pop(index)

            # Already open: same comparison.
            for index, open_node in enumerate(open_list):
                if child == open_node and child.g >= open_node.g:
                    skip = True
                if child == open_node and child.g < open_node.g:
                    open_list.pop(index)

            # The child does not improve on a node we already have.
            if skip:
                continue

            open_list.append(child)

    return None, expanded
