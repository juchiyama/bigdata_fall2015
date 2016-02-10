package rdt.nlp.hadoop;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import rdt.nlp.hadoop.POS.Map;
import rdt.nlp.hadoop.POS.Reduce;

public class POSDriver extends Configured implements Tool{

	@Override
	public int run(String[] args) throws Exception {
		
		JobConf conf = new JobConf(POS.class);
		conf.setJobName("POS");
		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(Text.class);
		//conf.setNumMapTasks(2);
		//conf.set("mapred.tasktracker.map.tasks.maximum", "2");
		conf.set("mapred.child.java.opts", "-Xmx2548m");
		
		conf.setMapperClass(Map.class);
		conf.setCombinerClass(Reduce.class);
		conf.setReducerClass(Reduce.class);
		conf.setInputFormat(TextInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);
		
		FileInputFormat.setInputPaths(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));
		JobClient.runJob(conf);
		return 0;
	}
	
	public static void main( String[] args ) throws Exception {
		int exitCode = ToolRunner.run(new POSDriver(), args);
		System.exit(exitCode);
	}
	
}
