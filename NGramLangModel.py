# This file will contain functions that are useful in NGram Language Modeling
# By Ari Boyarsky


# Imports
import re
import math
# Classes
# This class will hold info about each language model useful in our analysis
class NGram:
    def __init__(self, name, n, ngrams, unigrams, probs, tokensCount, tokens):
        self.name = name
        self.n = n
        self.tokens = tokens
        self.tokensCount = tokensCount
        self.ngrams = ngrams
        self.unigrams = unigrams
        self.probs = probs

# Todo: Make this regexp more comprehensive
# letter_tokenize, will return a letter tokenized list based on a given corpus
def letter_tokenize(corpus):
    # tokenize based on letter, and punctuation, leaving out digits
    tokenized = re.findall('[\sA-Za-z.,!@#$-+=?%^&*\(\)+\{\};:\'\"]', corpus)

    # clean tokenized i.e. remove ''
    tokens_cleaned = list(filter(None, tokenized))

    return tokens_cleaned


# word_tokenize, will return a tokenized word list based on a given corpus
def word_tokenize(corpus):
    # tokenize based on word, regexp = (\w|-)+
    # We assume here that a hyphantated word is a single word
    tokenized = re.findall('[A-Za-z]+', corpus)

    # clean list to remove ''
    tokens_cleaned = list(filter(None, tokenized))

    return tokens_cleaned


# get_unigram_freq, will return a dictionary of unigram frequencies based on a tokenized list
def get_unigram_freq(tokens):
    # create unigram dict
    unigrams = {}

    for t in tokens:
        if t in unigrams.keys():
            unigrams[t] += 1
        else:
            unigrams[t] = 1
    return unigrams


# get_bigram_dist, will return a dictionary of bigram probalities based on
def get_bigram_dist(tokens, unigrams):
    # create dictionary with letter bigrams and count
    bigram_dict = {}

    i = 0
    for t in tokens:
        if i < len(tokens) - 1:
            if (t, tokens[i + 1]) in bigram_dict.keys():
                bigram_dict[(t, tokens[i + 1])] += 1
            else:
                bigram_dict[(t, tokens[i + 1])] = 1
        i += 1

    # calculate probability
    for ngram in bigram_dict.keys():
        bigram_dict[ngram] = bigram_dict[ngram] / tokens.count(ngram[0])

    return bigram_dict
###############################################
# The following are generilized functions

# ngram_dict will create a ngram, size n, with ngram frequencies
def ngram_dict(n, tokens):
    # ngram dict
    ngrams = {}

    # start of document tags
    for i in range(n):
        tokens.insert(0, "[[START]]")

    index = 0
    for t in range(len(tokens)):
        ngram = ()

        for i in range(n):
            # In case we get to end of document
            if t + i >= len(tokens):
                ngram += ("[[END]]",)
            else:
                ngram += (tokens[t+i],)

        if ngram in ngrams:
            ngrams[ngram] += 1
        else:
            ngrams[ngram] = 1

        index += 1
    return ngrams

def calc_NGram_class(n, tokens, name):
    # calc unigrams
    unigrams = ngram_dict(1, tokens)
    # calc ngrams
    ngrams = ngram_dict(n, tokens)
    count = 0
    # start and end of document tags + 1 = 3
    tokensCount = len(tokens) + 3
    probs = {}

    for k, v in ngrams.items():
        if(k[0], ) in unigrams:
            count = unigrams[(k[0]),]
        if count == 0:
            probs[k] = 0.0000000001
        else:
            probs[k] = v/tokensCount

    model = NGram(name, n, ngrams, unigrams, probs, tokensCount, tokens)

    return model

def add_one_smoothing(lineModel, langModels):
    results = []
    for lang in langModels:
        for ngram in lineModel:
            if ngram not in lang.ngrams:
                lang.unigrams[ngram] = 0
                lang.ngrams[ngram] = 0
        # add 1 to each ngram, recalc probability
        assert isinstance(lang.ngrams, object)
        for n in lang.unigrams:
            lang.unigrams[n] += 1
        for n in lang.ngrams:
            lang.ngrams[n] += 1
            # get new probs: ngram count / (ngram count + number of unigrams)
            lang.probs[n] = lang.ngrams[n] / (lang.tokensCount + len(lang.unigrams))*100
        results.append(lang)
    return results
# this function will recalculate the lang models based on katz back off
def katz_back_off(testGrams, langModels):
    results = []
    # calc bigram model
    for lang in langModels:
        # create bigram model
        bigrams = calc_NGram_class(2, lang.tokens, lang.name)
        for ngram in testGrams:
            if ngram not in lang.ngrams:
                # check bigrams
                bigram_1 = (ngram[0], ngram[1])
                bigram_2 = (ngram[1], ngram[2])

                # for simplicity we will take the probability of the last viable option
                if bigram_1 not in bigrams.ngrams and bigram_2 not in bigrams.ngrams:
                    # all false go to unigrams
                    if ngram[0] not in lang.unigrams and ngram[1] not in lang.unigrams and ngram[2] not in lang.unigrams:
                        # give zero prob, we assume very low likelihood of word not in test sets here
                        lang.probs[ngram] = 0.0000000001
                    else:
                        if ngram[0] in lang.unigrams:
                            lang.probs[ngram] = lang.unigrams[ngram[0]]/len(lang.unigrams)
                        if ngram[1] in lang.unigrams:
                            lang.probs[ngram] = lang.unigrams[ngram[1]]/len(lang.unigrams)
                        if ngram[2] in lang.unigrams:
                            lang.probs[ngram] = lang.unigrams[ngram[2]]/len(lang.unigrams)
                else:
                    if bigram_1 in bigrams.ngrams:
                        lang.probs[ngram] = bigrams.ngrams[bigram_1]
                    if bigram_2 in bigrams.ngrams:
                        lang.probs[ngram] = bigrams.ngrams[bigram_2]
        results.append(lang)

    return results

# give this function a tokenized excerpt, and langModels, and smoothing decscion
# smoothing_type == 1, means add_one_smoothing
def calculate_lang_prob(langModels, testGrams, smoothing_type, smoothing):
    if smoothing_type == 1:
        # this means add one smoothing
        langModels = add_one_smoothing(testGrams, langModels)
    elif smoothing_type == 2:
        # this means good turing smoothing, we use 5 and below for doubted values
        langModels = good_turing_wfreq(testGrams, langModels, 5)
    # now we can just go ahead and calculate the probability
    elif smoothing_type == 3:
        # katz back off
        langModels = katz_back_off(testGrams, langModels)
    probabilities = {}

    for lang in langModels:
        i = 0
        # print("Running ", lang.name)
        probabilities[lang.name] = 1

        for n in testGrams:
            # start of document probability
            if i == 0:
                if n[0] in lang.unigrams:
                    probabilities[lang.name] *= (lang.unigrams[n[0]]/len(lang.unigrams))

                # else:
                   # probabilities[lang.name] = 0
            if smoothing is True:
                # no need to make sure we have ngram in lang model
                probabilities[lang.name] *= lang.probs[n]
            else:
                # we should probably check to make sure it exists
                if n in lang.probs:
                    probabilities[lang.name] *= lang.probs[n]
            i += 1

    return probabilities
# get number of bigrams appearing only once, we use the equation c* = (c+1)(N{c+1}/N{c})
# For simplicity we will assume that this needs to only be done for ngram frequencies of 0
# as those are the only ones we will consider unreliable
def good_turing_smoothing(testGrams, langModels):
    results = []
    for lang in langModels:
        singleNgrams = 0
        zeroNgrams = 0

        # get count of ngrams with freq 1
        for n in lang.ngrams:
            if lang.ngrams[n] == 1:
                singleNgrams += 1

        # get count for missing ngrams in line
        for n in testGrams:
            if n not in lang.ngrams:
                zeroNgrams += 1

        for n in testGrams:
            if n not in lang.ngrams:
                lang.ngrams[n] = singleNgrams/zeroNgrams

        # normilize probabilities
        for n in lang.ngrams:
            lang.probs[n] = lang.ngrams[n]/lang.tokensCount

        # add langmodel
        results.append(lang)
    return results

# get number of bigrams appearing only once, we use the equation c* = (c+1)(N{c+1}/N{c})
# crit_freq represents those cases in which we believe the results should be doubted
# as those are the only ones we will consider unreliable
def good_turing_wfreq(testGrams, langModels, crit_freq):
    results = []

    for lang in langModels:
        for x in range(crit_freq):
            # c + 1
            x_Ngrams = 0

            # c will be the ngram sum we are looking
            c_Ngrams = 0

            # get count of ngrams with freq 1
            for n in lang.ngrams:
                if lang.ngrams[n] == x:
                    x_Ngrams += 1

            # get count for missing ngrams in line
            for n in testGrams:
                if n not in lang.ngrams:
                    c_Ngrams += 1

            for n in testGrams:
                if n not in lang.ngrams:
                    lang.ngrams[n] = x_Ngrams/c_Ngrams

            # normilize probabilities
            for n in lang.ngrams:
                lang.probs[n] = lang.ngrams[n]/lang.tokensCount

            # add langmodel
        results.append(lang)

    return results


######################################################################
# The following functions are used for language detection testing

# check_acc is a testing function, used for languageDetection testing
def check_acc(res):
    file = open('LangID.gold.txt')
    raw = file.readlines()
    # print(raw)
    correct = 0
    for i in range(1, len(raw)-1):
        lg = re.findall('[A-Z]+', raw[i])[0]
        # print(lg)
        if lg == res[i-1]:
            correct += 1

    return correct / 150

# calculate language probability for english, french, german
# line = tokenized list for language detection
# xx_unigrams = language (xx) unigram distribution
# xx_bigram_dict = language (xx) bigram probabilities
# lang_probabiity will return a list of the probabilities assoicated with each language in order.
# smoothing_type, 0 drop nout founds, 1 add one smoothing
def lang_probability(line, en_unigrams, en_bigram_dict, fr_unigrams, fr_bigram_dict, gr_unigrams, gr_bigram_dict):
        m_en = 1
        m_fr = 1
        m_gr = 1
        i = 0
        for tok in line:

            # Assumption: instead of using start of sentence, we are using the probability that
            if i == 0:
                if tok in en_unigrams:
                    m_en *= en_unigrams[tok]/sum(en_unigrams.values())
                else:
                    # Our assumption here is that if the letter does not exist
                    # in a languages training corpus, then there is a 0 probability
                    # it is that language
                    m_en = 0
                if tok in fr_unigrams:
                    m_fr *= fr_unigrams[tok]/sum(fr_unigrams.values())
                else:
                    m_fr = 0
                if tok in gr_unigrams:
                    m_gr *= gr_unigrams[tok]/sum(gr_unigrams.values())
                else:
                    m_gr = 0

            #
            if i < len(line) - 1:
                bi = (tok, line[i+1])

                if bi in en_bigram_dict:
                    m_en *= en_bigram_dict[bi]

                if bi in fr_bigram_dict:
                    m_fr *= fr_bigram_dict[bi]

                if bi in gr_bigram_dict:
                    m_gr *= gr_bigram_dict[bi]


            i += 1

        return [m_en, m_fr, m_gr]

# this function will calculate the perplexity given a results list
def calc_perplexity(results, langModels):
    perplexities = {}
    for l in langModels:
        perplexities[l.name] = 1

    for i in results:
        for k, v in i.items():
            if v != 0:
                # due to the extremely small probabilities involved in this model
                # hence we do everything log space to prevent underflow ~ Stanford and Cornell study
                perplexities[k] *= math.log10(1/v)

        # take n-root
    for lang in langModels:
        s = 0
        for n in lang.ngrams:
            s += lang.ngrams[n]

        perplexities[lang.name] = math.pow(perplexities[lang.name],  (1/s))

    return perplexities
