# minimax_agent.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

"""
    Enter your details below:

    Name: Xinyun (Rita) Zhou
    Student ID: u7326123
    Email: u7326123@anu.edu.au
"""
from typing import Tuple

from agents import Agent
from game_engine.actions import Directions
from search_problems import AdversarialSearchProblem

Position = Tuple[int, int]
Positions = Tuple[Position]
State = Tuple[int, Position, Position, Positions, float, float]


class MinimaxAgent(Agent):
    """ The agent you will implement to compete with the black bird to try and
        save as many yellow birds as possible. """

    def __init__(self, max_player, depth="2"):
        """ Make a new Adversarial agent with the optional depth argument.
        """
        self.max_player = max_player
        self.depth = int(depth)

    def evaluation(self, problem: AdversarialSearchProblem, state: State) -> float:
        """
            (MinimaxAgent, AdversarialSearchProblem,
                (int, (int, int), (int, int), ((int, int)), number, number))
                    -> number
        """
        player, red_pos, black_pos, yellow_birds, score, yb_score = state

        # *** YOUR CODE GOES HERE ***

        def euclidean_heuristic(pos: Position, goal: Position) -> float:
            """
            The calculator of euclidean_heuristic
            """
            return ((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2) ** 0.5

        # calculate the distance from player to every bird and the distance from opponent to every bird
        # then tracking in the list
        bird_weights = []
        for position in yellow_birds:
            player_distance = euclidean_heuristic(red_pos, position)
            opponent_distance = euclidean_heuristic(black_pos, position)
            # if the opponent is closer, then player will give up
            if opponent_distance > player_distance:
                weights = 1

            # otherwise, calculate the path cost
            else:
                weights = yb_score-player_distance

            # add to list
            bird_weights.append(weights)

        # create a formula to calculate weight
        total_weight = sum(bird_weights)
        weight_score = score
        for weight in bird_weights:
            weight_score += weight / total_weight * 10

        return weight_score

    def maximize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> Tuple[float, str]:
        """ This method should return a pair (max_utility, max_action).
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """

        # raise_not_defined()  # Remove this line once you finished your implementation
        # *** YOUR CODE GOES HERE ***

        # find the leaves
        if problem.terminal_test(state) or current_depth == self.depth:
            return self.evaluation(problem, state), Directions.STOP

        # tracking
        max_utility = float('-inf')
        max_action = Directions.STOP

        # recursion
        for successor, action, cost in problem.get_successors(state):
            # successor contains (player_id, player_location, opponent_location, (yellow_birds), score, yb_value)
            # calculate new utility and update the alpha or beta
            utility = self.minimize(problem, successor, current_depth+1, alpha, beta)
            if utility > max_utility:
                max_utility = utility
                max_action = action
            if utility >= beta:
                return max_utility, max_action
            alpha = max(alpha, max_utility)

        return max_utility, max_action

    def minimize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> float:
        """ This function should just return the minimum utility.
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """

        # raise_not_defined()  # Remove this line once you finished your implementation
        # *** YOUR CODE GOES HERE ***

        # find the leaves
        if problem.terminal_test(state) or current_depth == self.depth:
            return self.evaluation(problem, state)

        # tracking
        min_utility = float('inf')

        # recursive
        for successor, action, cost in problem.get_successors(state):
            # calculate new utility and update alpha or beta
            utility, _ = self.maximize(problem, successor, current_depth, alpha, beta)
            if utility < min_utility:
                min_utility = utility
            if min_utility <= alpha:
                return min_utility
            beta = min(beta, min_utility)

        return min_utility

    def get_action(self, game_state):
        """ This method is called by the system to solicit an action from
            MinimaxAgent. It is passed in a State object.

            Like with all of the other search problems, we have abstracted
            away the details of the game state by producing a SearchProblem.
            You will use the states of this AdversarialSearchProblem to
            implement your minimax procedure. The details you need to know
            are explained at the top of this file.
        """
        # We tell the search problem what the current state is and which player
        # is the maximizing player (i.e. who's turn it is now).
        problem = AdversarialSearchProblem(game_state, self.max_player)
        state = problem.get_initial_state()
        utility, max_action = self.maximize(problem, state, 0)
        print("At Root: Utility:", utility, "Action:",
              max_action, "Expanded:", problem._expanded)
        return max_action
