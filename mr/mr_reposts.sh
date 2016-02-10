hadoop jar /home/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar \
-file reposts.mod \
-file ~/is_repost.json \
-file ~/is_not_repost.json \
-file map_reposts.py -mapper map_reposts.py \
-file reduce_reposts.py -reducer reduce_reposts.py \
-input ${1} -output ${2}