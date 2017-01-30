#!/bin/bash

if [ $# -eq 0 ]
then
	echo "[$(date +"%T")] [ERROR] You need to provide a config file as an argument. Aborting."
else
	GLOG_minloglevel=2 python calibrate.py -c $1
fi
