# heuristics.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This class contains heuristics which are used for the search procedures that
    you write in search_strategies.py.

    The first part of the file contains heuristics to be used with the algorithms
    that you will write in search_strategies.py.

    In the second part you will write a heuristic for Q4 to be used with a
    MultiplePositionSearchProblem.
"""
from typing import Tuple

from search_problems import (MultiplePositionSearchProblem,
                             PositionSearchProblem)

Position = Tuple[int, int]
YellowBirds = Tuple[Position]
State = Tuple[Position, YellowBirds]

# -------------------------------------------------------------------------------
# A set of heuristics which are used with a PositionSearchProblem
# You do not need to modify any of these.
# -------------------------------------------------------------------------------


def null_heuristic(pos: Position, problem: PositionSearchProblem) -> int:
    """The null heuristic. It is fast but uninformative. It always returns 0"""

    return 0


def manhattan_heuristic(pos: Position, problem: PositionSearchProblem) -> int:
    """The Manhattan distance heuristic for a PositionSearchProblem."""

    return abs(pos[0] - problem.goal_pos[0]) + abs(pos[1] - problem.goal_pos[1])


def euclidean_heuristic(pos: Position, problem: PositionSearchProblem) -> float:
    """The Euclidean distance heuristic for a PositionSearchProblem"""

    return ((pos[0] - problem.goal_pos[0]) ** 2 + (pos[1] - problem.goal_pos[1]) ** 2) ** 0.5


# Abbreviations
null = null_heuristic
manhattan = manhattan_heuristic
euclidean = euclidean_heuristic

# -------------------------------------------------------------------------------
# You have to implement the following heuristics for Q4 of the assignment.
# It is used with a MultiplePositionSearchProblem
# -------------------------------------------------------------------------------

# You can make helper functions here, if you need them


def bird_counting_heuristic(state: State,
                            problem: MultiplePositionSearchProblem) -> float:
    position, yellow_birds = state
    heuristic_value = 0

    """ *** YOUR CODE HERE *** """
    # h(s) = number_of_yellow_birds_still_to_be_captured
    for bird in yellow_birds:
        heuristic_value += 1
    return heuristic_value


bch = bird_counting_heuristic


def every_bird_heuristic(state: State,
                         problem: MultiplePositionSearchProblem) -> float:
    position, yellow_birds = state
    heuristic_value = 0

    """ *** YOUR CODE HERE *** """

    # 1. Calculate distances between all pairs of birds
    all_position = [position] + list(yellow_birds)
    distances = {}
    for i in range(len(all_position)):
        for j in range(len(all_position)):
            node_1, node_2 = all_position[i], all_position[j]
            if node_1 != node_2:
                distances[(node_1, node_2)] = problem.maze_distance(node_1, node_2)

    # 2. Sort distances in increasing order
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])

    # 3. Construct minimum spanning tree
    connected = {position}
    subtrees = [[position]]

    for edge, distance in sorted_distances:
        node_1, node_2 = edge

        # check the connection
        if node_1 in connected and node_2 in connected:
            for subtree in subtrees:
                if node_1 in subtree:
                    subtree_1 = subtree
                if node_2 in subtree:
                    subtree_2 = subtree
            # if not connected, then merge the subtrees
            if subtree_1 != subtree_2:
                subtrees.remove(subtree_2)
                subtree_1 += subtree_2

        # if one node is connected
        elif node_1 in connected:
            for subtree in subtrees:
                if node_1 in subtree:
                    subtree.append(node_2)
        elif node_2 in connected:
            for subtree in subtrees:
                if node_2 in subtree:
                    subtree.append(node_1)

        # if both nodes are not connected
        else:
            subtrees.append([node_1, node_2])

        connected.update([node_1, node_2])

        # stop the loop as all nodes are connected
        if len(connected) == len(all_position):
            break

    # 4. Return the sum of edge costs in the minimum spanning tree
    for subtree in subtrees:
        for i in range(len(subtree)):
            for j in range(i+1, len(subtree)):
                node_1, node_2 = subtree[i], subtree[j]
                if (node_1, node_2) in distances:
                    heuristic_value += distances[(node_1, node_2)]

    return heuristic_value


every_bird = every_bird_heuristic
