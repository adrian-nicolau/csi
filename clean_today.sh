#!/bin/bash

DATE=`date +%m%d`

echo "rm -rf png/data_$DATE*"
rm -rf png/data_"$DATE"_*

echo "rm -f json/data_$DATE.json"
rm -f json/data_"$DATE".json
