from strategy import *
import heapq
from Node.node import Node


class AStarFrontierSearch(Strategy):
    def __init__(self, initial) -> None:
        super().__init__()
        initial.cost = initial.heuristic_manhattan_distance()
        self.open_list = [initial]
        # heapq.heapify(self.open_list)
        self.goal = initial.PUZZLE_END_POSITION
        self.max_nodes = 1

    def __str__(self):
        return 'A* FrontierSearch'

    def cost_function(self, parent, child):
        return parent.cost + child.heuristic_manhattan_distance() - parent.heuristic_manhattan_distance()

    # def expand(self, node):
    #     neighbors = node.expand(self.cost_function)
    #     self.num_expanded_nodes += 1
    #     for n in neighbors:
    #         try:
    #             idx = self.open_list.index(n)
    #             old_n = self.open_list[idx]
    #             new_n = old_n.union(n)
    #             del self.open_list[idx]
    #             heapq.heappush(self.open_list, new_n)
    #         except:  # n not in open list
    #             heapq.heappush(self.open_list, n)

    def expand(self, node):
        neighbors = node.expand(self.cost_function)
        self.num_expanded_nodes += 1
        for n in neighbors:
            try:
                idx = self.open_list.index(n)
                old_n = self.open_list[idx]
                new_n = old_n.union(n)
                self.open_list[idx] = new_n
            except Exception as e:  # n not in open list
                self.open_list.append(n)

    def find_min_node(self):
        i = 0
        for j in range(1, len(self.open_list)):
            if self.open_list[i].cost > self.open_list[j].cost:  # minimum
                i = j
        min_node = self.open_list[i]
        del self.open_list[i]
        return min_node

    def do_algorithm(self):
        self.solution = []
        while len(self.open_list) > 0:
            self.max_nodes = max(self.max_nodes, len(self.open_list))
            next_node = self.find_min_node()
            self.solution.append(next_node)
            if next_node.state == self.goal:
                return "SUCCESS"
            self.expand(next_node)
        return "The are no nodes for expansion"
