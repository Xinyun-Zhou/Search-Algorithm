"""
    Enter your details below:

    Name: Xinyun (Rita) Zhou
    Student ID: u7326123
    Email: u7326123@anu.edu.au
"""
import queue
from collections import deque
from typing import List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem


def solve(problem: SearchProblem) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """

    # raise_not_defined()  # Remove this line when you have implemented BrFS
    # *** YOUR CODE HERE ***

    # tracking
    frontier = deque([(problem.get_initial_state(), [])])
    visited = set()

    # recursive
    while frontier:
        node, actions = frontier.popleft()

        # make sure no circle path occurs
        if node not in visited:
            visited.add(node)

            # test whether the current node is the goal
            if problem.goal_test(node):
                return actions

            # update the detail of the path
            for successor, action, _ in problem.get_successors(node):
                new_action = actions + [action]
                frontier.append((successor, new_action))
