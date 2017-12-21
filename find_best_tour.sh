#!/bin/bash
cd /mnt/d/Robbie/Documents/dev/sm-ai-search/tours/
echo $1
# echo "tourAISearchFile$1.txt"
# $OUTPUT = `find`
$OUTPUT = `/usr/bin/find | /bin/grep tourAISearchfile$1.txt`
# find | grep tourAISearchfile$1.txt
IFS=$'\n' read -r -a files <<< "$OUTPUT" #"$(find | grep tourAISearchfile$1.txt)"

echo ${#files[@]}

for element in "${files[@]}"
do
	echo "$element"
done