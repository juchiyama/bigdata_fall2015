hadoop jar /data/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar \
-file map_ner.py -mapper map_ner.py \
-file reduce_ner.py -reducer reduce_ner.py \
-file rdt.mod \
-input ${1} -output ${2}
