#!/bin/sh

no_of_directories=$(ls -l | grep -c ^d)

if [ $no_of_directories -ne 0 ]
then
    du -h */ --max-depth=0 | sort -hr | awk '
    BEGIN { OFS="\t" }
    { 
        name=substr($2,1,length($2)-1)
        size=$1;
        print name, size;
    }'
fi  