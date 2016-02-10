import mgdbfs.hooks as hooks
import mgdbfs.fs as fs
import json, sys, argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='MongoDB fs-like utility')
	parser.add_argument('-ls', metavar='FILE', type=str, nargs='+', help="fs utility")
	args = parser.parse_args()
	hooks.do(args)