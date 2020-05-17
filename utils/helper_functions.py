import pandas as pd
import seaborn as sns

TAGS = ['NAME', 'STRENGTH', 'PACK', 'FORM', 'O']


def get_data(data_path):
    """
    Read a comma-separated values from a csv file into DataFrame.
    :param data_path: source file path
    :return: Comma-separated values from a csv file.
    """

    data = pd.read_csv(data_path, sep=";", names=['Drug: #', 'Word', 'Tag'])
    data = data.fillna(method="ffill")

    return data


def generate_heatmap_values(matrix):
    return _generate_heatmap(matrix, 'd')


def generate_heatmap_percentage(matrix):
    return _generate_heatmap(matrix, '.4g')


def _generate_heatmap(matrix, fmt):
    """
    Generate a heatmap plot from 2D data
    :param matrix: 2D data
    :param fmt: String formatting code to use when adding annotations
    :return: Genrated plot as a color-encoded matrix.
    """

    return sns.heatmap(matrix,
                       annot=True,
                       fmt=fmt,
                       cmap=sns.cubehelix_palette(200, start=2, rot=0, dark=0, light=.95, reverse=False))


def join_true_values_with_predicted(true_values, predicted_values):
    """
    :param true_values:
    :param predicted_values:
    :return: Joined true and predicted values in a form of dictionary.
    """

    joined_values = []
    i = 0
    for true_value in true_values:
        merged_sentence = []
        j = 0
        for word in true_value:
            merged_sentence.append((word[0], predicted_values[i][j]))
            j += 1
        joined_values.append(merged_sentence)
        i += 1

    return joined_values


def save_predicted_results(drug_records, file_path):
    """
    Save predicted results in a tabular csv format.
    :param drug_records: predicted results
    :param file_path:
    :return: None
    """

    f = open(file_path, "w+")
    f.write('NAME;STRENGTH;PACK;FORM;O\n')

    for line in _compose_prediction_results(drug_records):
        result_line = ""
        for tag in TAGS:
            tag_column = line.get(tag) or ""
            if tag_column is not "":
                tag_column = ' '.join(''.join(t) for t, j in tag_column)

            if tag == 'NAME':
                result_line = tag_column
            else:
                result_line = result_line + ";" + tag_column

        f.write(result_line + '\n')

    f.close()


def _compose_prediction_results(drug_records):
    """
    Compose predicted results in a form of dictionary.
    :param drug_records: predicted results
    :return: Composed predicted results.
    """

    result = []
    for drug in drug_records:
        drug_result = {}
        for x, y in drug:
            if y in drug_result:
                drug_result[y].append((x, y))
            else:
                drug_result[y] = [(x, y)]
        result.append(drug_result)

    return result
