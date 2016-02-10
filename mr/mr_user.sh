hadoop jar /data/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar \
-file map_user.py -mapper map_user.py \
-file reduce_user.py -reducer reduce_user.py \
-file rdt.mod \
-input ${1} -output ${2}