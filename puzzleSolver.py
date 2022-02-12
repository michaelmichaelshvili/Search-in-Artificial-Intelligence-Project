from time import time
class PuzzleSolver:
    def __init__(self, strategy):
        """
        :param strategy: Strategy
        """
        self._strategy = strategy


    def get_performance(self):
        print(f'{self._strategy} - Number expanded Nodes: {self._strategy.num_expanded_nodes} - max: {self._strategy.max_nodes} - time: {self._strategy.time}')
        return self._strategy, self._strategy.num_expanded_nodes, self._strategy.max_nodes, self._strategy

    def print_solution(self):
        if self._strategy.solution[-1].state == self._strategy.goal:
            print('Solution:')
            for s in self._strategy.solution:
                print(s)
        else:
            print("No solution")

    def run(self):
        # if not self._strategy.start.is_solvable():
        #     raise RuntimeError('This puzzle is not solvable')
        print(str(self._strategy) + " is running")
        start = time()
        self._strategy.do_algorithm()
        self._strategy.time = time() - start