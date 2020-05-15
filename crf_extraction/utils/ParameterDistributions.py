import numpy
import scipy.stats


class ParameterDistributions:

    def __init__(self):
        self.l1_regularization_coef = scipy.stats.expon(scale=0.5)
        self.l2_regularization_coef = scipy.stats.expon(scale=0.05)
        self.max_iterations = 1 #[int(x) for x in numpy.linspace(start=40, stop=150, num=10)]
        self.all_possible_transitions = [True, False]

    def __str__(self):
        return str(self.get_param_grid())

    def get_param_grid(self):
        random_grid = {
            'c1': self.l1_regularization_coef,
            'c2': self.l1_regularization_coef,
            'max_iterations': self.max_iterations,
            'all_possible_transitions': self.all_possible_transitions
        }

        return random_grid
