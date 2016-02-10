package rdt.nlp.data;

import java.net.UnknownHostException;

import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import com.mongodb.ServerAddress;
import com.mongodb.DBCursor;

/**
 * Typical database driver-extra-wrapper-class.
 * Exposes some methods on MongoDB and exposes the DBCollection
 * object.
 * 
 * @author john
 *
 */

public class RedditCollection {
	
	private MongoClient client;
	private DB db;
	private DBCollection coll;
	public RedditCollection(String host, int port, String db, String coll){
		try{
			client = new MongoClient(new ServerAddress(host,port));
			this.db = client.getDB(db);
			this.coll = this.db.getCollection(coll);
		} catch (UnknownHostException e){
			System.out.println(e);
			System.exit(1);
		}
	}
	
	public DBCollection getCollection(){
		return coll;
	}
	
	public DBCursor find(DBObject ref){
		return getCollection().find(ref);
	}
	
	public DBCursor find(){
		return getCollection().find();
	}
	
	public DBObject findOne(){
		return getCollection().findOne();
	}
	
	public DBObject findOne(DBObject o ){
		return getCollection().findOne(o);
	}
	
	public long getCount(){
		return getCollection().getCount();
	}
	
	public void drop(){
		getCollection().drop();
	}
	
	public long getCount(DBObject query){
		return getCollection().getCount(query);
	}
	
	public long getCount(DBObject query, DBObject fields){
		return getCollection().getCount(query, fields);
	}
}
