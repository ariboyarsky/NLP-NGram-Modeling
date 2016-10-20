# NLP-NGram-Modeling
Ari Boyarsky
ariboyarsky@gwu.edu

This repo holds an example of NGram modeling for language detection. 

## Files
__init__.py: An empty file used by Pycharm to identify the project
HW2english: The English training corpus

HW2french: The french training corpus

HW2german: The german training corpus

LangID.gold: the file that holds the correct test set charecterization

LangID.test: the testing corpus

letterLangID.py: Runs a general language model with probabilities calculated by n/N

BigramWordLangId-AO.py: Runs an add one smoothing model of n/(U+N)

BigramWordLangId-GT.py: Runs a good turing smoothing model calculated by c* = (c+1)(N{c+1}/N{c})

TrigramWordLangId-KBO.py: Runs a Katz-Back-Off model on word trigrams, see https://www.cs.cmu.edu/~roni/papers/scalable-TR-96-139.pdf

TrigramWordLangId-KBO.out contains the results for q5

NGramLangModel.py: this file has code that is used by all other py files to run. This maintains most of the code preforms the ngram modeling and analysis. Please note that there are many unused methods in this file that were used for testing. These were included so that one could see the process of generlization, for example moving from creating just bigrams to creating ngrams of a given n in a single method. The best way to examine only the working functions is to first look at files such as letterLangId.py and see what is called. However here is a list of active functions:
	Class NGram
	word_tokenize
	letter_tokenize
	ngram_dict
	calc_NGram_class
	add_one_smoothing
	katz_back_off
	calculate_lang_prob
	good_turing_wfreq
	calc_perplexity
	check_acc
	



## System
This assignment was completed on a Windows 10 machine. I used the JetBrains Pycharm IDE. Specifcally, NGramLangModel.py is used as a library that contains the methods that do much of the work in solving this problem. This file imported into each of the solution files. There are no special features or limitations to note.

## How to Run
To run simply run each of the assignement files using the python command in terminal. Furthermore, one may open the files in IDLE (included with Python 3) and run using this system.

## References
https://docs.google.com/viewer?a=v&pid=sites&srcid=ZGVmYXVsdGRvbWFpbnxnd2NzY2kzOTA3NjkwN2ZhbGwxNnxneDozMWY1MzcxZWJhYzFiYzA
https://web.stanford.edu/class/cs124/lec/languagemodeling.pdf
http://nlp.stanford.edu/~wcmac/papers/20050421-smoothing-tutorial.pdf
http://www.cs.cornell.edu/courses/cs474/2005fa/Handouts/n-grams+smoothing.pdf
https://www.cs.cmu.edu/~roni/papers/scalable-TR-96-139.pdf
