def get_aggregate_function():
    return lambda s: [(w, t) for w, t in zip(s["Word"].values.tolist(), s["Tag"].values.tolist())]


class DrugRecords(object):

    def __init__(self, data):
        self.n_sent = 1
        self.data = data
        self.grouped = self.data.groupby("Drug: #").apply(get_aggregate_function())
        self.drug_records = [s for s in self.grouped]

    def get_next_drug_record(self):
        try:
            s = self.grouped["Drug: {}".format(self.n_sent)]
            self.n_sent += 1
            return s
        except:
            return None

    def get_drug_records(self):
        return self.drug_records
