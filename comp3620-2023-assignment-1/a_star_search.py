"""
    Enter your details below:

    Name: Xinyun (Rita) Zhou
    Student ID: u7326123
    Email: u7326123@anu.edu.au
"""
from queue import PriorityQueue
from typing import Callable, List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem


def solve(problem: SearchProblem, heuristic: Callable) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """

    # raise_not_defined()  # Remove this line when your solution is implemented
    # *** YOUR CODE HERE ***

    # tracking
    start_node = problem.get_initial_state()
    frontier = PriorityQueue()
    frontier.put((0 + heuristic(start_node, problem), start_node, []))
    visited = {start_node: 0}

    # recursive
    while not frontier.empty():
        _, current_node, actions = frontier.get()

        # test whether the current state is the goal
        if problem.goal_test(current_node):
            return actions

        # check if the node is already visited with a lower cost
        if current_node in visited:
            if visited[current_node] < problem.get_cost_of_actions(actions):
                continue

        # record the cost on the visited node
        visited[current_node] = problem.get_cost_of_actions(actions)

        # update the detail in tracking
        for successor, action, cost in problem.get_successors(current_node):
            new_actions = actions + [action]
            new_cost = problem.get_cost_of_actions(new_actions)
            priority = new_cost + heuristic(successor, problem)
            # record a new node in visited list, or update a new list which cost less
            if successor not in visited or new_cost < visited[successor]:
                frontier.put((priority, successor, new_actions))
                visited[successor] = new_cost

    return []
