from rdt.data.mongo.features import Features
import rdt.job as job, nltk, sys
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

if __name__ == "__main__":
	subreddit = sys.argv[1]
	stopwords = stopwords.words('english') + ['-','https', '%','[', ']', "''", "``",'--', "'s", ",", ".","-","(",")",":","n't", "?","!"]
	ft_db=Features(host="localhost",port=27017,database="reddit_stream",collection="features")
	job = job.AnnotatedSource(host="localhost",port=27017,database="reddit_stream",collection="big_combined")
	gen = job.to_words({"subreddit" : subreddit}, remove_stopwords=True, limit=6000)
	finder = job.bigram_collocation_finder(gen)
	finder.apply_freq_filter(7)
	finder.apply_word_filter(lambda w: w in stopwords)
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	scored = finder.score_ngrams(bigram_measures.raw_freq)
	ft_db.upsert({"subreddit" : subreddit}, {"bigrams" : sorted(finder.ngram_fd.items(), key=lambda t:(-t[1], t[0])) })
	# print(sorted(finder.ngram_fd.items(), key=lambda t:(-t[1], t[0]))[:10])
	# print(len(finder.ngram_fd.items()))