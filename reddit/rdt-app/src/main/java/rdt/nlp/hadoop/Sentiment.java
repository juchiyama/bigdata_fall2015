package rdt.nlp.hadoop;

import java.io.IOException;
import java.util.Iterator;
import java.util.Properties;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;

import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.neural.rnn.RNNCoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.util.CoreMap;

import com.cedarsoftware.util.io.JsonReader;

public class Sentiment {
	
	public static class Map extends MapReduceBase 
		implements Mapper<LongWritable, Text, Text, Text>{
		
		public final static IntWritable one = new IntWritable(1);
		private Text word = new Text();
		private Properties props = properties();
		private StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		
		public void map(LongWritable key, Text value, 
				OutputCollector<Text, Text> output, Reporter reporter) throws IOException{
			java.util.Map<String, Object> j = JsonReader.jsonToMaps(value.toString());

			String c_text = (String) j.get("cleansed_text");
			String name = (String) j.get("name");
			
			output.collect(new Text(name), new Text(String.valueOf(annotate(c_text,pipeline))));
		}		
				
	}
	
	public static class Reduce extends MapReduceBase 
		implements Reducer<Text, Text,Text, Text>{
		public void reduce(Text key, Iterator<Text> values, OutputCollector<Text, Text> output, Reporter reporter) 
				throws IOException{
			while(values.hasNext()){
				output.collect(key, values.next());
			}		
		}
	}
	
	public static int annotate(String text, StanfordCoreNLP pipeline){
        // create an empty Annotation just with the given text
		Annotation annotation = pipeline.process(text);
		int mainSentiment = 0;
		int longest = 0;
		for ( CoreMap sentence : annotation.get(SentencesAnnotation.class) ){
			Tree tree = sentence.get(SentimentCoreAnnotations.AnnotatedTree.class);
			int sentiment = RNNCoreAnnotations.getPredictedClass(tree) - 2;
			String partText = sentence.toString();
			if ( partText.length() > longest){
				mainSentiment = sentiment;
				longest = partText.length();
			}
		}
        return mainSentiment;
	}

	
	private static Properties properties(){
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit, parse, sentiment");
		return props;
	}
	
	public static void run(String[] args) throws Exception{
		JobConf conf = new JobConf(Sentiment.class);
		conf.setJobName("Sentiment");
		
		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(Text.class);
		
		conf.setMapperClass(Map.class);
		conf.setCombinerClass(Reduce.class);
		conf.setReducerClass(Reduce.class);
		
		conf.setInputFormat(TextInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);
		
		FileInputFormat.setInputPaths(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));
		
		JobClient.runJob(conf);
	}
}
