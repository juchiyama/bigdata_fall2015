import nltk
from nltk.collocations import *


if __name__ == "__main__":
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	trigram_measures = nltk.collocations.TrigramAssocMeasures()

	