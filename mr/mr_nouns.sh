hadoop jar /data/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar \
-file map_nouns.py -mapper map_nouns.py \
-file reduce_nouns.py -reducer reduce_nouns.py \
-file rdt.mod \
-input ${1} -output ${2}