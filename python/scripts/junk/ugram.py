import nltk, rdt.nlp.pos as pos
from nltk.corpus import conll2000

class UnigramChunker(nltk.ChunkParserI):
	def __init__(self, train_sents):
		train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
					  for sent in train_sents]
		self.tagger = nltk.UnigramTagger(train_data)

	def parse(self, sentence):
		pos_tags = [pos for (word,pos) in sentence]
		tagged_pos_tags = self.tagger.tag(pos_tags)
		chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
		conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
					 in zip(sentence, chunktags)]
		return nltk.chunk.conlltags2tree(conlltags)

if __name__ == "__main__":
	test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
	train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
	# print(train_sents)
	unigram_chunker = UnigramChunker(train_sents)
	print(unigram_chunker.evaluate(test_sents))
	d = [ unigram_chunker.parse(sent) for sent in pos.preprocess("The dog went to the park.")]
	print(d)
	# print(unigram_chunker.parse(pos.preprocess("The dog went to the park.")))