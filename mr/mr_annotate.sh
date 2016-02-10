hadoop jar /data/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar \
-file map_annotate.py -mapper map_annotate.py \
-file reduce_annotate.py -reducer reduce_annotate.py \
-file rdt.mod \
-input ${1} -output ${2}
