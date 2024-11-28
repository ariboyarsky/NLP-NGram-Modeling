__author__ = 'ariboyarsky'
# word trigram model
# By Ari Boyarsky

# Imports
import math
from NGramLangModel import *

###############################################
# Training Sets
# English
# import training data
file = open('HW2english.txt', mode="r", encoding="MacRoman")
raw = file.read()

# Tokenize english raw
tokens = word_tokenize(raw)
# get unigram, bigram dist for english
en_model = calc_NGram_class(3, tokens, "EN")

###############################################
# French

file = open('HW2french.txt', mode="r", encoding="MacRoman")
raw = file.read()

# Tokenize french raw
tokens = word_tokenize(raw)
# get unigram, bigram dist for french
fr_model = calc_NGram_class(3, tokens, "FR")

###############################################
# German
file = open('HW2german.txt', mode="r", encoding="MacRoman")
raw = file.read()

# Tokenize german raw
tokens = word_tokenize(raw)
# get unigram, bigram dist for french

gr_model = calc_NGram_class(3, tokens, "GR")

###############################################
# testing
langModels = [en_model, fr_model, gr_model]


file = open('LangID.test.txt', mode="r", encoding="MacRoman")
sents = file.readlines()

# tokenize training data by char
cleaned = []
tokenized = []

probs = []

count = 0
for line in sents:
    words = word_tokenize(line)
    lang_probability = calculate_lang_prob(langModels, ngram_dict(3, words), 3, True)
    probs.append(lang_probability)

# get language
results = []
for i in range(len(probs)):
    # get max and index
    # 0->en, 1->fr, 2->
    print(i+1, ": ", max(probs[i], key=probs[i].get))
    results.append(max(probs[i], key=probs[i].get))

acc = check_acc(results)
print("Percent Correct: ", acc * 100)

perplexities = calc_perplexity(probs, langModels)

for p in perplexities:
    print("Perplexities ", p, " : ", perplexities[p], "\n")

f = open('TrigramWordLangId-KBO.out', 'w')
for i in range(len(results)):
    f.write("%s: %s\n" % (i+1, results[i]))

f.write('\n Percent Correct: %s' % int(acc*100))

for p in perplexities:
    f.write("Perplexities %s: %s" % (p, perplexities[p]))

f.close()
