#!/bin/bash

# if [[ $# -ne 1 ]]; then
#     echo "Usage: # $0 <.dat file>"
#     exit 1
# fi

while true; do
    read -p "What is your X? " xpos
    read -p "What is your Y? " ypos

    echo "You are at ($xpos, $ypos)"

    # Allow me to exit the room :-).
    # sleep 10

    # Start collecting CSI for an adaptive ping.
    sudo ping -Aq 192.168.43.1 &
    sudo ext/log_to_file_3ant_10pkts dat/temp.dat

    sudo killall ping

    # # Stop log_to_file via SIGINT, not SIGKILL.
    # sudo killall -s SIGINT log_to_file_3ant

    # Process the data and show the results.
    ./src/collect.py dat/temp.dat $xpos $ypos
    # PNGDIR=`ls -t png/ | head -n 1`
    # eog png/$PNGDIR/0001.png

    read -p "Press something to get to next iteration.. (or Ctrl-C to exit)"
done

exit 0
