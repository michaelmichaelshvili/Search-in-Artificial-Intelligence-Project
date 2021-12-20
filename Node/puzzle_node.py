from Node.node import *


class PuzzleNode(Node):

    def __init__(self, position, operators=None, cost=None) -> None:
        if cost is None:
            cost = 1
        if operators is None:
            operators = {k: False for k in ("UP", "RIGHT", "DOWN", "LEFT")}
        else:
            operators = {k: False if k not in operators else True for k in ("UP", "RIGHT", "DOWN", "LEFT")}
        super().__init__(position, operators, cost)
        self.PUZZLE_NUM_ROWS = len(position)
        self.PUZZLE_NUM_COLUMNS = len(position[0])
        self.PUZZLE_END_POSITION = self._generate_end_position()

    def __str__(self) -> str:
        puzzle_string = '—' * 13 + '\n'
        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                puzzle_string += '│{0: >2}'.format(str(self.state[i][j]))
                if j == self.PUZZLE_NUM_COLUMNS - 1:
                    puzzle_string += '│\n'

        puzzle_string += '—' * 13 + '\n'
        return puzzle_string

    def __eq__(self, o) -> bool:
        return self.state == o.state if type(o) is PuzzleNode else False

    def expand(self, cost_function):
        moves = []
        i, j = self._get_coordinates(0)  # blank space

        if i > 0 and not self.operators["UP"]:
            next_node = PuzzleNode(self._swap(i, j, i - 1, j), operators={"DOWN": True})
            next_node_cost = cost_function(self, next_node)
            next_node.cost = next_node_cost
            moves.append(next_node)  # move up

        if j < self.PUZZLE_NUM_COLUMNS - 1 and not self.operators["RIGHT"]:
            next_node = PuzzleNode(self._swap(i, j, i, j + 1), operators={"LEFT": True})
            next_node_cost = cost_function(self, next_node)
            next_node.cost = next_node_cost
            moves.append(next_node)  # move right

        if j > 0 and not self.operators["LEFT"]:
            next_node = PuzzleNode(self._swap(i, j, i, j - 1), operators={"RIGHT": True})
            next_node_cost = cost_function(self, next_node)
            next_node.cost = next_node_cost
            moves.append(next_node)  # move left

        if i < self.PUZZLE_NUM_ROWS - 1 and not self.operators["DOWN"]:
            next_node = PuzzleNode(self._swap(i, j, i + 1, j), operators={"UP": True})
            next_node_cost = cost_function(self, next_node)
            next_node.cost = next_node_cost
            moves.append(next_node)  # move down
        return moves

    def union(self, o):
        if self.state != o.state:
            raise ValueError("The nodes are not in same state")
        return PuzzleNode(self.state,
                          {k1: v1 or v2 for ((k1, v1), (k2, v2)) in zip(self.operators.items(), o.operators.items())},
                          min(self.cost, o.cost))

    def _swap(self, x1, y1, x2, y2):
        """
        Swap the positions between two elements
        """
        puzzle_copy = [list(row) for row in self.state]  # copy the puzzle
        puzzle_copy[x1][y1], puzzle_copy[x2][y2] = puzzle_copy[x2][y2], puzzle_copy[x1][y1]

        return puzzle_copy

    def _get_coordinates(self, tile, position=None):
        """
        Returns the i, j coordinates for a given tile
        """
        if not position:
            position = self.state

        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                if position[i][j] == tile:
                    return i, j

        return RuntimeError('Invalid tile value')

    def _generate_end_position(self):
        """
        Example end position in 4x4 puzzle
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
        """
        end_position = []
        new_row = []

        for i in range(1, self.PUZZLE_NUM_ROWS * self.PUZZLE_NUM_COLUMNS + 1):
            new_row.append(i)
            if len(new_row) == self.PUZZLE_NUM_COLUMNS:
                end_position.append(new_row)
                new_row = []

        end_position[-1][-1] = 0
        return end_position

    def heuristic_misplaced(self):
        """
        Counts the number of misplaced tiles
        """
        misplaced = 0

        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                if self.state[i][j] != self.PUZZLE_END_POSITION[i][j]:
                    misplaced += 1

        return misplaced

    def heuristic_manhattan_distance(self):
        """
        Counts how much is a tile misplaced from the original position
        """
        distance = 0

        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                i1, j1 = self._get_coordinates(self.state[i][j], self.PUZZLE_END_POSITION)
                distance += abs(i - i1) + abs(j - j1)

        return distance
