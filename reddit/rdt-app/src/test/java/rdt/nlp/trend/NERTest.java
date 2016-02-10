package rdt.nlp.trend;

import static org.junit.Assert.*;

import java.util.List;
import java.util.Properties;

import org.junit.Before;
import org.junit.Test;

import com.mongodb.Cursor;
import com.mongodb.DBObject;

import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;
import rdt.nlp.data.FieldComprehension;
import rdt.nlp.data.Source;

public class NERTest {
	
	Source source;
	Properties props;
	StanfordCoreNLP pipeline;
	
	@Before
	public void setUp(){
		source = new Source("localhost",27017,"reddit_stream","combined", 10_000);
		props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
        
        pipeline = new StanfordCoreNLP(props);
	} 
	
	@Test
	public void test() {
		Double high = source.getMostRecentCreatedUTC();
		Double low = high - 10_000.0;
		Cursor docs = source.getDocumentsBetween(low, high);
		try{
			while(docs.hasNext()){
				DBObject doc = docs.next();
				System.out.println(doc.get("name"));
				String text = FieldComprehension.bodyOrSelftext(doc);
				System.out.println(text);
				System.out.print(text.length());
				if (text == ""){
					continue;
				}
				Annotation document = new Annotation(text);
				pipeline.annotate(document);
				List<CoreMap> sentences = document.get(SentencesAnnotation.class);
				for(CoreMap sentence: sentences){
					for(CoreLabel token: sentence.get(TokensAnnotation.class)){
						String word = token.get(TextAnnotation.class);
						String pos = token.get(PartOfSpeechAnnotation.class);
						String ne = token.get(NamedEntityTagAnnotation.class);
						System.out.print("(" + word + ", "  + pos + ", " + ne + ")");
					}
					System.out.println();
				}
				
			}
		} finally {
			docs.close();
		}
				
	}

}
