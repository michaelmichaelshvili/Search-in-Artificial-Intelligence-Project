class Strategy:
    num_expanded_nodes = 0
    solution = None
    max_nodes = 0
    done = False

    def do_algorithm(self):
        raise NotImplemented