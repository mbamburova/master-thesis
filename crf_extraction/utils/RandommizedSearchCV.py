from sklearn.model_selection import RandomizedSearchCV


class RandomizedSearchCrossValidator:

    def __init__(self, estimator, param_distribution, scoring):
        self.estimator = estimator
        self.param_distribution = param_distribution
        self.cv = 5,
        self.verbose = 1,
        self.n_jobs = -1,
        self.n_iter = 50,
        self.scoring = scoring

    def get_validator(self):
        return RandomizedSearchCV(
            estimator=self.estimator,
            param_distributions=self.param_distribution,
            cv=self.cv,
            verbose=self.verbose,
            n_jobs=self.n_jobs,
            n_iter=self.n_iter,
            scoring=self.scoring
        )
