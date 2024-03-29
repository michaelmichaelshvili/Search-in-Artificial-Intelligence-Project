from algorithms import *
from domains import *
from puzzleSolver import *
from Algorithms.best_first_frontier_search import *
from Algorithms.a_star_frontier_search import *
from Node.node import *
from random import shuffle
import numpy as np
from Algorithms.RBFS import RBFS

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
        initial_state = [[5, 3, 6], [2, 4, 8], [7, 0, 1]]


        for strategy in [BreadthFirst, BestFirstFrontierSearch, RBFS]:
            p = PuzzleSolver(strategy(initial_state))
            p.run()
            p.get_performance()
