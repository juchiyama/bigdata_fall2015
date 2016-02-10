from nltk.corpus import conll2000
import nltk, rdt.nlp.pos as pos

"""taken directly from NLTK textbook"""
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

class BigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.BigramTagger(train_data)

    def parse(self, sentence):
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)


def conll2000_np_test():
	return conll2000.chunk_sents("test.txt", chunktypes=["NP"])

def conll2000_np_train():
	return conll2000.chunk_sents("train.txt", chunktypes=["NP"])

def simple_np_ugram(documents):
	ugram = UnigramChunker(conll2000.chunked_sents('train.txt'))

	"""String sentences get split up into a datastructure"""
	for doc in documents:
		buf = []
		for sent in pos.preprocess(doc):
			buf.append(ugram.parse(sent))
		yield buf

def simple_np_bgram(documents):
	bgram = BigramChunker(conll2000.chunked_sents('train.txt'))
	for doc in documents:
		buf = []
		for sent in pos.preprocess(doc):
			buf.append(bgram.parse(sent))
		yield buf