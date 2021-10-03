#! /bin/sh

if [ $# -ne 1 ]
then
    echo "Provide one argument as input word"
    exit 0
fi

string=$1
sorted_string=$(echo $string | grep -o . | sort | tr -d '\n')
commands=$(compgen -c)
output=""
for var in $commands
do
    if [[ ${#var} -ne ${#sorted_string} ]]
    then
        continue
    fi

    sorted_command=$(echo $var | grep -o . | sort | tr -d '\n')
    
    if [[ $sorted_command == $sorted_string ]]
    then
        output=$output" "$var
    fi
done

if [[ ${#output} -eq 0 ]]
then
    echo "NO"
else
    echo -n -e "YES"'\t'
    echo $output | tr ' ' '\n' | sort -u | tr '\n' '\t' | awk '{print}'
fi
