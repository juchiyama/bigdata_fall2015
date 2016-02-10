use JSON qw(decode_json);


my $ct = 0;
while(<STDIN>){
	$ct++;
	chomp;
	print "$ct\n";
	decode_json $_;

}
