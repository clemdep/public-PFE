#!/bin/sh 
for file in ./*.py; 
do
    if [ "$file" != "./__init__.py" ]
    then
      autopep8 -aa --in-place $file 
    fi
done 

