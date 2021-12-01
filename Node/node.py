from functools import total_ordering


@total_ordering
class Node:
    def __init__(self, state, operators: dict, cost: float) -> None:
        super().__init__()
        self.operators = operators  # dictionary {str: bool}
        self.state = state
        self.neighbors = []
        self.cost = cost

    def __eq__(self, o: object) -> bool:
        return self.cost == o.cost if o is Node else False

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self) -> str:
        return str(f"position: {self.state} \n operators: {self.operators}")

    def expand(self):
        raise NotImplemented
