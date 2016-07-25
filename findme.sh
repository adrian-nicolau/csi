#!/bin/bash

# if [[ $# -ne 1 ]]; then
#     echo "Usage: # $0 <.json db>"
#     exit 1
# fi

while true; do

    # Allow me to go to a position :-).
    sleep 5

    # Start collecting CSI for an adaptive ping.
    sudo ping -Aq 192.168.43.1 &
    sudo ext/log_to_file_3ant_10pkts dat/temp.dat

    sudo killall ping

    # Process the data
    ./src/collect.py dat/temp.dat ? ?
    db=`ls -t json/ | head -2 | tail -1`
    echo "Using db $db"
    ./src/fingerprint.py "json/"$db json/online.json

    read -p "Press something to get to next iteration.. (or Ctrl-C to exit)"

done

exit 0
