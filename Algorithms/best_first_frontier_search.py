import heapq
from strategy import *


class BestFirstFrontierSearch(Strategy):
    def __init__(self, initial) -> None:
        super().__init__()
        self.open_list = [initial]
        heapq.heapify(self.open_list)
        self.goal = initial.PUZZLE_END_POSITION
        self.max_nodes = 1

    # def union_nodes(self, node1: Node, node2: Node):
    #     if node1.state != node2.state:
    #         raise ValueError("The nodes are not in same state")
    #     return PuzzleNode(node1.state,
    #                 {k1: v1 or v2 for ((k1, v1), (k2, v2)) in zip(node1.operators.items(), node2.operators.items())},
    #                 min(node1.cost, node2.cost))

    def expand(self, node):
        neighbors = node.expand()
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

    def __str__(self):
        return 'Frontier Search'
