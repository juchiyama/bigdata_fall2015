hadoop jar /data/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar \
-file map_day.py -mapper map_day.py \
-file reduce_day.py -reducer reduce_day.py \
-file rdt.mod \
-input ${1} -output ${2}
