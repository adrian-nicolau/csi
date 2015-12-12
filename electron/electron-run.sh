#!/bin/bash

ws='/home/adrian/workspace/csi'

while true; do
  # Start collecting CSI for an adaptive ping.
  sudo $ws/ext/log_to_file_3ant $2 &
  sudo ping -Aq -w $1 192.168.43.1

  # Stop log_to_file via SIGINT, not SIGKILL.
  sudo killall -s SIGINT log_to_file_3ant

  # Process the data and show the results.
  $ws/src/process_csi.py $2
  # Find the latest plot.
  result=`find $ws/png -type f -printf "%T@ %p\n" | sort -n | cut -d' ' -f 2 | tail -n 1`
  # Print crafted message to trigger Electorn image reload.
  echo REFRESH:$result
done
