package rdt.nlp.app;


import java.util.List;
import java.util.Map;
import java.util.Properties;

import org.junit.Test;

import com.mongodb.BasicDBObject;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;

import rdt.nlp.data.Source;
import edu.stanford.nlp.dcoref.CorefChain;
import edu.stanford.nlp.dcoref.CorefCoreAnnotations.CorefChainAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations.TreeAnnotation;
import edu.stanford.nlp.util.CoreMap;

public class POSMongo {
	/**
	 * This test is being used to measure the speed of the CoreNLP package.
	 * 
	 * 
	 */
	@Test
	public void test() {
		Properties props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner");
        
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
        
        Source source = new Source("localhost",27017,"reddit_stream_test","big_combined");
        // Source output = new Source("localhost", 27017, "reddit_stream_test", "annotated");
       
        BasicDBObject filt = new BasicDBObject("cleansed_text", new BasicDBObject("$ne", ""));
        DBCursor cursor = source.find(filt);
        cursor.limit(100000);
        try{
            while(cursor.hasNext()){
            	DBObject doc = cursor.next();
            	describe(doc,pipeline);
            }
        } finally {
        	cursor.close();
        }
        // read some text in the text variable
	}
	
	public static void describe(DBObject doc,StanfordCoreNLP pipeline){
        // create an empty Annotation just with the given text
        Annotation document = new Annotation((String)doc.get("cleansed_text"));
        BasicDBObject m_doc = new BasicDBObject();
        // run all Annotators on this text
        pipeline.annotate(document);
        
        // these are all the sentences in this document
        // a CoreMap is essentially a Map that uses class objects as keys and has values with custom types
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);
        
        for(CoreMap sentence: sentences) {
          // traversing the words in the current sentence
          // a CoreLabel is a CoreMap with additional token-specific methods
          for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
            // this is the text of the token
            String word = token.get(TextAnnotation.class);
            
            // this is the POS tag of the token
            String pos = token.get(PartOfSpeechAnnotation.class);
            
            // this is the NER label of the token
            String ne = token.get(NamedEntityTagAnnotation.class);
           // System.out.print("(" + word + ", " + pos + ", " + ne + ")");
          }
          // System.out.println();

          // this is the parse tree of the current sentence
          Tree tree = sentence.get(TreeAnnotation.class);

          // this is the Stanford dependency graph of the current sentence
          SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);
        }

        // This is the coreference link graph
        // Each chain stores a set of mentions that link to each other,
        // along with a method for getting the most representative mention
        // Both sentence and token offsets start at 1!
        Map<Integer, CorefChain> graph = 
          document.get(CorefChainAnnotation.class);
	}

}
