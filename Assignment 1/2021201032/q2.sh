#! /bin/sh

if [ $# -eq 2 ]
then
    awk '{
        out="";
        for(i=1; i<=NF; i++){
            # For getting last three letters of the word
            l = length($i)-2;
            if(substr(tolower($i),l) == "ing")
                print tolower($i) 
        }
    } ' $1 > $2
else
    echo "Provide two arguments for input file and output file"
fi