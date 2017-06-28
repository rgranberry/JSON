import json
import io
import os
import Preprocessing


def jsonWriterPhonemesOnly(in_file, new_file, sentence):
    os.chdir('/Users/robingranberry/PycharmProjects/JSONBuilder/TIMIT Info')

    text = Preprocessing.process_phonemes(in_file)

    phonemes = build_obj(text, 'phoneme')

    file = in_file.split('.')[0] + '.wav'

    json_obj = {'Filename': file,
                'Text': sentence,
                'PhonemeInfo': phonemes}

    with io.open(new_file, 'w', encoding='utf8') as outfile:
        json.dump(json_obj, outfile, ensure_ascii=False)


def jsonWriter(in_file, new_file, sentences, sentence):
    os.chdir('/Users/robingranberry/PycharmProjects/JSONBuilder/TIMIT Info')

    word_text = Preprocessing.process_phonemes(in_file)

    letter_text = Preprocessing.process_letters(in_file, sentences)

    phonemes = build_obj(word_text, 'phoneme')
    letters = build_obj(letter_text, 'letter')

    file = in_file.split('.')[0] + '.wav'

    json_obj = {'Filename': file,
                'Text': sentence,
                'PhonemeInfo': phonemes,
                'LetterTimingInfo': letters}

    with io.open(new_file, 'w', encoding='utf8') as outfile:
        json.dump(json_obj, outfile, ensure_ascii=False)


def build_obj(text, word):

    array = []

    for row in text:
        info = {word: row[0],
                'start': row[1],
                'end': row[2]
                }
        array.append(info)
    return array


jsonWriter('SX295.txt', 'SX295_MAJC0.json', 'SX295_words.txt',
           'If Carol comes tomorrow, have her arrange for a meeting at two.')

jsonWriter('SI904.txt', 'SI904_MGLB0.json', 'SI904_words.txt',
           'He peered ahead and grinned as the railroad tracks came into view again below.')

jsonWriter('SX289.txt', 'SX289_FTLH0.json', 'SX289_words.txt', 'Weatherproof galoshes are very useful in Seattle.')

jsonWriter('SX138.txt', 'SX138_MPAB0.json', 'SX138_words.txt', 'The clumsy customer spilled some expensive perfume.')
#
jsonWriter('SI2300.txt', 'SI2300_FMML0.json', 'SI2300_words.txt', 'My mother was beside herself with curiosity.')
#
jsonWriter('SX209.txt', 'SX209_MERS0.json', 'SX209_words.txt', 'Michael colored the bedroom wall with crayons.')

jsonWriter('SX139.txt', 'SX139_MDAB0.json', 'SX139_words.txt', 'The bungalow was pleasantly situated near the shore.')

jsonWriter('SX313.txt', 'SX313_FAKS0.json', 'SX313_words.txt', 'Drop five forms in the box before you go out.')
