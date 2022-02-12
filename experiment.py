import csv
import os
from multiprocessing import Process, Queue, Array
import time
from random import shuffle
import numpy as np
from algorithms import *
from domains import *
from puzzleSolver import *
from Algorithms.best_first_frontier_search import *
from Algorithms.a_star_frontier_search import *
from Node.node import *
from Node.puzzle_node import *
from math import sqrt
from random import shuffle
from Algorithms.RBFS import RBFS
N = 3


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
def is_solvable(puzzle) -> bool:
    # Count inversions in given puzzle
    invCount = getInvCount(puzzle)

    # If grid is odd, return true if inversion
    # count is even.
    if (N % 2 == 1):
        return invCount % 2 == 0

    else:  # grid is even
        pos = findXPosition(puzzle)
        if (pos % 2 == 1):
            return invCount % 2 == 0
        else:
            return invCount % 2 == 1


def create_random_puzzle(size):
    """Returns a new valid random puzzle."""
    puzzle = [i for i in range(size ** 2)]
    # return [[1,0,3],[4,2,5],[7,8,6]]
    # shuffle the puzzle until it's solvable
    shuffle(puzzle)
    while not is_solvable(np.reshape(puzzle, (N, N)).tolist()):
        shuffle(puzzle)
    return np.reshape(puzzle, (N, N)).tolist()


def run_strategy(solver, q, idx, strategy_finished):
    solver.run()
    q.put([*solver.get_performance()])
    strategy_finished[idx] = 1


def create_result_file(strategies):
    header = ['puzzle']
    measures = ['nodes expanded', 'max nodes stored', 'time']
    for s in strategies:
        for m in measures:
            header.append(s.__name__ + " " + m)
    filename = f'results_{len(os.listdir("experiments")) + 1}'
    with open(fr'experiments/{filename}.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    return filename


def write_result(filename, puzzle, row_res):
    row = [puzzle, *row_res]
    with open(fr'experiments/{filename}.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)


if __name__ == '__main__':
    strategies = [BreadthFirst, BestFirstFrontierSearch, RBFS]
    filename = create_result_file(strategies)
    iteration_finished = 0
    while iteration_finished < 5:
        row_res = []
        initial_state = create_random_puzzle(N)
        print(initial_state)
        q = Queue()
        strategy_finished = Array('i', len(strategies))
        for idx, strategy in enumerate(strategies):
            s = PuzzleSolver(strategy(initial_state))
            p = Process(target=run_strategy, name=f"{strategy.__name__} run", args=(s, q, idx, strategy_finished))
            p.start()
            p.join(60 * 4)
            if p.is_alive():
                print(f"{p.name} is running... let's kill it...")

                # Terminate foo
                p.terminate()
                p.join()
                break
            else:
                perf = q.get()
                row_res.extend(perf[1:])

        if sum(strategy_finished) == len(strategies):
            write_result(filename, initial_state, row_res)
            iteration_finished += 1
