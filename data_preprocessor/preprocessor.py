import math

import pandas as pd

from data_preprocessor.helper_functions \
    import is_punctuation, \
    is_number, \
    split_word_with_number, \
    split_word_with_punctuation

FORM = 'FORM'
NAME = 'NAME'
PACK = 'PACK'
STRENGTH = 'STRENGTH'
UNDEFINED = 'O'

MAH_BLACKLIST = ['krka', 'polfa', 'fresenius', 'stada', 'medana', 'sandoz', 'meda', 'panpharma',
                 'sanitas', 'braun', 'sr', 'polpharma', 'nkc', 'teva', 'gsk', 'nycomed', 'ebewe',
                 'turbuhaler', 'flakone', 'užpildytame', 'švirkšte', 'lannacher', 'sopharma', 'hexal',
                 'licaformot', 'actavis', 'orion', 'medochemie', 'aurobindo', 'kabi', 'accord', 'hospira',
                 'zentiva', 'kabi', 'ingen', 'pharma', 'stada', 'baxter', 'ebewe', 'sanoswiss', 'mylan',
                 'portfarma', 'lannacher', 'hospira', 'elvim', 'life', 'medical', 'synthon', 'torrent',
                 'eras', 'teva', 'bv', 'dura', 'ranbaxy', 'apotex', 'hexal', 'tad', 'fresenius', 'sandoz',
                 'vitabalans', 'ingen', 'sun', 'billev', 'baxter', 'bioorganics', 'hispania', 'grindeks',
                 'liconsa', 'alvogen', 'mylan', 'lek', 'ranbaxy', 'biopartners', 'sandoz', 'pfizer',
                 'gmbh', 'vaistažolių', 'mišinys', 'nuo', 'hemorojaus', 'smulkinti', 'valerijonų',
                 'šakniastiebiai', 'su', 'šaknimis', 'pensa', 'bluefish', 'teva', 'abece', 'aurobindo',
                 'aristo', 'ebb', 'hameln', 'hexal', 'sachet', 'accord', '2care4', 'stada®', 'jubilant',
                 'amneal', 'eql', 'glenmark', 'medartuum', 'astrazeneca', 'anpharm', 'takeda', 'amneal',
                 'nordic', 'drugs', 'pharmadone', 'evolan', 'liconsa', 'medical', 'valley', 'arnet',
                 'ardeapharma', 'eumedica', 'lyfjaver', 'europharma', 'europharmad', 'europharmadk',
                 'paranova', 'chemvet', 'danmark']

UNDEFINED_BLACKLIST = ['ampule', 'lahvicka', 'roztok', 'blist', 'blister', 'flakonas', 'sylinteriampullia',
                       'sylinteriampulli', 'flakon', 'ikke', 'angitt', '(', ')', '[', ']', ',', 'inhalaattori']

STRENGTH_IN_NAME = ['mg', 'ml', '/']
DATASOURCES_WITH_STRENGTH_IN_NAME = ['BG_NCPR_PRILOGENIE_III', 'BG_NCPR_PRILOGENIE_II', 'BG_NCPR_PRILOGENIE_I',
                                     'CH_FOPH_SL_PRODUCTS_PRICES', 'IS_LGN']

DATASOURCE = 'medic'  # datasource to be preprocessed
EXPERIMENTAL_DATASET_PATH = 'experimental_dataset.csv'


def create_experimental_dataset():
    """
    This method preprocesses a provided DATASOURCE file, labels every token
    and created labelled dataset write into a file.
    Every column of every row is firstly tokenized, and then every token is labelled with NAME, STRENGTH, PACK, FORM,
    or UNDEFINED label based on conditions.
    """

    f = open(EXPERIMENTAL_DATASET_PATH, "w+")
    f.write('Sentence: #;Word;Tag\n')

    dataset = pd.read_csv("medic.csv", sep=',', quotechar='\'')
    counter = 0
    for row in dataset.iterrows():
        sentence = []
        for head in dataset.head():
            sentence.extend(label_column(row, head, None))

        i = 0
        for word, tag in sentence:
            if word == ';':
                word = '";"'
            if i == 0:
                f.write('Sentence: ' + str(counter) + ';' + word + ';' + tag + '\n')
            else:
                f.write(';' + word + ';' + tag + '\n')
            i += 1

        counter += 1

    f.close()


def _preprocess_column(column: str):
    """
    :param column: Already preprocessing column
    :return: Tokenized column
    """

    stripped = []
    for split in str(column).split():
        for punc_split in split_word_with_punctuation(split):
            for spl in split_word_with_number(punc_split):
                if spl != '':
                    stripped.append(spl.strip().lower())

    return stripped


def label_column(row: tuple, header: str, datasource: str):
    """
    
    :param row: Drug row to pre labelled
    :param header: Header from an already preprocessing file.
    :param datasource: Datasource to be preprocessed
    :return: Return a list of labelled column's tokens.
    """

    column = row[1].get(header)
    if isinstance(column, float) and math.isnan(column):
        return []

    label = header.split('.')[0]
    preprocessed_form = _preprocess_column(column)
    labelled_column = []
    for token in preprocessed_form:
        if token == '"':
            continue
        if token in UNDEFINED_BLACKLIST:
            labelled_column.append((token, UNDEFINED))
            continue
        if 'N/A' in token:
            labelled_column.append((token, UNDEFINED))
            continue
        if token == ',' and preprocessed_form.index(token) > 0:
            if preprocessed_form[preprocessed_form.index(token) - 1].isdigit() \
                    and preprocessed_form[preprocessed_form.index(token) + 1].isdigit():
                labelled_column.append((token, label))

        elif len(token) != 1 or not is_punctuation(list(token)[0]):
            if datasource in DATASOURCES_WITH_STRENGTH_IN_NAME and label == NAME \
                    and (is_number(token) or token in STRENGTH_IN_NAME):
                labelled_column.append((token, STRENGTH))

            elif datasource == 'medic' and (label == NAME or label == PACK):
                label_medic_datasource(preprocessed_form, token, label, labelled_column)

            elif label == NAME and (token in MAH_BLACKLIST or token in STRENGTH_IN_NAME):
                labelled_column.append((token, UNDEFINED))

            else:
                labelled_column.append((token, label))
        else:
            labelled_column.append((token, label))

    return labelled_column


def label_medic_datasource(preprocessed_form, token, label, labelled_column):
    """
    Method labels a token by NAME, PACK, or UNDEFINED label based on a provided conditions,
     and then adds such labelled token into a list of labelled tokens.

    :param preprocessed_form:
    :param token: word from a column to be labelled
    :param label: NAME or PACK label
    :param labelled_column: list of labelled tokens of a column
    """

    if 0 < preprocessed_form.index(token) < len(preprocessed_form) - 1:
        if label == NAME:
            if (preprocessed_form[preprocessed_form.index(token) - 1] == '"'
                    or preprocessed_form[preprocessed_form.index(token) + 1] == '"'):
                labelled_column.append((token, UNDEFINED))
            else:
                labelled_column.append((token, label))

        elif label == PACK:
            if token.isdigit():
                labelled_column.append((token, label))

            elif token != 'ml' and \
                    (preprocessed_form[preprocessed_form.index(token) - 1] == '('
                     or preprocessed_form[preprocessed_form.index(token) + 1] == ')'):
                labelled_column.append((token, UNDEFINED))
            else:
                labelled_column.append((token, label))
    else:
        labelled_column.append((token, label))
