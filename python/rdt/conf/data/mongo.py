import json, os

def get_conf(conf="/home/john/nltkconf.json"):
	with open(conf) as json_file:
		return json.load(json_file)
