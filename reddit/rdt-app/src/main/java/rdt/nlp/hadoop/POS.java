package rdt.nlp.hadoop;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Properties;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;

import edu.stanford.nlp.ie.AbstractSequenceClassifier;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;

import com.cedarsoftware.util.io.JsonReader;
import com.mongodb.util.JSON;

public class POS extends Configured implements Tool{

	public static class Map extends MapReduceBase 
		implements Mapper<LongWritable, Text, Text, Text>{
		
		public final static IntWritable one = new IntWritable(1);
		private Properties props = properties();
		private StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		
		public void map(LongWritable key, Text value, OutputCollector<Text,
				Text> output, Reporter reporter) throws IOException {
	        java.util.Map<String, Object> j = JsonReader.jsonToMaps(value.toString());
	        
	        // read some text in the text variable
			String c_text= (String) j.get("cleansed_text");
			String name = (String) j.get("name");
			output.collect(new Text(name), new Text(JSON.serialize(annotate(c_text,pipeline))));
		}
	}
	
	private static Properties properties(){
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner");
		return props;
	}
	
	public static List<List<String[]>> annotate(String text, StanfordCoreNLP pipeline){
        // create an empty Annotation just with the given text
		if ( text == null || text == "" ){
			return new ArrayList<>();
		}
        Annotation document = new Annotation(text);
        
        // run all Annotators on this text
        pipeline.annotate(document);
        
        // these are all the sentences in this document
        // a CoreMap is essentially a Map that uses class objects as keys and has values with custom types
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);
        // String all_str = "";
        List<List<String[]>> all_str = new ArrayList<>();
        for(CoreMap sentence: sentences) {
          // traversing the words in the current sentence
          // a CoreLabel is a CoreMap with additional token-specific methods
      	  List<String[]> sent = new ArrayList<>();
          for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
            // this is the text of the token
            String word = token.get(TextAnnotation.class);
            
            // this is the POS tag of the token
            String pos = token.get(PartOfSpeechAnnotation.class);
            
            // this is the NER label of the token
            String ne = token.get(NamedEntityTagAnnotation.class);
            String[] w = {word, pos, ne};
            sent.add(w);
          }
          all_str.add(sent);
        }
        return all_str;
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
	public static void main(String[] args) throws Exception{
		Configuration confc = new Configuration();
		int res = ToolRunner.run(confc, new rdt.nlp.hadoop.POS(), args);
		System.exit(res);
	}

	@Override
	public int run(String[] args) throws Exception {
		// TODO Auto-generated method stub
		JobConf conf = new JobConf(POS.class);
		conf.setJobName("POS");
		
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
		return 0;
	}
	
}