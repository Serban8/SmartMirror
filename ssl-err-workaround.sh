#!/bin/bash

ret=1

while [ $ret != 0 ]
do
	python3 MainBlynk.py
	ret=$?
done

