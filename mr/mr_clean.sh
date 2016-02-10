hadoop jar /data/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar \
-file map_clean.py -mapper map_clean.py \
-file reduce_clean.py -reducer ./reduce_clean.py \
-file rdt.mod \
-input ${1} -output ${2}