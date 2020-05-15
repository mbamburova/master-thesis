import unicodedata

UNITS = ['mikrogram', 'mg', 'ml', 'g', 'u', 'µg', 'tv', 'pfv', 'iu', 'ha', 'log', 'val', 'ppm',
         'mbq', 'dagv', 'mmol', 'dozėje', 'mikrog', 'ui', 'unt', 'un', 'gm', 'mcg', 'ppm']


def word_to_features(sent, i):
    word = sent[i][0]

    features = {
        'bias': 1.0,
        # 'word._is_unit()': _is_unit(word),
        'word.lower()': word.lower(),
        'word[-2:]': word[-2:],
        'word[-3:]': word[-3:],
        'word[:-3]': word[:-3],  # World! -> Wor
        'word.isdigit()': word.isdigit(),
        # 'word._is_punctuation()': _is_punctuation(word)
    }

    if i > 0:
        word1 = sent[i - 1][0]
        features.update({
            # '-1:word._is_unit()': _is_unit(word1),
            '-1:word.lower()': word1.lower(),
            '-1:word.isdigit()': word1.isdigit(),
            '-1:word[:-3]': word1[:-3],
            # '-1:word._is_punctuation()': _is_punctuation(word1)
        })
    else:
        features['BOS'] = True

    # if i > 1:
    #     word2 = sent[i-2][0]
    #     features.update({
    #         '-2:word._is_unit()': _is_unit(word2),
    #         '-2:word.lower()': word2.lower(),
    #         '-2:word.isdigit()': word2.isdigit(),
    #         '-2:word[:-3]': word2[:-3],
    #         '-2:word._is_punctuation()': _is_punctuation(word2)
    #     })

    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        features.update({
            #  '+1:word._is_unit()': _is_unit(word1),
            '+1:word.lower()': word1.lower(),
            '+1:word.isdigit()': word1.isdigit(),
            '+1:word[:-3]': word1[:-3],
            # '+1:word._is_punctuation()': _is_punctuation(word1)
        })
    else:
        features['EOS'] = True

    # if i < len(sent) - 2:
    #     word2 = sent[i + 2][0]
    #     features.update({
    #         '+2:word._is_unit()': _is_unit(word2),
    #         '+2:word.lower()': word2.lower(),
    #         '+2:word.isdigit()': word2.isdigit(),
    #         '+2:word[:-3]': word2[:-3],
    #         '+2:word._is_punctuation()': _is_punctuation(word2)
    #     })

    return features


def _is_punctuation(chars):
    if len(chars) != 1:
        return False
    
    cp = ord(chars[0])
    if (33 <= cp <= 47) or (58 <= cp <= 64) or (91 <= cp <= 96) or (123 <= cp <= 126):
        return True
    
    cat = unicodedata.category(chars[0])
    return cat.startswith("P")


def _is_unit(chars):
    return chars in UNITS


def sent_to_features(sent):
    return [word_to_features(sent, i) for i in range(len(sent))]


def sent_to_labels(sent):
    return [label for token, label in sent]