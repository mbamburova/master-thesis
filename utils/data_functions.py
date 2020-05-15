import pandas as pd


def get_data(data_path):
    data = pd.read_csv(data_path, sep=";", names=['Drug: #', 'Word', 'Tag'])
    data = data.fillna(method="ffill")

    return data
