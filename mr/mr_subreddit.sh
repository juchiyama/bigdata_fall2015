hadoop jar /data/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar \
-file map_subreddit.py -mapper map_subreddit.py \
-file reduce_subreddit.py -reducer ./reduce_subreddit.py \
-file rdt.mod \
-input ${1} -output ${2}