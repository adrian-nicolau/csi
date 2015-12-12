#!/bin/bash

if [[ $# -ne 2 ]]; then
    echo "Usage: # $0 <time to run> <.dat file>"
    exit 1
fi

# Start collecting CSI for an adaptive ping.
sudo ext/log_to_file_3ant $2 &
sudo ping -Aq -w $1 192.168.43.1

# Stop log_to_file via SIGINT, not SIGKILL.
sudo killall -s SIGINT log_to_file_3ant

# Process the data and show the results.
./src/process_csi.py $2
PNGDIR=`ls -t png/ | head -n 1`
eog png/$PNGDIR/0001.png

exit 0
