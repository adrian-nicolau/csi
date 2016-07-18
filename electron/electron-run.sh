#!/bin/bash

ws='/home/adrian/workspace/csi'

# Start an adaptive ping for the whole script run.
ping -Aq 192.168.1.1 &

while true; do
  # Start collecting CSI.
  sudo $ws/ext/log_to_file_3ant_1pkt $ws/dat/electron.dat
  # Process the data and show the results.
  $ws/src/process_csi.m $ws/dat/electron.dat &> /dev/null
  # Print crafted message to trigger Electron image reload.
  echo REFRESH
done
