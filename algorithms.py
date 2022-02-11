from strategy import *
from domains import *


class BreadthFirst(Strategy):
    def __init__(self, initial_puzzle):
        """
        :param initial_puzzle: Puzzle
        """
        self.start = Puzzle(initial_puzzle)

    def __str__(self):
        return 'Breadth First'

    def do_algorithm(self):
        queue = [self.start]
        expanded = []
        num_expanded_nodes = 0

        while queue:
            c_move = queue[0]
            queue.pop(0)  # dequeue (FIFO)
            if c_move.position == c_move.PUZZLE_END_POSITION:
                self.done = True
                break
            if c_move.position in expanded:
                continue

            moves = c_move.get_moves()
            num_expanded_nodes += 1
            for move in moves:
                if move.position in expanded:
                    continue
                queue.append(move)  # add new path at the end of the queue

            expanded.append(c_move.position)
            self.max_nodes = max(self.max_nodes, len(expanded) + len(queue))

        self.num_expanded_nodes = num_expanded_nodes


class AStar(Strategy):
    def __init__(self, initial_puzzle):
        """
        :param initial_puzzle: Puzzle
        """
        self.start = Puzzle(initial_puzzle)

    def __str__(self):
        return 'A*'

    @staticmethod
    def _calculate_new_heuristic(move, end_node):
        return move.heuristic_manhattan_distance() - end_node.heuristic_manhattan_distance()

    def do_algorithm(self):
        queue = [[self.start.heuristic_manhattan_distance(), self.start]]
        expanded = []
        num_expanded_nodes = 0
        path = None

        while queue:
            i = 0
            for j in range(1, len(queue)):
                if queue[i][0] > queue[j][0]:  # minimum
                    i = j

            path = queue[i]
            queue = queue[:i] + queue[i + 1:]
            end_node = path[-1]

            if end_node.position == end_node.PUZZLE_END_POSITION:
                self.done = True
                break
            if end_node.position in expanded:
                continue
            moves = end_node.get_moves()
            num_expanded_nodes += 1

            for move in moves:
                if move.position in expanded:
                    continue
                new_path = [path[0] + self._calculate_new_heuristic(move, end_node)] + path[1:] + [move]
                queue.append(new_path)
                expanded.append(end_node.position)
                self.max_nodes = max(self.max_nodes, len(expanded) + len(queue))


        self.num_expanded_nodes = num_expanded_nodes
