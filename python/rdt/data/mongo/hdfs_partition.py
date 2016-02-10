import rdt.data.mongo.source as source, json, pymongo

def partition(conf_key="source",out_dir="."):
	"""Takes all the documents from the source and splits
	them into hdfs friendly sized files.

	:param conf_key: The nltkconf key used to indicate the collection to use.
	:type conf_key: str
	:param out_dir: The directory to put the files
	:type out_dir: str

	"""

	combined = source.Source(conf_key=conf_key)
	b = combined.find().sort("created_utc", pymongo.ASCENDING)
	b.batch_size(10000)
	buff = []
	out_dir = os.path.abspath(out_dir)
	for ind, doc in enumerate(b):
		del(doc["_id"])
		buff.append(doc)
		if ( ind + 1) % 100000 == 0:
			file_name = out_dir + "/" + buff[-1]["name"] + "_" + str(int(buff[-1]["created_utc"])) +".json"
			with open(file_name, "w") as f:
				[ f.write(json.dumps(d)) for d in buff ]
			buff = []