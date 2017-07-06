import json
import csv
import io
import os
import Preprocessing


def json_writer(filename):
    groups_of_words = []

    info = []

    words = []
    group = []

    # redirect to the folder with all of the correct files
    os.chdir('/Users/robingranberry/PycharmProjects/JSONBuilder/CaST Info')

    with open(filename) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(read_csv):
            if row[0] == 'New':
                if len(group) != 0:
                    info.append(group)
                group = []
                words.append(row[1])
            else:
                group.append(row)
        info.append(group)

    for word_index in range(0, len(info)):
        words_in_group = []
        for speaker_index in range(0, len(info[word_index]), 2):

            speaker = {'file_name': info[word_index][speaker_index][0],
                       'phoneme_index': Preprocessing.toInt(info[word_index][speaker_index][2]),
                       'phonemes': build_phoneme_object(word_index, speaker_index, info)
                       }

            words_in_group.append(speaker)

        pair_obj = {'word': info[word_index][0][1],
                    'speakers': words_in_group
                    }
        groups_of_words.append(pair_obj)
    print(groups_of_words)

    with io.open('CaST.json', 'w', encoding='utf8') as outfile:

        json.dump(groups_of_words, outfile, ensure_ascii=False)


def build_phoneme_object(pair_index, word_index, info):
    phonemes = []
    for phoneme_index in range(3, len(info[pair_index][word_index])):
        if info[pair_index][word_index][phoneme_index] == '':
            break
        start = 0 if phoneme_index == 3 else \
            Preprocessing.toInt((info[pair_index][word_index + 1][phoneme_index - 1]))
        end = Preprocessing.toInt(info[pair_index][word_index + 1][phoneme_index])

        phoneme = {'phoneme': info[pair_index][word_index][phoneme_index],
                   'start': start,
                   'end': end
                   }
        phonemes.append(phoneme)
    return phonemes


json_writer('JSON - Sheet2.csv')
