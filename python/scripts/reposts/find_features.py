#!/usr/bin/python3.4
import nltk, sys
from nltk.collocations import *
from nltk.corpus import stopwords
from operator import itemgetter
import rdt.job as job

def main(argv):
	if(len(argv) == 0): sys.exit(1)

	sw = stopwords.words('english') + ['-','https', '%','[', ']', "''", "``",'--', "'s", ",", ".","-","(",")",":","n't", "?","!"]

	job_ = job.AnnotatedSource(host="localhost",port=27017,database="corpora",collection=sys.argv[1])

	gen = job_.to_words({}, remove_stopwords=True, limit=6000)

	finder = job_.bigram_collocation_finder(gen)

	finder.apply_word_filter(lambda w: w in sw)

	bigram_measures = nltk.collocations.BigramAssocMeasures()

	scored = finder.score_ngrams(bigram_measures.raw_freq)

	for bigram, tag in sorted(scored, key=itemgetter(1), reverse=True)[:300]:
		print(bigram)

if __name__ == '__main__': main(sys.argv[1:])