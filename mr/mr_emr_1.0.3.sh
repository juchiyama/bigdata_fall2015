# ermagherd scripts
# in the hadoop/python directory
# zip -r rdt.mod rdt
# mv rdt.mod ../mr

hadoop jar ~/contrib/streaming/hadoop-streaming-1.0.3.jar \
-file map_clean.py -mapper map_clean.py \
-file reduce_clean.py -reducer reduce_clean.py \
-file rdt.mod \
-input /in -output /clean

hadoop jar ~/contrib/streaming/hadoop-streaming-1.0.3.jar \
-file map_annotate.py -mapper map_annotate.py \
-file reduce_annotate.py -reducer reduce_annotate.py \
-file rdt.mod \
-input /clean -output /annotated

hadoop jar ~/contrib/streaming/hadoop-streaming-1.0.3.jar \
-file map_ner.py -mapper map_ner.py \
-file reduce_ner.py -reducer reduce_ner.py \
-file rdt.mod \
-input /annotated -output /ner

hadoop jar ~/contrib/streaming/hadoop-streaming-1.0.3.jar \
-file map_subreddit.py -mapper map_subreddit.py \
-file reduce_subreddit.py -reducer ./reduce_subreddit.py \
-file rdt.mod \
-input /annotated -output /subreddit

hadoop jar ~/contrib/streaming/hadoop-streaming-1.0.3.jar \
-file map_user.py -mapper map_user.py \
-file reduce_user.py -reducer reduce_user.py \
-file rdt.mod \
-input /annotated -output /user_out

mkdir /mnt/pkg
mkdir /mnt/pkg/clean
mkdir /mnt/pkg/annotated
mkdir /mnt/pkg/ner
mkdir /mnt/pkg/subreddit
mkdir /mnt/pkg/user

hadoop fs -get /clean /mnt/pkg/clean
hadoop fs -get /annotated /mnt/pkg/annotated
hadoop fs -get /ner /mnt/pkg/ner
hadoop fs -get /subreddit /mnt/pkg/subreddit
hadoop fs -get /user_out /mnt/pkg/user

tar -zcvf /mnt/rdt_data.tgz /mnt/pkg
