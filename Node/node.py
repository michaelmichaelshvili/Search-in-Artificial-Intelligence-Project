from functools import total_ordering


@total_ordering
class Node:
    def __init__(self, state, operators: dict, cost: list) -> None:
        super().__init__()
        self.operators = operators  # dictionary {str: bool}
        self.state = state
        self.neighbors = []
        self.cost = cost

    def __eq__(self, o) -> bool:
        print(type(o))
        return self.state == o.state if type(o) is Node else False

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return sum(self.cost) < sum(other.cost)

    def __str__(self) -> str:
        return f"pos: {self.state}\tops: {self.operators}\tcost: {sum(self.cost)}"

    def __repr__(self) -> str:
        return self.__str__()

    def expand(self, cost_function):
        raise NotImplemented

    def union(self, o):
        raise NotImplemented
