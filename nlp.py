from nltk import ngrams
import codecs
from collections import Counter
import csv

wordDict_unigram_hafez = Counter()
wordDict_bigram_hafez = Counter()
word_unigram_Probability_hafez = {}
word_bigram_Probability_hafez = {}
wordDict_unigram_ferdowsi = Counter()
wordDict_bigram_ferdowsi = Counter()
word_unigram_Probability_ferdowsi = {}
word_bigram_Probability_ferdowsi = {}
wordDict_unigram_molavi = Counter()
wordDict_bigram_molavi = Counter()
word_unigram_Probability_molavi = {}
word_bigram_Probability_molavi = {}
hafez_address = "Train_set/hafez_train.txt"
ferdowsi_address = "Train_set/ferdowsi_train.txt"
molavi_address = "Train_set/molavi_train.txt"


def number_of_words_poet(address):
    file = open(address, "rt", encoding='UTF-8')
    data = file.read()
    words = data.split()
    total_num_words = len(words)
    return total_num_words


def probabilities(address, wordDict_unigram, wordDict_bigram, word_unigram_probability, word_bigram_probability,
                  total_num_words):
    with codecs.open(address, 'r', encoding='UTF-8') as f:
        for line in f:
            wordDict_unigram.update(line.strip().split())
            wordDict_bigram.update(ngrams(line.strip().split(), 2))

    for word, count in wordDict_unigram.most_common():
        word_unigram_probability.update({word: count / total_num_words})
        # print(word, count)

    for word, count in wordDict_bigram.most_common():
        word_bigram_probability.update({word: count / total_num_words})



hafez_word_count = number_of_words_poet(hafez_address)
ferdowsi_word_count = number_of_words_poet(ferdowsi_address)
molavi_word_count = number_of_words_poet(molavi_address)

probabilities(hafez_address, wordDict_unigram_hafez, wordDict_bigram_hafez, word_unigram_Probability_hafez,
              word_bigram_Probability_hafez, hafez_word_count)
probabilities(ferdowsi_address, wordDict_unigram_ferdowsi, wordDict_bigram_ferdowsi, word_unigram_Probability_ferdowsi,
              word_bigram_Probability_ferdowsi, ferdowsi_word_count)
probabilities(molavi_address, wordDict_unigram_molavi, wordDict_bigram_molavi, word_unigram_Probability_molavi,
              word_bigram_Probability_molavi, molavi_word_count)

with open('Test_set/test_file.txt', encoding='UTF-8') as f:
    first_column = [{row[1]: row[0]} for row in csv.reader(f, delimiter='\t')]

landa1_fer = 0.7
landa2_fer = 0.1
landa3_fer = 0.2
epsilone_fer = 0.1
landa1_hafez = 0.7
landa2_hafez = 0.1
landa3_hafez = 0.2
epsilone_hafez = 0.1
landa1_mol = 0.8
landa2_mol = 0.1
landa3_mol = 0.1
epsilone_mol = 0.1
ferdowsi_prob = 0
hafez_prob = 0
molavi_prob = 0
correct_guess = 0

for i in range(len(first_column)):
    unigram_str = "".join(first_column[i].keys()).strip().split()
    bigram_str = ngrams("".join(first_column[i].keys()).split(), 2)
    print("".join(first_column[i].keys()))

    for grams in bigram_str:
        if grams in word_bigram_Probability_ferdowsi:
            ferdowsi_prob += landa3_fer * word_bigram_Probability_ferdowsi[grams]

    for grams in unigram_str:
        if grams in word_unigram_Probability_ferdowsi:
            ferdowsi_prob += (landa2_fer * word_unigram_Probability_ferdowsi[grams]) + (landa1_fer * epsilone_fer)

    for grams in bigram_str:
        if grams in word_bigram_Probability_hafez:
            hafez_prob += landa3_hafez * word_bigram_Probability_hafez[grams]

    for grams in unigram_str:
        if grams in word_unigram_Probability_hafez:
            hafez_prob += landa2_hafez * word_unigram_Probability_hafez[grams] + (landa1_hafez * epsilone_hafez)

    for grams in bigram_str:
        if grams in word_bigram_Probability_molavi:
            molavi_prob += landa3_mol * word_bigram_Probability_molavi[grams]

    for grams in unigram_str:
        if grams in word_unigram_Probability_molavi:
            molavi_prob += landa2_mol * word_unigram_Probability_molavi[grams] + (landa1_mol * epsilone_mol)

    if ferdowsi_prob > hafez_prob and ferdowsi_prob > molavi_prob:
        print("poet is ferdowsi")
        if "".join(first_column[i].values()) == '1':
            print("correct guess")
            correct_guess += 1
    elif hafez_prob > ferdowsi_prob and hafez_prob > molavi_prob:
        print("poet is hafez")
        if "".join(first_column[i].values()) == '2':
            print("correct guess")
            correct_guess += 1
    elif molavi_prob > hafez_prob and molavi_prob > ferdowsi_prob:
        print("poet is molavi")
        if "".join(first_column[i].values()) == '3':
            print("correct guess")
            correct_guess += 1
    print("**********************************")


print("Accurate diagnosis" , (correct_guess / len(first_column)) * 100)
