from sklearn.metrics import make_scorer
from sklearn_crfsuite import metrics


class Scoring:
    def __init__(self):
        self.score_func = metrics.flat_f1_score,
        self.average = 'weighted',
        self.labels = ['O', 'NAME', 'STRENGTH', 'PACK', 'FORM']

    # use the same metric for evaluation
    def make_scorer(self):
        return make_scorer(
            score_func=self.score_func,
            average=self.average,
            labels=self.labels
        )
