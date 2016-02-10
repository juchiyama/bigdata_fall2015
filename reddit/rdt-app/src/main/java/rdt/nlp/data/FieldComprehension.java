package rdt.nlp.data;

import com.mongodb.Cursor;
import com.mongodb.DBObject;

import java.util.Arrays;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Pattern;
import java.io.IOException;

public class FieldComprehension {
	/**
	 * Everything here is static. These are essentially
	 * functions for commonly used patterns. The CloseableIterators
	 * and the AnnotatedDocumentIterators wrap aggregation options
	 * found in rdt.nlp.AnnotatedQueryBuilder. These need to be moved.
	 * Should put them in rdt.nlp as a factory like creation.
	 * 
	 */
	private static final Pattern comment = Pattern.compile("^t1_");
	private static final Pattern submission = Pattern.compile("^t3_");
	public static final String[] commentFields = { 
		"body", "body_html", "ups", "downs", "created", "created_utc", "distinguished",
        "num_reports", "likes", "id", "gilded", "parent_id",
        "approved_by", "edited", "fullname", "name", "permalink", "is_root"
	};
	public static Set<String> getCommentFieldsSet(){
		return new HashSet<String>(Arrays.asList(commentFields));
	}
	public static final String[] submissionFields =	{
		"author","id","likes","name","num_comments","num_reports","permalink",
	      "subreddit","subreddit_id","title","ups","downs","url","short_link","created",
	      "created_utc","score","over_18","gilded","selftext","selftext_html","domain","is_self"
	};
	public static Set<String> getSubmissionFieldSet(){
		return new HashSet<String>(Arrays.asList(submissionFields));
	}
	public static final String[] authorFields = {
		"author"
	};
	public static final String[] subredditFields = {
		"subreddit", "subreddit_id"
	};
	
	public static boolean isComment(String name){
		return comment.matcher(name).find();
	}
	
	public static boolean isComment(DBObject doc){
		return isComment((String) doc.get("name"));
	}
	
	public static boolean parentIsComment(DBObject doc){
		return isComment((String)doc.get("parent_id"));
	}
	
	public static boolean parentIsSubmission(DBObject doc){
		return isSubmission((String) doc.get("parent_id"));
	}
	
	public static boolean isSubmission(String name){
		return submission.matcher(name).find();
	}
	
	public static boolean isSubmission(DBObject doc){
		return isSubmission(new String((String) doc.get("name")));
	}
	
	public static Date dateFromTimestamp(Double timestamp){
		return new Date(timestamp.longValue()*1000);
	}
	
	public static String bodyOrSelftext(DBObject doc){
		if (doc.containsField("selftext")){
			return (String) doc.get("selftext");
		} else if (doc.containsField("body")){
			return (String)doc.get("body");
		} else {
			return ""; 
		}
	}
	
	/**
	 * Ensures that annotated and raw document sources return jus the raw document.
	 * 
	 * @param sbms
	 * @return
	 */
	
	public static CloseableIterator<DBObject> submissionIterator(final Cursor sbms){
		CloseableIterator<DBObject> it = new CloseableIterator<DBObject>(){
			
			@Override
			public boolean hasNext(){
				return sbms.hasNext();
			}
			
			@Override
			public DBObject next(){
				DBObject sbm = sbms.next();
				if ( sbm.containsField("event")){
					return (DBObject) sbm.get("event");
				}
				return sbm;
			}
			
			@Override
			public void remove(){
				sbms.remove();
			}
			
			@Override
			public void close() throws IOException{
				sbms.close();
			}
		};
		return it;
	}
	
	/**
	 * Transforms fields in the aggregated Cursor. The author field originally
	 * comes in as the "_id" field. This is changed to "author" for simplicities sake.
	 * 
	 * @param authors	MongoDB Cursor
	 * @return			An iterator that acts just like a cursor.
	 */
	
	public static CloseableIterator<DBObject> authorIterator(final Cursor authors){
		CloseableIterator<DBObject> it = new CloseableIterator<DBObject>(){
			
			@Override
			public boolean hasNext(){
				return authors.hasNext();
			}
			
			@Override
			public DBObject next(){
				DBObject temp = authors.next();
				temp.put("author", temp.get("_id"));
				temp.removeField("_id");
				return temp;
			}
			
			@Override
			public void remove(){
				authors.remove();
			}
			
			@Override
			public void close() throws IOException{
				authors.close();
			}
		};
		return it;
	}
	
	/**
	 * The aggregation cursor returns ugly fields. This wrapper
	 * adjusts the fields for ease of implementation.
	 * 
	 * @param subreddits
	 * @return				CloseableIterator that works just like a Cursor.
	 */
	
	public static CloseableIterator<DBObject> subredditIterator(final Cursor subreddits){
		CloseableIterator<DBObject> it = new CloseableIterator<DBObject>(){
			
			@Override
			public boolean hasNext(){
				return subreddits.hasNext();
			}
			
			@Override
			public DBObject next(){
				DBObject temp = subreddits.next();
				temp.put("subreddit", ((List)temp.get("subreddit")).get(0));
				temp.put("subreddit_id", temp.get("_id"));
				temp.removeField("_id");
				return temp;
			}
			
			@Override
			public void remove(){
				subreddits.remove();
			}
			
			@Override
			public void close() throws IOException{
				subreddits.close();
			}
		};
		return it;
	}
	
}
