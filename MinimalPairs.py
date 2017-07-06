import json
import csv
import io
import os
import Preprocessing


def json_writer(filename):
    groups_of_minimal_pairs = []

    info = []

    minimal_pairs = []
    group = []

    os.chdir('/Users/robingranberry/PycharmProjects/JSONBuilder/Minimal Pairs Info')

    with open(filename) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            if row[0] == 'New':
                if len(group) != 0:
                    info.append(group)
                group = []
                minimal_pairs.append([Preprocessing.timitToPhoneme(row[1]), Preprocessing.timitToPhoneme(row[2])])
            else:
                group.append(row)
        info.append(group)

    for pair_index in range(0, len(info)):
        pairs = []
        for word_index in range(0, len(info[pair_index]), 4):
            phonemes1 = build_phoneme_object(pair_index, word_index, info)
            phonemes2 = build_phoneme_object(pair_index, word_index + 2, info)

            first_word = {'file_name': info[pair_index][word_index][0],
                          'word': info[pair_index][word_index][1],
                          'min_pair_phoneme_index': Preprocessing.toInt(info[pair_index][word_index][2]),
                          'phonemes': phonemes1
                          }

            second_word = {'file_name': info[pair_index][word_index + 2][0],
                           'word': info[pair_index][word_index + 2][1],
                           'min_pair_phoneme_index': Preprocessing.toInt(info[pair_index][word_index + 2][2]),
                           'phonemes': phonemes2
                           }

            pair = {'first_word': first_word,
                    'second_word': second_word
                    }

            pairs.append(pair)

        pair_obj = {'paired_phonemes': minimal_pairs[pair_index],
                    'pairs': pairs

                    }
        groups_of_minimal_pairs.append(pair_obj)
    print(groups_of_minimal_pairs)

    with io.open('NewMinimalPairs.json', 'w', encoding='utf8') as outfile:

        json.dump(groups_of_minimal_pairs, outfile, ensure_ascii=False)


def build_phoneme_object(pair_index, word_index, info):
    phonemes = []
    for phoneme_index in range(3, len(info[pair_index][word_index])):
        if info[pair_index][word_index][phoneme_index] == '':
            break
        start = 0 if phoneme_index == 3 else \
            Preprocessing.toInt((info[pair_index][word_index + 1][phoneme_index - 1])) + 1
        end = Preprocessing.toInt(info[pair_index][word_index + 1][phoneme_index])

        phoneme = {'phoneme': info[pair_index][word_index][phoneme_index],
                   'start': start,
                   'end': end
                   }
        phonemes.append(phoneme)
    return phonemes

json_writer('JSON - Sheet1.csv')
