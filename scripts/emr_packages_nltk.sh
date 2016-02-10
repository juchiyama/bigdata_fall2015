sudo apt-get update
sudo apt-get install -q -y python-lxml
sudo apt-get install -q -y python-pip 
sudo pip install nltk
sudo pip install pymongo
hadoop fs -get s3://uchiyamadeps/nltk_data.tgz ./
mkdir -p /usr/share/nltk_data
mv nltk_data.tgz /usr/share/nltk_data
tar -zxf /usr/share/nltk_data/nltk_data.tgz

