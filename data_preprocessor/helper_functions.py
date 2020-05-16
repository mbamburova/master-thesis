import re
import unicodedata

NUMBER_RE = re.compile(r'^([0-9]+(,|.)[0-9]+|[0-9]+)$')
NUMBER_STRING_FORMAT_RE = re. \
    compile(r'^(?P<number>[0-9]+)(?P<string>[a-zA-Z]+)(?P<number2>[0-9]*)(?P<string2>[a-zA-Z]*)$')


def is_number(value: str):
    if NUMBER_RE.match(value):
        return True
    return False


def split_word_with_number(word: str):
    number_string_match = NUMBER_STRING_FORMAT_RE.match(word)
    if not number_string_match:
        return [word]
    return number_string_match.groupdict().values()


def is_punctuation(char: str):
    cp = ord(char)
    if (33 <= cp <= 47) or (58 <= cp <= 64) or (91 <= cp <= 96) or (123 <= cp <= 126):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False


def split_word_with_punctuation(text: str):
    chars = list(text)
    i = 0
    start_new_word = True
    output = []
    while i < len(chars):
        char = chars[i]
        if is_punctuation(char):
            output.append([char])
            start_new_word = True
        else:
            if start_new_word:
                output.append([])
            start_new_word = False
            output[-1].append(char)
        i += 1

    return ["".join(x) for x in output]


def save(path, drug_records):
    f = open(path + ".csv", "w+")
    f.write('Drug: #;Word;Tag\n')
    counter = 0
    for sentence in drug_records:
        i = 0
        for word, tag in sentence:
            if word == ';':
                word = '";"'
            if i == 0:
                f.write('Drug: ' + str(counter) + ';' + word + ';' + tag + '\n')
            else:
                f.write(';' + word + ';' + tag + '\n')
            i += 1

        counter += 1
    f.close()
