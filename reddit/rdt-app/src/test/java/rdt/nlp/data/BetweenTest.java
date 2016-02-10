package rdt.nlp.data;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.junit.Test;

import com.mongodb.Cursor;
import com.mongodb.DBObject;

public class BetweenTest {
	
	@Test
	public void test() {
		Source source = new Source("localhost",27017,"reddit_stream","combined",10_000);
		Double mostRecent = source.getMostRecentCreatedUTC();
		Date mostRecentD = source.getMostRecentDate();
		System.out.println(
			mostRecentD + "\n" + 
			String.valueOf(mostRecent)
		);
		Double lowerBound = mostRecent - 1000000;
		Cursor cmms = source.getCommentsBetween(lowerBound, mostRecent);
		List<DBObject> comments = new ArrayList<>();
		long size = 0;
		try{
			while(cmms.hasNext()){
				DBObject cmm = cmms.next();
				Double created_utc = (Double) cmm.get("created_utc");
				size++;
				assertTrue(created_utc < mostRecent && created_utc > lowerBound);
			}
		} finally {
			cmms.close();
		}
		System.out.println(size);
	}

}
