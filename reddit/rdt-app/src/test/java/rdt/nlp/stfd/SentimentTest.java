package rdt.nlp.stfd;

import static org.junit.Assert.*;

import java.util.Properties;

import org.junit.Before;
import org.junit.Test;

import com.mongodb.DBCursor;
import com.mongodb.DBObject;

import rdt.nlp.data.Source;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.neural.rnn.RNNCoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.util.CoreMap;

public class SentimentTest {

	Properties props;
	StanfordCoreNLP pipeline;
	Source source;
	
	@Before
	public void setUp(){
		props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit, parse, sentiment");
		pipeline = new StanfordCoreNLP(props);
		
		source = new Source("localhost", 27017, "reddit_stream_test", "big_combined");
	}
	
	@Test
	public void test() {
		
		DBCursor docs = source.find();
		docs.batchSize(1000);
		docs.limit(1000);
		int mainSentiment = 0;
		while(docs.hasNext()){
			DBObject doc = docs.next();
			int longest = 0;
			Annotation annotation = pipeline.process((String)doc.get("cleansed_text"));
			for ( CoreMap sentence : annotation.get(SentencesAnnotation.class) ){
				Tree tree = sentence.get(SentimentCoreAnnotations.AnnotatedTree.class);
				int sentiment = RNNCoreAnnotations.getPredictedClass(tree) - 2;
				String partText = sentence.toString();
				System.out.println("Part Text" + partText);
				System.out.println(
					"Part text length :" + String.valueOf(partText.length()) + "\n" +
					"sentiment :" + String.valueOf(sentiment)  + "\n"
				);
				if ( partText.length() > longest){
					mainSentiment = sentiment;
					longest = partText.length();
				}
			}
		}
		docs.close();
		
	}

}
