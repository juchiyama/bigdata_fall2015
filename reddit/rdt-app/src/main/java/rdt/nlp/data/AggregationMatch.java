package rdt.nlp.data;

import java.util.Collection;
import java.util.List;

import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

/**
 * Provides match arguments for aggregatoin
 * operations. These arguments could
 * be used in many places.
 * 
 * Currently, this supports aggregation
 * for nouns only. Later, adjective aggregation
 * will occur.
 * 
 * @author John Uchiyama
 *
 */
public class AggregationMatch {
	
	/**
	 * Returns a BasicDBObject with parameters to get a timespan
	 * of documents that match at least one given noun.
	 * 
	 * @param low	lower bound created_utc
	 * @param high	upper bound created_utc
	 * @param nouns	Collection of nouns to search for
	 * @return		BasicDBObject match parameter
	 */

	public static BasicDBObject matchBetweenUTCWithNouns(Double low,
			Double high, Collection<String> nouns){
		//{event.created_utc : { lte : , gte } , features.nouns : ['sdfas'] 
		return new BasicDBObject("$match", betweenUTCWithNouns(low,high,nouns));
	}
	
	/**
	 * Specifies the match parameter of an aggregation.
	 * Matches nouns given for nouns in the document. 
	 * 
	 * 
	 * @param low	lower bound created_utc unix timestamp
	 * @param high	lower bound created_utc unix timestamp
	 * @param nouns	Collection of nouns to be searched for
	 * @return		BasicDBObject as match parameters
	 */
	
	public static BasicDBObject betweenUTCWithNouns(Double low,
			Double high, Collection<String> nouns){

		BasicDBObject d = new BasicDBObject("event.created_utc", between(low,high));
		
		BasicDBObject e = new BasicDBObject("$in", nouns);
		d.append("features.nouns", e);
		
		return d;
	}
	
	public static BasicDBObject between(Double low, Double high){
		BasicDBObject a = new BasicDBObject("$lt", high);
		a.append("$gte", low);
		return a;
	}
	
	public static BasicDBObject betweenUTC(Double low, Double high){
		BasicDBObject s = new BasicDBObject("created_utc", between(low,high));
		BasicDBObject d = new BasicDBObject("$match", s);
		return d;
	}
}
