hadoop jar /home/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar \
-file map_completeness.py -mapper map_completeness.py \
-file reduce_completeness.py -reducer reduce_completeness.py \
-input ${1} -output ${2}