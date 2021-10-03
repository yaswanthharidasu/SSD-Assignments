#! /bin/sh

intToRoman(){
    integer=$1
    values=(1000 900 500 400 100 90 50 40 10 9 5 4 1)
    romans=("M" "CM" "D" "CD" "C" "XC" "L" "XL" "X" "IX" "V" "IV" "I")
    ans=""
    for ((i=0; i<13; i++))
    do
        while [ $integer -ge ${values[$i]} ]
        do
            ans=${ans}${romans[$i]}
            (( integer-=${values[$i]} ))
        done
    done
    echo $ans
}

romanToInt(){
    declare -A roman_values

    roman_values=(
        ['M']=1000
        ['D']=500
        ['C']=100
        ['L']=50
        ['X']=10
        ['V']=5   
        ['I']=1
    )

    roman=$1
    roman_length=${#roman}
    ans=0
    i=0
    while [ $i -lt $(( $roman_length-1 )) ]
    do
        j=$(($i+1))
        curr_value=${roman_values[${roman:i:1}]}
        next_value=${roman_values[${roman:j:1}]}
        if [ $curr_value -ge $next_value ]
        then
            (( ans+=$curr_value ))
        else
            (( ans-=$curr_value ))
        fi
        ((i++))
    done
    curr_value=${roman_values[${roman:i:1}]}
    ((ans+=$curr_value))
    echo $ans
}

if [ $# -eq 1 ]
then
    one=$1
    if [[ "$one" =~ ^[0-9]+$ ]]
    then
        if [ $one -gt 0 ]
        then
            ans=$(intToRoman $1)
            echo $ans
        fi
    # else
    #     echo "Provide correct input"
    fi
elif [ $# -eq 2 ]
then
    one=$1
    two=$2
    if [[ "$one" =~ ^[IVXLCDM]+$ ]] && [[ "$two" =~ ^[IVXLCDM]+$ ]]
    then
        num1=$(romanToInt $one)
        num2=$(romanToInt $two)
        sum=$(($num1+$num2))
        echo $sum
    elif [[ "$one" =~ ^[0-9]+$ ]] && [[ "$two" =~ ^[0-9]+$ ]] && [ $one -ne 0 ] || [ $two -ne 0 ]
    then
        sum=$(($one+$two))
        if [ $sum -gt 0 ]
        then
            ans=$(intToRoman $sum)
            echo $ans
        fi
    # else
    #     echo "Provide correct input"
    fi
else
    echo "Provide correct no.of arguments"
fi
