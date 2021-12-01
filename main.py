from algorithms import *
from domains import *
from puzzleSolver import *
from strategy import *



if __name__ == '__main__':
    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]])

    for strategy in [BreadthFirst, AStar]:
        p = PuzzleSolver(strategy(puzzle))
        p.run()
        p.print_performance()
        p.print_solution()