from sklearn_crfsuite import CRF


class CRFClassifier(object):

    def __init__(self, c1, c2, max_iterations, all_possible_transitions):
        self.algorithm = 'lbfgs'
        self.c1 = c1  # default 0
        self.c2 = c2  # default 1
        self.max_iterations = max_iterations
        self.all_possible_transitions = all_possible_transitions
        # self.verbose = 0

    # use the same metric for evaluation
    def get_crf_classifier(self):
        crf = CRF(
            algorithm=self.algorithm,
            c1=self.c1,  # default 0
            c2=self.c2,  # default 1
            max_iterations=self.max_iterations,
            all_possible_transitions=self.all_possible_transitions,
            verbose=0,
        )

        return crf
