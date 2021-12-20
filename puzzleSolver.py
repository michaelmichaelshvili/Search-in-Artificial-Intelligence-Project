class PuzzleSolver:
    def __init__(self, strategy):
        """
        :param strategy: Strategy
        """
        self._strategy = strategy


    def print_performance(self):
        print(f'{self._strategy} - Number expanded Nodes: {self._strategy.num_expanded_nodes} - max: {self._strategy.max_nodes}')

    def print_solution(self):
        if self._strategy.solution:
            print('Solution:')
            for s in self._strategy.solution:
                print(s)
        else:
            print("No solution")

    def run(self):
        # if not self._strategy.start.is_solvable():
        #     raise RuntimeError('This puzzle is not solvable')

        self._strategy.do_algorithm()