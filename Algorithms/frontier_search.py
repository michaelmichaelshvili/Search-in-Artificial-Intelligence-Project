from Node.node import Node
import heapq

class FrontierSearch:
    def __init__(self, initial: Node, goal: Node) -> None:
        super().__init__()
        self.open_list =[initial]
        heapq.heapify(self.open_list)
        self.goal = goal
        self.max_nodes = 1

    def union_nodes(self, node1: Node, node2: Node):
        if (node1.state != node2.state):
            raise ValueError("The nodes are not in same state")
        return Node(node1.state,
                    {k1: v1 or v2 for ((k1, v1), (k2, v2)) in zip(node1.operators.items(), node2.operators.items())},
                    min(node1.cost, node2.cost))
    def expand(self):
        if len(self.open_list) == 0:
            raise Exception("The are no nodes to expansion")
        next = heapq.heappop(self.open_list)
        if next == self.goal:
            return "SUCCESS"
        neighbors = next.expand()
        for n in neighbors:
            try:
                idx = self.open_list.index(n)
                old_n = self.open_list[idx]
                new_n = self.union_nodes()
            except:
                idx = -1
            if idx != -1: # n in
                self.open_list[self.open_list.index(n)]
            else:
                pass



