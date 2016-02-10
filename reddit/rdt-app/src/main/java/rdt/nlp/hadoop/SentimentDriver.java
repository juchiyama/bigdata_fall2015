package rdt.nlp.hadoop;

import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class SentimentDriver extends Configured implements Tool{

	@Override
	public int run(String[] args) throws Exception{
		
		JobConf conf = new JobConf(Sentiment.class);
		conf.setJobName("Sentiment");
		
		conf.setOutputKeyClass(Text.class);
		conf.setOutputKeyClass(Text.class);
		
		// conf.set("mapred.child.java.opts", "-Xmx2548m");
		
		conf.setMapperClass(Sentiment.Map.class);
		conf.setReducerClass(Sentiment.Reduce.class);
		conf.setInputFormat(TextInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);
		
		FileInputFormat.setInputPaths(conf,  new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));
		JobClient.runJob(conf);
		return 0;
	}
	
	public static void main( String[] args) throws Exception {
		int exitCode = ToolRunner.run(new SentimentDriver(), args);
		System.exit(exitCode);
	}
}
