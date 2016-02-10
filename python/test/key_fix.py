import unittest, re, string, nltk, json, rdt.mr.annotation as annotation

class KeyFixTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
	def tearDown(self):	
		pass

	def test_keyfix_characters(self):
		lines = []
		a = re.compile('\.|\$')
		b = re.compile('^\W$')
		with open("data/test_key.json") as f:
			for line in f:
				line = line.split('\t')
				name, data = line[0], json.loads("".join(line[1:]))
				print(name, data)
				data["nouns"] = annotation.no_none(annotation.filter_keys(annotation.fix_keys(data["nouns"])))
				print(name, data)
				print("-"*50)

def main():
	suite = lambda x : unittest.TestLoader().loadTestsFromTestCase(x)
	runner = lambda x : unittest.TextTestRunner(verbosity=2).run(x)
	run = lambda x : runner(suite(x))
	return run(KeyFixTestCase)