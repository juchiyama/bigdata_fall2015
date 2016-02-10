package rdt.nlp.data;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.List;

import com.mongodb.AggregationOptions;
import com.mongodb.BasicDBObject;
import com.mongodb.Cursor;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;

/**
 * @author John Uchiyama
 *
 */
public class AnnotatedSource extends RedditCollection{

	int batchSize = 1000;
	protected DBObject projectSbr;
	protected DBObject projectAth;
	/**
	 * Extends RDTCollection, which is a wrapper for a MongoDB driver.
	 * It adds domain specific operations. The aggregation
	 * operations output ugly-formed DBObjects. 
	 * See rdt.data.FieldComprehension for the 
	 * wrappers of these MongoDB Cursor outputs.
	 * 
	 * This class also provides the main interface to iterating annotated documents.
	 * 
	 * @param host 			MongoDB hostname
	 * @param port 			MongoDB port
	 * @param database 		MongoDB database name
	 * @param collection 	MongoDB collection name
	 */
	public AnnotatedSource(String host, int port, String database, String collection){
		super(host,port,database,collection);
		BasicDBObject onlySubreddit = 
				new BasicDBObject("_id","$event.subreddit_id");
		onlySubreddit.append("subreddit", 
				new BasicDBObject("$addToSet", "$event.subreddit"));
		projectSbr = new BasicDBObject("$group", onlySubreddit);
		projectAth = new BasicDBObject(
				"$group", new BasicDBObject("_id", "$event.author"));
	}
	
	/**
	 * Returns a MongoDB cursor with a unique set of authors. The authors
	 * are encoded in the DBObject MongoDB format. The DBObjects work
	 * much like json. 
	 * 
	 * 
	 * @param nouns List of nouns to match annotated documents
	 * @param low 	Minimum created_utc value to find ( gte in seconds ) 
	 * @param high	Maximum created_utc value to find ( lt in seconds )
	 * @return		MongoDB Cursor which can be used or wrapped in an iterator
	 * @serdt.data.ata.FieldComprehension
	 */
	
	public Cursor getAuthorsForNouns(Collection<String> nouns,
			Double low, Double high){
		ArrayList<DBObject> aggParams = new ArrayList<>();
		aggParams.add(AggregationMatch.matchBetweenUTCWithNouns(low, high, nouns));
		BasicDBObject projectAth 
			= new BasicDBObject("$group", 
					new BasicDBObject("_id", "$event.author"));
		aggParams.add(projectAth);
		return aggregate(aggParams);
	}
	
	/**
	 * This method wraps getAuthorsForNouns by setting the low bound to 
	 * zero. 
	 * 
	 * @param nouns 
	 * @param high
	 * @return
	 */
	public Cursor getAuthorsForNounsBefore(Collection<String> nouns, Double high){
		return getAuthorsForNouns(nouns,0.0,high);
	}
	
	/**
	 * This method returns a MongoDB cursor for annotated comment
	 * documents that include at least one noun from the nouns Collection.
	 * 
	 * @param nouns List of nouns searched for.
	 * @param low Low created_utc number ( gte in seconds ).
	 * @param high High created_utc number ( lt in seconds )
	 * @return MongoDB cursor
	 */
	
	public Cursor getCommentsForNouns(Collection<String> nouns,Double low, Double high){
		BasicDBObject onlyComments = AggregationMatch.betweenUTCWithNouns(low,high,nouns); 
		onlyComments.append("event.body",	new BasicDBObject("$exists", true));		
		DBCursor cursor = find(onlyComments);
		cursor.batchSize(batchSize);
		cursor.sort(new BasicDBObject("event.created_utc", 1));
		return cursor;
	}
	
	/**
	 * This method wraps getCommentsForNouns by setting the low bound
	 * to zero.
	 * 
	 * @param nouns
	 * @param high
	 * @return
	 */
	
	public Cursor getCommentsForNounsBefore(Collection<String> nouns, Double high){
		return getCommentsForNouns(nouns,0.0,high);
	}
	
	/**
	 * This method returns a MongoDB cursor for the submissions
	 * that contain a noun in given Collection.
	 * 
	 * @param nouns A collection of nouns.
	 * @param low Low created_utc number ( gte in seconds )
	 * @param high High created_utc number ( lt in seconds )
	 * @return MongoDB cursor
	 */
	
	public Cursor getSubmissionsForNouns(Collection<String> nouns, Double low, Double high){
		BasicDBObject derp = AggregationMatch.betweenUTCWithNouns(low, high, nouns);
		derp.append("event.selftext", new BasicDBObject("$exists", true));
		DBCursor cursor = find(derp);
		cursor.batchSize(batchSize);
		cursor.sort(new BasicDBObject("event.created_utc", 1));
		return cursor;
	}
	
	/**
	 * A wrapper for the getSubmissionsForNouns method. It sets the low bound 
	 * to zero.
	 * 
	 * @param nouns
	 * @param high
	 * @return
	 */
	
	public Cursor getSubmissionsForNounsBefore(Collection<String> nouns, Double high){
		return getSubmissionsForNouns(nouns,0.0,high);
	}
	
	/**
	 * Calls the MongoDB aggregate method with the given aggregation options.
	 * Additional arguments are specified in aggOpps. This method 
	 * standardizes the way the Cursor is created and returned.
	 * 
	 * @param params
	 * @return
	 */
	
	private Cursor aggregate(List<DBObject> params){
		return getCollection().aggregate(params, aggOpps());
	}
	
	/**
	 * This method works some standard options for the aggregation options.
	 * 
	 * @return
	 */
	
	private AggregationOptions aggOpps(){
		return AggregationOptions.builder()
				.batchSize(batchSize)
				.outputMode(AggregationOptions.OutputMode.CURSOR)
				.build();
	}
	
	/**
	 * Finds the annotated document with the largest event.created_utc field.
	 * It returns the document.
	 * 
	 * @return
	 */
	
	public DBObject getMostRecentDoc(){
		BasicDBObject d = new BasicDBObject();
		BasicDBObject ctdFields = new BasicDBObject("event.created_utc", 1);
		BasicDBObject sortrecent = new BasicDBObject("event.created_utc", -1);
		DBCursor cursor = getCollection().find(d, ctdFields);
		cursor.sort(sortrecent);
		DBObject first = cursor.one();
		cursor.close();
		return first;
	}
	
	/**
	 * Calls getMostRecentDoc and returns the event.created_utc field.
	 * 
	 * @return	DBObject of most recently created doc
	 */
	
	public Double getMostRecentCreatedUTC(){
		return (Double) ( (DBObject) getMostRecentDoc().get("event")).get("created_utc");
	}
	
	/**
	 * CAlls getMostRecentCreatedUTC and returns a Date Object
	 * 
	 * @return	Double created_utc unix timestamp in seconds
	 */
	
	public Date getMostRecentDate(){
		return utcToDate(getMostRecentCreatedUTC());
	}
	/**
	 * Wraps the FieldComprehenion static helper class.  
	 * 
	 * @param createdUTC
	 * @return
	 */
	
	public static Date utcToDate(Double createdUTC){
		return FieldComprehension.dateFromTimestamp(createdUTC);
	}
	
	/**
	 * Finds unique subreddits in the annotated collection. Returns 
	 * a funky document structure. This document
	 * structure is remedied in the rdt.data.FieldComprehension.subredditIterator .
	 * That methods returns a CloseableIterator, allowing this method to be used
	 * in a nice-field way.
	 * 
	 * @param createdUTC
	 * @param stoppingPoint
	 * @return
	 */
	
	public Cursor getUniqueSubredditsBetween(Double createdUTC, Double stoppingPoint){
		ArrayList<DBObject> aggSbr = new ArrayList<>();
		BasicDBObject lte = new BasicDBObject("$lt", stoppingPoint);
		lte.append("$gte", createdUTC);
		BasicDBObject d = new BasicDBObject("event.created_utc", lte);
		BasicDBObject match = new BasicDBObject("$match", d);
		aggSbr.add(match);
		aggSbr.add(projectSbr);
		return aggregate(aggSbr);
	}
	
	/**
	 * Wraps the getUniqueSubredditsBetween method. 
	 * 
	 * @param createdUTC	High created_utc
	 * @return				MongoDB cursor
	 * @see					getUniqueSubredditsBetween
	 */
	
	public Cursor getUniqueSubredditsBefore(Double createdUTC){
		return getUniqueSubredditsBetween(0.0,createdUTC);
	}
	
	/**
	 * 
	 * 
	 * @param createdUTC		gte created_utc bound
	 * @param stoppingPoint		lt created_utc bound
	 * @return					MongoDB cursor suitable for wrapping in a CloseableIterator
	 * @see						rdt.data.FieldComprehension
	 */
	
	public Cursor getCommentsBetween(Double createdUTC, Double stoppingPoint){
		BasicDBObject onlyComments = new BasicDBObject("event.body", new BasicDBObject("$exists", true));
		BasicDBObject d = new BasicDBObject("$lt", stoppingPoint);
		d.append("$gte", createdUTC);
		onlyComments.append("event.created_utc", d);
		DBCursor cursor = find(onlyComments);
		cursor.batchSize(batchSize);
		cursor.sort(new BasicDBObject("event.created_utc", 1));
		return cursor;
	}
	
	/**
	 * Wraps getCommentsBetween.
	 * 
	 * @param createdUTC	max created_utc bound
	 * @return				MongoDB cursor
	 * @see					getCommentsBetween
	 */
	
	public Cursor getCommentsBefore(Double createdUTC){
		return getCommentsBetween(0.0, createdUTC);
	}
	
	/**
	 * Returns a cursor between ( lt stopping point and gte createdUTC )
	 * specified unix timestamps.
	 * 
	 * @param createdUTC	upper bound created_utc
	 * @param stoppingPoint	lower bound created_utc
	 * @return				MongoDB cursor suitable for wrapping in a CloseableIterator
	 */

	public Cursor getSubmissionsBetween(Double createdUTC, Double stoppingPoint){
		BasicDBObject selftextExists = new BasicDBObject("$exists", true );
		BasicDBObject onlySubmissions = new BasicDBObject("event.selftext", selftextExists);
		BasicDBObject r = new BasicDBObject("$lt", stoppingPoint);
		r.append("$gte", createdUTC);
		onlySubmissions.append("event.created_utc", r);
		DBCursor cursor = find(onlySubmissions);
		cursor.sort(new BasicDBObject("event.created_utc", 1));
		cursor.batchSize(batchSize);
		return cursor;
	}
	
	/**
	 * Wraps getSubmissionsBetween .
	 * 
	 * @param createdUTC	upperbound created_utc unix timestamp
	 * @return				MongoDB cursor
	 * @see					getSubmissionsBetween
	 */
	
	public Cursor getSubmissionsBefore(Double createdUTC){
		return getSubmissionsBetween(0.0, createdUTC);
	}
	
	/**
	 * Returns a cursor that finds submissions with selftext-text. 
	 * 
	 * @param createdUTC
	 * @return
	 */
	
	public Cursor getSelfTextSubmissionsBefore(Double createdUTC){
		//so, set parameters to limit he annotated source
		//need selftext, also, selftext needs to be full
		//{ event.selftext : { $exists : true, "$ne" : "" }, event.created_utc : { "$lt" : "createdUTC"} }
		BasicDBObject a = new BasicDBObject("$exists", true );
		a.append("$ne", "");
		BasicDBObject b = new BasicDBObject("event.selftext", a);
		BasicDBObject c = new BasicDBObject("$lt", createdUTC);
		b.append("event.created_utc", c);
		DBCursor cursor = find(b);
		cursor.sort(new BasicDBObject("event.created_utc", 1));
		cursor.batchSize(batchSize);
		return cursor;
	}
	
	/**
	 * Returns a cursor with documents between the given unix time stamps.
	 * The cursor returns an ugly document format that should
	 * be wrapped in a closeableiterator.
	 * 
	 * @param createdUTC	lt created_utc unix timestamp
	 * @param stoppingPoint	gte created_utc unix timestamp
	 * @return				MongoDB cursor
	 * @see					rdt.data.FieldComprehension
	 */
	
	public Cursor getUniqueAuthorsBetween(Double createdUTC, Double stoppingPoint){
		ArrayList<DBObject> aggParams = new ArrayList<>();
		BasicDBObject a = new BasicDBObject("$lt", stoppingPoint);
		a.append("$gte", createdUTC);
		BasicDBObject s = new BasicDBObject("event.created_utc", a);
		BasicDBObject d = new BasicDBObject("$match", s);
		aggParams.add(d);
		aggParams.add(projectAth);
		return aggregate(aggParams);
	}
	
	/**
	 * Wraps getUniqueAuthorsBetween
	 * 
	 * @param createdUTC	upper bound created_utc unix timestamp
	 * @return				MongoDB cursor
	 * @see					getUniqueAuthorsBetween
	 */
	
	public Cursor getUniqueAuthorsBefore(Double createdUTC){
		return getUniqueAuthorsBetween(0.0,createdUTC);
	}
	
}