import sys, importlib

if __name__ == '__main__':
	# looks for stuff in the test/* file, file name matches STDIN
	get = lambda x : importlib.import_module("test." + x)
	if len(sys.argv) == 1:
		t_mod = get(input("test_name: ").rstrip("\n"))
		t_mod.main()
	else:
		t_mod = get(sys.argv[1].rstrip("\n"))
		t_mod.main()