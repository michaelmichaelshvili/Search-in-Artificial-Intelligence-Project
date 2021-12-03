from Node.node import *
from collections import defaultdict


class PuzzleNode(Node):

    def __init__(self, position, operators=None, cost=1) -> None:
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

    def expand(self):
        moves = []
        i, j = self._get_coordinates(0)  # blank space

        if i > 0 and not self.operators["UP"]:
            moves.append(PuzzleNode(self._swap(i, j, i - 1, j), cost=self.cost + 1, operators={"DOWN": True}))  # move up

        if j < self.PUZZLE_NUM_COLUMNS - 1 and not self.operators["RIGHT"]:
            moves.append(PuzzleNode(self._swap(i, j, i, j + 1), cost=self.cost+1, operators={"LEFT": True}))  # move right

        if j > 0 and not self.operators["LEFT"]:
            moves.append(PuzzleNode(self._swap(i, j, i, j - 1), cost=self.cost+1, operators={"RIGHT": True}))  # move left

        if i < self.PUZZLE_NUM_ROWS - 1 and not self.operators["DOWN"]:
            moves.append(PuzzleNode(self._swap(i, j, i + 1, j), cost=self.cost+1, operators={"UP": True}))  # move down

        return moves

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
