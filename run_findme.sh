#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: # $0 <.json db>"
    exit 1
fi

while true; do

    # Start collecting CSI for an adaptive ping.
    sudo ping -Aq 192.168.43.1 &
    sudo ext/log_to_file_3ant_10pkts dat/temp.dat

    sudo killall ping

    # Process the data
    ./src/collect.py dat/temp.dat ? ?
    ./src/fingerprint.py $1 json/online.json

    read -p "Press something to get to next iteration.. (or Ctrl-C to exit)"

done

exit 0
