def word_to_features(sent, i):
    word = sent[i][0]

    features = {
        'bias': 1.0,
        'word[-2:]': word[-2:],
        'word[:-3]': word[:-3],
        'word.isdigit()': word.isdigit(),
    }

    if i > 0:
        word1 = sent[i - 1][0]
        features.update({
            '-1:bias': 1.0,
            '-1:word[-2:]': word1[-2:],
            '-1:word[:-3]': word1[:-3],
            '-1:word.isdigit()': word1.isdigit(),
        })
    else:
        features['BOS'] = True

    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        features.update({
            '+1:bias': 1.0,
            '+1:word[-2:]': word1[-2:],
            '+1:word[:-3]': word1[:-3],
            '+1:word.isdigit()': word1.isdigit(),
        })
    else:
        features['EOS'] = True

    return features


def sent_to_features(sent):
    return [word_to_features(sent, i) for i in range(len(sent))]


def sent_to_labels(sent):
    return [label for token, label in sent]


def sent2tokens(sent):
    return [token for token, label in sent]
