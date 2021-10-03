
# SSD Assignment-1

- **Name**: Haridasu Yaswanth
- **Rollno**: 2021201032
- **Branch**: M.Tech CSE
***

### Question 1: Printing the directories in the descending order of their sizes

1. If there are no directories present in the current directory, **nothing is printed**

2. Printing the tab spaces using Output Field Separator (OFS = "\t") in awk program. Due to the difference in the length of the file names, sometimes the output may not be oriented properly.

Command to run: `bash q1.sh`

***

### Question 2: Printing all the words ending with *ing* of a given input file in new line inside a file

1. If the no.of arguments provided are not equal to 2 (one for input and other for output file) then following message will be displayed: <br />
`Provide two arguments for input file and output file`

Command to run: `bash q2.sh inputfile.txt outputfile.txt`
- *inputfile.txt* contains the random text
- *outputfile.txt* contains the final output .i.e the words ending with *ing* in lower case

***
    
### Question 3: Checking whether the input word contains any BASH command by permuting the letters of the input word

1. If no argument is provided as input word or no.of arguments are more than 1 then the following message will be displayed: <br />
`Provide one argument as input word`

Command to run: `bash q3.sh input_word`

***

### Question 4: 

1. Written two functions:
    - `intToRoman()` which converts the given integer into roman equivalent number.
    - `romanToInt()` which converts the given roman numeral into its equivalent integer.

### Valid cases of input arguments:
***

| No.of Arguments |  Type          | Result                                     |
| :-------------: | :------------- | :----------------------------------------- |
| 1               | Integer        | Print its Roman equivalent number          |
| 2               | Integer        | Print sum of two integers as roman numeral |
| 2               | Roman          | Print sum of two roman numerals as integer |

### Invalid cases are handled as follows:
***

| No.of Arguments |  Type                        | Result                                     |
| :-------------: | :--------------------------- | :----------------------------------------- |
| 0               |      -                       | Printing "Provide correct no.of arguments" |
| 1               | Not a valid integer          | Print nothing                              |
| 1               | Intger <=0                   | Print nothing                              |
| 2               | Not a valid integers/romans  | Print nothing                              |
| 2               | 0 and 0                      | Print nothing                              |
| 2               | Sum of two integers <=0      | Print nothing                              |
| > 2             |          -                   | Printing "Provide correct no.of arguments" |

Command to run: `bash q4.sh 10` <br /> output: `X` <br />
Command to run: `bash q4.sh 10 20` <br /> output: `XXX` <br />
Command to run: `bash q4.sh X XX` <br /> output: `30` <br />
Command to run: `bash q4.sh X XX XXX` <br /> output:  `Provide correct no.of arguments`

*** 

### Question 5:

No assumptions are made. <br />
Command to run: `bash q5.sh`

***