from strategy import *
import heapq
from Node.node import Node


class AStarFrontierSearch(Strategy):
    def __init__(self, initial) -> None:
        super().__init__()
        initial.cost = [0, initial.heuristic_manhattan_distance()]
        self.open_list = [initial]
        heapq.heapify(self.open_list)
        self.goal = initial.PUZZLE_END_POSITION
        self.max_nodes = 1

    def __str__(self):
        return 'A* FrontierSearch'

    def expand(self, node):
        neighbors = node.expand(lambda parent, child: [parent.cost[0] , child.heuristic_manhattan_distance() - parent.heuristic_manhattan_distance()])
        self.num_expanded_nodes += 1
        for n in neighbors:
            try:
                idx = self.open_list.index(n)
                old_n = self.open_list[idx]
                new_n = old_n.union(n)
                del self.open_list[idx]
                heapq.heappush(self.open_list, new_n)
            except:  # n not in open list
                heapq.heappush(self.open_list, n)

    def do_algorithm(self):
        self.solution = []
        while len(self.open_list) > 0:
            self.max_nodes = max(self.max_nodes, len(self.open_list))
            next = heapq.heappop(self.open_list)
            self.solution.append(next)
            if next.state == self.goal:
                return "SUCCESS"
            self.expand(next)
        return "The are no nodes for expansion"
