#! /bin/sh

# Creating directory named temp_activity
mkdir temp_activity

# Moving into that directory
cd temp_activity

# Creating 50 files named temp<i>.txt where 1<=i<=50
touch temp{1..50}.txt

# Changing extensions of files temp1.txt to temp25.txt from txt to md
i=1
while [ $i -lt 26 ]
do
	mv "temp$i.txt" "temp$i.md"
	(( i++ ))
done

# Chaging file names from temp to temp_modified

for file in *
do
	file_name=${file%.*}
	file_extension=${file##*.}
	new_name=${file_name}"_modified."${file_extension}
	mv "$file" "$new_name"
done

# Zipping .txt files and naming it as txt_compressed.zip
zip -q txt_compressed.zip *.txt
