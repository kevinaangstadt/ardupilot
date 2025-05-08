#!/bin/bash

# This file does a transplant and starts up ardupilot

# Uncomment the next three comments to let the dump happen
start_time_dump=$(date +%s%3N)
python3 dump_state_covariance.py --device udp:0.0.0.0:14551 # FIXME 
end_time_dump=$(date +%s%3N)
dump_time=$(( end_time_dump - start_time_dump ))
#echo "after dump"

start_time_scp=$(date +%s%3N)
scp -i /home/pi/.ssh/id_rsa pi@192.168.5.1:/home/pi/Peyton/ardupilot/ArduCopter/CoreData0.bin /home/pi/Peyton/ardupilot/ArduCopter # check storage location
scp -i /home/pi/.ssh/id_rsa pi@192.168.5.1:/home/pi/Peyton/ardupilot/ArduCopter/CovarianceData0.bin /home/pi/Peyton/ardupilot/ArduCopter # check storage location
end_time_scp=$(date +%s%3N)
scp_time=$(( end_time_scp - start_time_scp ))

echo "Covariance Dump: $dump_time" >> Timing_log.txt
echo "SCP: $scp_time" >> Timing_log.txt
../build/navio2/bin/arducopter --serial0 udp:localhost:14552 --serial3 /dev/ttyAMA0 --serial1 udp:192.168.0.104:14552 &
PID1=$!

