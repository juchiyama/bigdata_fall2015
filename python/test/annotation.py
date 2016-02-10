import unittest, re, string, nltk, json, rdt.mr.annotation as annotation

class AnnotationTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
	def tearDown(self):	
		pass

	def test_no_bad_characters(self):
		lines = []
		a = re.compile('\.|\$')
		b = re.compile('^\W$')
		with open("data/test_key.json") as f:
			for line in f:
				line.rsplit('\n')
				line = line.split("\t")
				key, value = line[0], json.loads("".join(line[1:]))
				value["author"] = key
				no_nonwords = annotation.filter_nouns(value["nouns"].keys())
				print(list(value["nouns"].keys()))
				print(list(no_nonwords))
				[self.t(a.search(w) is None) for w in no_nonwords]

def main():
	suite = lambda x : unittest.TestLoader().loadTestsFromTestCase(x)
	runner = lambda x : unittest.TextTestRunner(verbosity=2).run(x)
	run = lambda x : runner(suite(x))
	return run(AnnotationTestCase)