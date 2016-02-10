# HOW-TO

Installing things on the EMR cluster requires using a bootstrap script.
There are two versions that do roughly the same thing.
They are: emr_packages_nltk.sh and emr_packages.sh . 
The first downloads the nltk language models from s3 and the second downloads the nltk
language models from the internet.
The emr_packages_nltk.sh is significantly faster than emr_packages.sh, but it requires that the user download the data first and then upload it to s3.

	$ mkdir nltk_data
	$ python -m nltk.downloader -d ./nltk_data all
	$ tar -zcvf nltk_data.tgz

Then either through s3 command line or the web user interface, upload the data to s3.

	$ hadoop fs -put nltk_data.tgz s3://<bucket_name>/some/dir

Look in the hadoop/mr directory. 
That is where all of the python scripts are that run hadoop.
An example job is as follows:
	
	$ cd hadoop/python
	$ zip -r rdt.mod rdt
	$ mv rdt.mod ../mr
	$ hadoop fs -put small_sample.json /in
	$ ./mr_clean.py /in /clean

That is the pattern that all of the scripts use. If you read the mr_*.py scripts
if shows the parameters necessary to run each mapreduce job.
The rdt.mod contains the rdt-python module.
This module is necessary to run anything using nltk and the custom module..: