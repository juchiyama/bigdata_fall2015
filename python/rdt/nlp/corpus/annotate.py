from nltk.classify import PositiveNaiveBayesClassifier

class CorpusAnnotater(object):

	def __init__(self,*args, **kwargs):
		if_def = lambda x: kwargs[x] if x in kwargs else None
		for attr in ["corpora_iter","corpora","train_set","test_set","feature"]:
			setattr(self,attr,if_def(attr))
		self.tool_chain = kwargs.get("tool_chain", lambda x : x)

	def classify(self,doc):
		return self.classifier.classify(self.feature(doc))

	def classify_iter(self,iterr):
		for anno in iterr:
			yield (anno, self.classify(anno))

class PNBAnnotater(CorpusAnnotater):

	def __init__(self,*args,**kwargs):
		super(PNBAnnotater, self).__init__(*args,**kwargs)
		if_def = lambda x: kwargs[x] if x in kwargs else None
		for attr in ["labeled_set","unlabeled_set","annotater","co"]:
			setattr(self,attr,if_def(attr))

	def train(self):
		label = lambda x : list(map(self.feature,x))
		self.classifier = PositiveNaiveBayesClassifier.train(label(self.labeled_set()),label(self.unlabeled_set()))

	def describe(self):
		self.classifier.show_most_informative_features();

	def __exit__(self):
		self.exit(self)

class NBClassifier(CorpusAnnotater):
	def __init__(self,*args,**kwargs):
		super(NBClassifier,self).__init__(*args,**kwargs)

	def train(self,train_set):
		self.classifier = nltk.NaiveBayesClassifier(train_set)
