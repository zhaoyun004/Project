#!/usr/bin/perl

use strict;
use warnings;

our $test;

my $file = 'first.gui';
open my $info, $file or die"Could not open $file: $!";

sub is_blank()
{
  for (my $i=0; $i<length $1; $i++) {
    if (substr($1, $i, $i+1) != ' ' or substr($1, $i, $i+1) != '\t' or substr($1, $i, $i+1) != '\n' or substr($1, $i, $i+1) != '\r') {
      return 0;
    }
  }
  return 1;
}

while( my $line = <$info>) {
  print $line;
  print substr($line, 0, 1)."\n"; 
}

close $info;

foreach (keys %main::) {
    print $_ . "\n";
}

my %data = ('google'=>'google.com', 'runoob'=>'runoob.com', 'taobao'=>'taobao.com');

print "\$data{'google'} = $data{'google'}\n";
print "\$data{'runoob'} = $data{'runoob'}\n";
print "\$data{'taobao'} = $data{'taobao'}\n";