import rdt.data.clean.html as clean_html
import sys, json

if __name__ == "__main__":
	for line in sys.stdin:
		line = line.rstrip('\n')
		print((json.dumps(clean_html.clean_json(line))))