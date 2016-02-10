package rdt.nlp.data;

import com.mongodb.AggregationOptions;

import com.mongodb.BasicDBObject;
import com.mongodb.Cursor;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;

import java.util.ArrayList;
import java.util.List;
import java.util.Date;

/**
 * Accesses raw unannotated reddit documents. 
 * @author john
 *
 */

/*
 * Subtle implementation note: The range queries used follow the pattern:
 * 	comments/subreddits (before utc) by less than, lt, exclusive operator
 *  comments/subreddits (after utc) by greater than or equal to, gte, inclusive operator
 * 
 * This usage stops the edge case where certain documents can be inserted more than once.
 * This makes insert operations conceptually simpler.
 * 
 */


public class Source extends RedditCollection{
		
	private int batchSize = 1000;
	
	/**
	 * Wraps the MongoDB Collection class. Thusly, it requires 
	 * parameters to reach that point.
	 * @param host	Host of the MongoDB instance
	 * @param port	Port to access the MongoDB host
	 * @param db	database name
	 * @param coll	collection name
	 */
	
	public Source(String host, int port, String db, String coll) {
		super(host, port, db, coll);
	}
	
	public Source(String host, int port, String db, String coll, int batchSize){
		super(host,port,db,coll);
		this.batchSize = batchSize;
	}
	
	/**
	 * Some standard aggregation parameters.
	 * @return
	 */
	
	private AggregationOptions aggOpps(){
		return AggregationOptions.builder()
				.batchSize(batchSize)
				.outputMode(AggregationOptions.OutputMode.CURSOR)
				.build();
	}
	
	/**
	 * Returns the document with the largest created_utc value. Largely relies
	 * on an index on this field if there are a large amount of documents. 
	 * @return	DBObject of the comment or submission
	 */
	
	public DBObject getMostRecentDoc(){
		BasicDBObject d = new BasicDBObject();
		BasicDBObject ctdFields = new BasicDBObject("created_utc", 1);
		BasicDBObject sortrecent = new BasicDBObject("created_utc", -1);
		DBCursor cursor = getCollection().find(d, ctdFields);
		cursor.sort(sortrecent);
		DBObject first = cursor.one();
		cursor.close();
		return first;
	}
	
	/**
	 * Find the most recent document and returns the created_utc from that document
	 * @return
	 */
	
	public Double getMostRecentCreatedUTC(){
		return (Double) getMostRecentDoc().get("created_utc");
	}
	
	/**
	 * Finds the most recent created_utc and turns that into a Date
	 * @return	a Date object
	 */
	
	public Date getMostRecentDate(){
		return utcToDate(getMostRecentCreatedUTC());
	}
	
	public static Date utcToDate(Double createdUTC){
		return FieldComprehension.dateFromTimestamp(createdUTC);
	}
	
	/**
	 * Returns unique subreddits for a given collection.
	 * 
	 * @param createdUTC	The low bound for the created_utc range
	 * @param stoppingPoint	The high bound for the created_utc range
	 * @return				A MongoDB cursor return an ugly document per subreddit
	 */
	
	public Cursor getUniqueSubredditsBetween(Double createdUTC, Double stoppingPoint){
		BasicDBObject onlySubreddit = new BasicDBObject("_id","$subreddit_id");
		onlySubreddit.append("subreddit", new BasicDBObject("$addToSet", "$subreddit"));
		BasicDBObject projectSbr = new BasicDBObject("$group", onlySubreddit);
		ArrayList<DBObject> aggSbr = new ArrayList<>();
		aggSbr.add(new BasicDBObject("$match", AggregationMatch.betweenUTC(createdUTC, stoppingPoint)));
		aggSbr.add(projectSbr);
		return aggregate(aggSbr);
	}
	
	/**
	 * Wraps getUniqueSubredditsBetween. Returns all documents before a specified created_utc
	 * @param createdUTC	The upper bound created_utc document to grab ( created_utc : { lt < "number" } )
	 * @return				A Cursor that iterates over an ugly set of documents.
	 */
	
	public Cursor getUniqueSubredditsBefore(Double createdUTC){
		return getUniqueSubredditsBetween(0.0, createdUTC);
	}
	
	public BasicDBObject comments(){
		return new BasicDBObject("body", new BasicDBObject("$exists", true));
	}
	
	/**
	 * Returns a cursor arg1 >= created_utc < arg2
	 * @param createdUTC	Lower created_utc bound ( lt )
	 * @param stoppingPoint	Upper created_utc bound ( gt )
	 * @return				MongoDB cursor
	 */
	
	// DBCursor cur = find(between(documents(), low, high));
	// return batch(sortUTC(cur));
	
	public Cursor getCommentsBetween(Double low, Double high){
		return batch(sortUTC(find(between(comments(), low, high))));	
	}
	/**
	 * Wraps getCommentsBetween
	 * 
	 * @param createdUTC
	 * @return				MongoDB Cursor
	 */
	public Cursor getCommentsBefore(Double createdUTC){
		return getCommentsBetween(0.0, createdUTC);
	}
	
	/**
	 * Returns condition for submissions only.
	 * @return A BasicDBObject matching for selftext
	 */
	
	public BasicDBObject submissions(){
		return new BasicDBObject("selftext", new BasicDBObject("$exists", true));
	}
	
	/**
	 * Returns a Cursor for the range arg1 >= created_utc < arg2
	 * @param createdUTC
	 * @param stoppingPoint
	 * @return
	 */
	
	// DBCursor cur = find(between(documents(), low, high));
	// return batch(sortUTC(cur));
	
	public Cursor getSubmissionsBetween(Double low, Double high){
		return batch(sortUTC(find(between(submissions(), low, high))));
	}
	
	/**
	 * Wraps getSubmissionsBetween
	 * @param createdUTC
	 * @return
	 */
	
	public Cursor getSubmissionsBefore(Double createdUTC){
		return getSubmissionsBetween(0.0, createdUTC);
	}
	
	public BasicDBObject between(BasicDBObject documents, Double low, Double high){
		documents.append("created_utc", AggregationMatch.between(low, high));
		return documents;
	}
	
	public BasicDBObject documents(){
		return new BasicDBObject();
	}
	
	private DBCursor sortUTC(DBCursor cursor, int how){
		cursor.sort(new BasicDBObject("created_utc", how));
		return cursor;
	}
	
	private DBCursor sortUTC(DBCursor cursor){
		return sortUTC(cursor, 1);
	}
	
	private DBCursor batch(DBCursor cursor, int size){
		cursor.batchSize(size);
		return cursor;
	}
	
	private DBCursor batch(DBCursor cursor){
		return batch(cursor, batchSize);
	}
	
	
	public Cursor getDocumentsBetween(Double low, Double high){
		return batch(sortUTC(find(between(documents(), low, high))));
	}
	
	/**
	 * Returns a cursor representing a set of authors. The DBObject
	 * returned is ugly.
	 * @param createdUTC
	 * @param stoppingPoint
	 * @return				A MongoDB cursor
	 */
	
	public Cursor getUniqueAuthorsBetween(Double low, Double high){
		BasicDBObject projectAth = new BasicDBObject("$group", new BasicDBObject("_id", "$author"));
		ArrayList<DBObject> aggParams = new ArrayList<>();
		aggParams.add(AggregationMatch.betweenUTC(low, high));
		aggParams.add(projectAth);
		return aggregate(aggParams);
	}
	
	public Cursor getUniqueAuthorsBefore(Double createdUTC){
		return getUniqueAuthorsBetween(0.0, createdUTC);
	}
	
	private Cursor aggregate(List<DBObject> params){
		return getCollection().aggregate(params, aggOpps());
	}

}
