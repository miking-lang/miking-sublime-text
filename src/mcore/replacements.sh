#!/bin/sh

if [ $# -ne 1 ]; then
	echo "usage: replacements.sh <syntax-file>"
	exit 1
fi

FILE=$1

if [ ! -e $FILE ]; then
	echo "error: File \"$FILE\" does not exist"
	exit 1
fi

# 'set: []' -> 'pop: true'
sed -i 's/set: \[\]/pop: true/g' $FILE

