package rdt.nlp.stfd;

import static org.junit.Assert.*;

import java.io.IOException;
import java.util.List;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import edu.stanford.nlp.ie.AbstractSequenceClassifier;
import edu.stanford.nlp.ie.crf.CRFClassifier;
import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;

public class NERTest {

	@Before
	public void setUp() throws Exception {
	}

	@After
	public void tearDown() throws Exception {
	}

	@Test
	public void test() {
		String[] args = {};
		String serializedClassifier = "/home/john/stfd_nlp/stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.crf.ser.gz";
		
	    /*if (args.length > 0) {
	      serializedClassifier = args[0];
	    }*/
		

	    AbstractSequenceClassifier<CoreLabel> classifier = null;
		try {
			classifier = CRFClassifier.getClassifier(serializedClassifier);
			
		} catch (ClassCastException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		assertTrue(classifier != null);
		

	    /* For either a file to annotate or for the hardcoded text example,
	       this demo file shows two ways to process the output, for teaching
	       purposes.  For the file, it shows both how to run NER on a String
	       and how to run it on a whole file.  For the hard-coded String,
	       it shows how to run it on a single sentence, and how to do this
	       and produce an inline XML output format.
	    */
	    if (args.length > 1) {
	      String fileContents = null;
		try {
			fileContents = IOUtils.slurpFile("/home/john/sample.txt");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	      List<List<CoreLabel>> out = classifier.classify(fileContents);
	      for (List<CoreLabel> sentence : out) {
	        for (CoreLabel word : sentence) {
	          System.out.print(word.word() + '/' + word.get(CoreAnnotations.AnswerAnnotation.class) + ' ');
	        }
	        System.out.println();
	      }
	      System.out.println("---");
	      out = classifier.classifyFile(args[1]);
	      for (List<CoreLabel> sentence : out) {
	        for (CoreLabel word : sentence) {
	          System.out.print(word.word() + '/' + word.get(CoreAnnotations.AnswerAnnotation.class) + ' ');
	        }
	        System.out.println();
	      }

	    } else {
	      String[] example = {"Good afternoon Rajat Raina, how are you today?",
	                          "I go to school at Stanford University, which is located in California." };
	      for (String str : example) {
	        System.out.println(classifier.classifyToString(str));
	      }
	      System.out.println("---");

	      for (String str : example) {
	        // This one puts in spaces and newlines between tokens, so just print not println.
	        System.out.print(classifier.classifyToString(str, "slashTags", false));
	      }
	      System.out.println("---");

	      for (String str : example) {
	        System.out.println(classifier.classifyWithInlineXML(str));
	      }
	      System.out.println("---");

	      for (String str : example) {
	        System.out.println(classifier.classifyToString(str, "xml", true));
	      }
	      System.out.println("---");

	      int i=0;
	      for (String str : example) {
	        for (List<CoreLabel> lcl : classifier.classify(str)) {
	          for (CoreLabel cl : lcl) {
	            System.out.print(i++ + ": ");
	            System.out.println(cl.toShorterString());
	          }
	        }
	      }
	    }

	}

}
