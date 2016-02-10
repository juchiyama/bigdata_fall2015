Configuration
*************

Environment
===========

The $NLTKCONF environment variable should point
to where ever the mongodb and other global
variables are stored. Use "source" whenever you
see a conf_key parameter.

nltkconf.json::

	{   "source" : {    "host" : "localhost",
	                    "port" : 27017,
	                    "database" : "reddit_stream",
	                    "collection" : "combined"
	                }
	}

Dependencies
============

* nltk
* numpy
* matplotlib
* pymongo