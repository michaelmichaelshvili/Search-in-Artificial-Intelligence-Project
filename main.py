from algorithms import *
from domains import *
from puzzleSolver import *
from Algorithms.best_first_frontier_search import *
from Node.node import *
from Node.puzzle_node import *

if __name__ == '__main__':

    # Best First Frontier Search
    initial_state = [[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]]
    initial = PuzzleNode([[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]])

    p = PuzzleSolver(BestFirstFrontierSearch(initial))
    print(p)
    p.run()
    p.print_performance()
    p.print_solution()

    # Frontier-A* Search
    # initial = PuzzleNode([[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]])
    #
    # p = PuzzleSolver(BestFirstFrontierSearch(initial))
    # print(p)
    # p.run()
    # p.print_performance()
    # p.print_solution()
    #
    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]])

    for strategy in [BreadthFirst, AStar]:
        p = PuzzleSolver(strategy(puzzle))
        print(p)
        p.run()
        p.print_performance()
        p.print_solution()

    # initial = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]])
    # goal = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
    # # initial = PuzzleNode([[1, 0], [3, 2]])
    # # goal = PuzzleNode([[1, 2], [3, 0]])
    # frontier = FrontierSearch(initial, goal)
    # print(frontier.do_algorithm())
