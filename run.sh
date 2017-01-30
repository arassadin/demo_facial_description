#!/bin/bash

if [ $# -eq 0 ]
then
	echo "[$(date +"%T")] [ERROR] You need to provide a config file as an argument. Aborting."
else
	CAFFE_ROOT=/home/alexandr/distr/caffe/ GLOG_minloglevel=2 python app.py -c $1
fi
