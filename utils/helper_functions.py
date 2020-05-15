import pandas as pd
import seaborn as sns


def get_data(data_path):
    data = pd.read_csv(data_path, sep=";", names=['Drug: #', 'Word', 'Tag'])
    data = data.fillna(method="ffill")

    return data


def generate_heatmap_values(matrix):
    return _generate_heatmap(matrix, 'd')


def generate_heatmap_percentage(matrix):
    return _generate_heatmap(matrix, '.4g')


def _generate_heatmap(matrix, fmt):
    return sns.heatmap(matrix,
                       annot=True,
                       fmt=fmt,
                       cmap=sns.cubehelix_palette(200, start=2, rot=0, dark=0, light=.95, reverse=False))
