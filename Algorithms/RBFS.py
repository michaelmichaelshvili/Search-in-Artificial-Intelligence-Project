from strategy import *
from sys import maxsize
from Node.node import Node
import numpy as np
from puzzleSolver import *


class Puzzle:
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    heuristic = None
    f_value = None
    needs_hueristic = False
    num_of_instances = 0

    # for generating parent, action, path_cost initially
    def __init__(self, state, parent, action, path_cost, needs_hueristic=False):
        self.parent = parent
        self.state = state
        self.action = action
        self.board_size = int(np.sqrt(len(state)))
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost
        # if heuristic is needed then inly will calculate and update value
        if needs_hueristic:
            self.needs_hueristic = True
            self.find_heuristic_value()
            self.f_value = self.heuristic + self.path_cost
        Puzzle.num_of_instances += 1

    def find_actions(self, i, j):  # when we find blank i.e zero and take actions UP,DOWN,LEFT, RIGHT
        actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        # for avoiding out of bound case, remove from actions
        if i == 0:
            actions.remove('UP')
        elif i == 2:
            actions.remove('DOWN')
        if j == 0:
            actions.remove('LEFT')
        elif j == 2:
            actions.remove('RIGHT')
        return actions

    def __str__(self):
        return str(self.state[0:3]) + '\n' + str(self.state[3:6]) + '\n' + str(self.state[6:9])

    def find_heuristic_value(self):  # for calculating huristic value using man-hattan diatance
        self.heuristic = 0
        for num in range(1, self.board_size ** 2):
            distance = abs(self.state.index(num) - self.goal.index(num))
            i = int(distance / self.board_size)
            j = int(distance % self.board_size)
            self.heuristic = self.heuristic + i + j

    def goal_test(self):
        if self.state == self.goal:  # for verifying with goal
            return True
        return False

    def generate_child(self):
        children = []
        x = self.state.index(0)  # getting index and converting into 2D array of 3x3
        i = int(x / self.board_size)
        j = int(x % self.board_size)
        actions = self.find_actions(i, j)  # getting all actions

        for action in actions:
            new_state = self.state.copy()  # copy,for avoiding call by reference in array pointer
            if action == 'UP':
                new_state[x], new_state[x - self.board_size] = new_state[x - self.board_size], new_state[x]
            elif action == 'DOWN':
                new_state[x], new_state[x + self.board_size] = new_state[x + self.board_size], new_state[x]
            elif action == 'LEFT':
                new_state[x], new_state[x - 1] = new_state[x - 1], new_state[x]
            elif action == 'RIGHT':
                new_state[x], new_state[x + 1] = new_state[x + 1], new_state[x]
            children.append(Puzzle(new_state, self, action, 1, self.needs_hueristic))
        return children

    def solution(self):  # for finding solution steps as UP, DOWN, LEFT, RIGHT
        solution = []
        solution.append(self.action)
        path = self
        while path.parent is not None:
            path = path.parent
            solution.append(path.state)
        solution = solution[:-1]
        solution.reverse()
        return solution


class RBFS(Strategy):

    def __init__(self, initial) -> None:
        super().__init__()
        self.initial = np.reshape(initial, (-1)).tolist()
        self.max_nodes = 1

    # code for Recursive Best First Search as RBFS
    def do_algorithm(self):
        node = self.find_solution(
            Puzzle(state=self.initial, parent=None, action=None, path_cost=0, needs_hueristic=True),
            f_limit=maxsize)
        return "SUCCESS" if node[0] else "No solution found"

    def find_solution(self, node, f_limit, len_prev_successors=0):

        result = None

        successors = []
        if node.goal_test():
            return node, None

        children = node.generate_child()  # generating all the valid children node from parent node
        self.num_expanded_nodes += 1
        if not len(children):
            return None, maxsize

        count = -1
        for child in children:
            count += 1
            successors.append((child.f_value, count, child))

        self.max_nodes = max(self.max_nodes, len(successors) + len_prev_successors)

        while len(successors):
            successors.sort()
            best = successors[0][2]  # for finding best node with f_value
            if best.f_value > f_limit:
                return None, best.f_value  # in case of failure
            alternative = successors[1][0]  # for finding 2nd minimum best node with f_value

            result, best.f_value = self.find_solution(best, min(f_limit, alternative),
                                                      len(successors) + len_prev_successors)

            successors[0] = (best.f_value, successors[0][1], best)
            if result is not None:
                break

        return result, None

    def __str__(self):
        return 'RBFS'

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    initial = [[1, 2, 3], [5, 6, 7], [8, 0, 4]]
    rbfs = PuzzleSolver(RBFS(initial))
    steps = rbfs.run()
    rbfs.print_performance()

    print("\nNote:- \nLEFT action :=> for going to new state by replacing zero with LEFT number of zero.")
    print("\nRIGHT action :=> for going to new state by replacing zero with RIGHT number of zero.")
    print("\nUP action :=> for going to new state by replacing zero with UP number of zero.")
    print("\nDOWN action :=> for going to new state by replacing zero with DOWN number of zero.\n\n ")

    print("strated execution............ \n\nstarting state is: \n", [[1, 2, 3], [5, 6, 0], [7, 8, 4]])
    print("\nActions, that are taken, are following.......\n\n", steps)
