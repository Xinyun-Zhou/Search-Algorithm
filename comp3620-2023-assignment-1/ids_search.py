"""
    Enter your details below:

    Name: Xinyun (Rita) Zhou
    Student ID: u7326123
    Email: u7326123@anu.edu.au
"""
import sys
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

    # Remove this line when you have implemented Iterative Deepening Depth First Search
    # raise_not_defined()
    # *** YOUR CODE HERE ***

    for depth in range(sys.getrecursionlimit()):
        # tracking
        visited = set()
        frontier = [(problem.get_initial_state(), 0, [])]

        # recursive
        while frontier:
            state, current_depth, actions = frontier.pop()

            # check the goal
            if problem.goal_test(state):
                return actions

            # else recursive
            if current_depth < depth:
                for successor, action, cost in problem.get_successors(state):
                    if successor not in visited:
                        visited.add(successor)
                        new_actions = actions + [action]
                        frontier.append((successor, current_depth + 1, new_actions))
