import re
from collections import defaultdict


def process_phonemes(filename):
    text = open(filename, 'r')
    new_text = []

    for row in text:
        new_row = row.split(' ')
        phoneme = timitToPhoneme(new_row[2].rstrip("\n"))

        if phoneme == '  ':
            continue

        if len(new_text) != 0:
            if phoneme == new_text[-1][2]:
                new_text[-1][2] = toInt(new_row[1])
            else:
                new_text.append([phoneme, toInt(new_row[0]), toInt(new_row[1])])

        else:
            new_text.append([phoneme, toInt(new_row[0]), toInt(new_row[1])])
    return new_text


def process_letters(filename, filename2):
    phoneme_text = open(filename, 'r')
    word_text = open(filename2, 'r')

    word_times = []
    words = []

    # get all of the separate words associated with their times as well as a list of letters
    for row in word_text:
        new_row = row.split(' ')
        word_times.append([toInt(new_row[0]), toInt(new_row[1])])
        letters = []
        for char in new_row[2].rstrip('\n'):
            letters.append([char])
        words.append(letters)

    word_count = 0

    end_time = word_times[word_count][1]
    phonemes_per_word = []
    current_phonemes = defaultdict(list)

    for row in phoneme_text:
        new_row = row.split(' ')
        if new_row[2].rstrip('\n') == 'h#':
            continue

        phoneme = timitToPhoneme(new_row[2].rstrip('\n'))

        current_phonemes[None] = [[0]]

        # add phonemes together
        if phoneme in current_phonemes.keys():
            # combine together two of the same phoneme (pcl and p)
            if current_phonemes[phoneme][0][1] == toInt(new_row[0]):
                current_phonemes[phoneme][0][1] = toInt(new_row[1])
            # add a separate time to a preexisting phoneme
            else:
                current_phonemes[phoneme].append([toInt(new_row[0]), toInt(new_row[1])])
        # create a new phoneme
        else:
            current_phonemes[phoneme] = [[toInt(new_row[0]), toInt(new_row[1])]]

        # separate phonemes into words
        if toInt(new_row[1]) == end_time:
            phonemes_per_word.append(current_phonemes)
            current_phonemes = defaultdict(list)
            if word_count < len(word_times) - 1:
                word_count += 1
                end_time = word_times[word_count][1]

    all_letter_times = []
    word_letter_times = []
    start_time = 0
    letters = ''

    # iterate over every word
    for word_index in range(0, len(words)):
        # iterate over every letter in the word
        for letter_index in range(0, len(words[word_index])):
            # add the current letter to the list of letters
            letter = words[word_index][letter_index][0]
            letters += letter

            # if the phoneme had a one to one correspondence in the word, you know where it is located and can add times
            if letter in list(phonemes_per_word[word_index].keys()):
                # end_time is the end time of the corresponding phoneme
                end_time = phonemes_per_word[word_index][letter][0][1]

                # if there are no other letters, the times will directly correspond
                if len(letters) == 1:
                    start_time = phonemes_per_word[word_index][letter][0][0]
                    all_letter_times.append([letters, start_time, end_time])

                # otherwise, split the current letters into even chunks and add them all
                else:
                    # split the times into even chunks
                    times = int((end_time - start_time) / len(letters))
                    for char in letters:
                        end = start_time + times
                        all_letter_times.append([char, start_time, end])
                        start_time = end
                        # end_time += times
                        # end_time = phonemes_per_word[word_index][letter][1]

                letters = ''
                start_time = phonemes_per_word[word_index][letter][0][1]

                # remove the time for that specific letter from the phoneme key in case there are multiple instances
                # of that letter in the word
                phonemes_per_word[word_index][letter].pop(0)

                # if the value of the phoneme is empty, remove it as a key
                if len(phonemes_per_word[word_index][letter]) == 0:
                    del phonemes_per_word[word_index][letter]

            # if the end of the word is not a recognized phoneme, add the remaining letters to the list
            elif letter_index == len(words[word_index]) - 1:
                end_time = word_times[word_index][1]
                times = int((end_time - start_time) / len(letters))

                for char in letters:
                    end = start_time + times
                    all_letter_times.append([char, start_time, end])
                    start_time = end

                letters = ''

                if word_index != len(word_times) - 1:
                    start_time = word_times[word_index + 1][0]

                    # print('Word_letter_times: ', word_letter_times)
        # all_letter_times.append(word_letter_times)
        word_letter_times = []
        # all_letter_times.append([' ', start_time, end_time])
    print('All_letter_times: ', all_letter_times)

    return all_letter_times


def timitToPhoneme(x):
    return {
        'a': 'a',
        'b': 'b',
        'c': 'c',
        'd': 'd',
        'e': 'e',
        'f': 'f',
        'g': 'g',
        'h': 'h',
        'i': 'i',
        'j': 'j',
        'k': 'k',
        'l': 'l',
        'm': 'm',
        'n': 'n',
        'o': 'o',
        'p': 'p',
        'q': '  ',
        'r': 'r',
        's': 's',
        't': 't',
        'u': 'u',
        'v': 'v',
        'w': 'w',
        'x': 'x',
        'y': 'y',
        'z': 'z',
        'aa': 'a',
        'bcl': 'b',
        'dcl': 'd',
        'gcl': 'g',
        'kcl': 'k',
        'pcl': 'p',
        'tcl': 't',
        'ae': u"\u00C6",
        'ng': u"\u014B",
        'ah': u"\u028C",
        'ch': u"\u02A7",
        'dh': u"\u00f0",
        'eh': u"\u025B",
        'hh': 'h',
        'ih': u"\u026A",
        'jh': 'j',
        'sh': u"\u0283",
        'th': u"\u03B8",
        'el': u"\u0259" + 'l',
        'en': u"\u0259" + 'n',
        'ao': u"\u0254",
        'er': u"\u025C",
        'hv': 'h',
        'aw': 'a' + u"\u028A",
        'ow': 'o' + u"\u028A",
        'uw': 'u',
        'ax': 'a' + u"\u028A",
        'ax-h': u"\u028C",
        'axr': u"\u0259" + 'r',
        'dx': 'd',
        'ix': u"\u026A",
        'ux': 'u',
        'ay': 'a' + u"\u026A",
        'ey': 'e' + u"\u026A",
        'iy': 'i',
        'θ': u"\u03B8",
        'ɛ': u"\u025B",
        'ɪ': u"\u026A",
        'ʌ': u"\u028C",
        'ŋ': u"\u014b",
        'ð': u"\u00f0",
        'æ': u"\u00e6",
        'ə': u"\u0259",
        'ɑ': u"\u0251",
        'ɜ': u"\u025C",
        'ʧ': u"\u02A7",
        'ɔ': u"\u0254",
        'ʊ': u"\u028A",
        'oʊ': 'o' + u"\u028A",
        'aʊ': 'a' + u"\u028A",
        'eɪ': 'e' + u"\u026A",
        'aɪ': 'a' + u"\u026A",
        'Pre': 'Pre',
        'pau': 'pause',
        'h#': 'pause',
    }.get(x, 'Phoneme not in database')


def toInt(string):
    return int(re.search(r'\d+', string).group())
