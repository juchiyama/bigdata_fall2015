hadoop fs -rmr /user/john/ner
hadoop jar ~/hadoop-1.2.1/contrib/streaming/hadoop-streaming-1.2.1.jar \
-file map_ner.py -mapper map_ner.py \
-file reduce_ner.py -reducer reduce_ner.py \
-file rdt.mod \
-input /user/john/small_sample.json -output /user/john/ner

hadoop fs -ls /user/john/ner
hadoop fs -cat /user/john/ner/part-00000
