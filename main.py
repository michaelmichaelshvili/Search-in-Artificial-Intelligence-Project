from algorithms import *
from domains import *
from puzzleSolver import *
from Algorithms.best_first_frontier_search import *
from Algorithms.a_start_frontier_search import *
from Node.node import *
from Node.puzzle_node import *
from math import sqrt
from random import shuffle
import numpy as np
from threading import Timer

N = 4


def getInvCount(arr):
    arr1 = []
    for y in arr:
        for x in y:
            arr1.append(x)
    arr = arr1
    inv_count = 0
    for i in range(N * N - 1):
        for j in range(i + 1, N * N):
            # count pairs(arr[i], arr[j]) such that
            # i < j and arr[i] > arr[j]
            if (arr[j] and arr[i] and arr[i] > arr[j]):
                inv_count += 1

    return inv_count


# find Position of blank from bottom
def findXPosition(puzzle):
    # start from bottom-right corner of matrix
    for i in range(N - 1, -1, -1):
        for j in range(N - 1, -1, -1):
            if (puzzle[i][j] == 0):
                return N - i


# This function returns true if given
# instance of N*N - 1 puzzle is solvable
def isSolvable(puzzle):
    # Count inversions in given puzzle
    invCount = getInvCount(puzzle)

    # If grid is odd, return true if inversion
    # count is even.
    if (N % 2 == 1):
        return invCount%2==0

    else:  # grid is even
        pos = findXPosition(puzzle)
        if (pos%2==1):
            return invCount%2==0
        else:
            return invCount%2==1

def spuzzle(size):
  """Returns a new valid random puzzle."""
  puzzle = [i for i in range(size ** 2)]
  # puzzle = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,15,14,0]]
  # shuffle the puzzle until it's solvable
  shuffle(puzzle)
  while not isSolvable(np.reshape(puzzle, (4,4)).tolist()):
    shuffle(puzzle)
  return puzzle

if __name__ == '__main__':
        # print(isSolvable([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,15,14,0]]))
        # Best First Frontier Search
        initial_state = [[1,2,5,9]
                        ,[14,15,10,0],
                         [12,8,4,13]
                        ,[11,7,3,6]]
        # initial_state = [[1, 2, 3, 4],
        #                  [5, 6, 7, 8],
        #                  [0, 10, 11, 12],
        #                  [9, 13, 14, 15]]
        # initial_state = np.reshape(spuzzle(4), (4,4)).tolist()

        # p.print_solution()

        # Frontier-A* Search
        # initial = PuzzleNode([[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]])
        #
        # p = PuzzleSolver(BestFirstFrontierSearch(initial))
        # print(p)
        # p.run()
        # p.print_performance()
        # p.print_solution()
        #
        puzzle = Puzzle(initial_state)

        for strategy in [AStar]:
            p = PuzzleSolver(strategy(puzzle))
            p.run()
            p.print_performance()
            p.print_solution()

        initial = PuzzleNode(initial_state)

        # p = PuzzleSolver(BestFirstFrontierSearch(initial))
        # p.run()
        # p.print_performance()

        p = PuzzleSolver(AStarFrontierSearch(initial))
        p.run()
        p.print_performance()
        # initial = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]])
        # goal = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
        # # initial = PuzzleNode([[1, 0], [3, 2]])
        # # goal = PuzzleNode([[1, 2], [3, 0]])
        # frontier = FrontierSearch(initial, goal)
        # print(frontier.do_algorithm())
