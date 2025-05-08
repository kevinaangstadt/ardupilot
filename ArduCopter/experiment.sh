#!/bin/bash
echo "first"
# calls dump state covariance, pulls files over, starts ardupilot
sudo ./goArduCopter.sh
echo "second"
#sleep 35
# starts the lua script, puts us in the air and turns on brakes
python3 ./initAir.py &
PID1=$!
wait $PID1
#echo "shell: time $(awk '{print int($1 * 1000)}' /proc/uptime) ms"
# switch control over
#sleep 1
#sudo i2cset -y 1 0x26 0x0 0x0
DATE_STR=$(date +"%Y-%m-%d_%H-%M-%S")
DEST_DIR="../../Timing"
mv Timing_log.txt "${DEST_DIR}/Timing_log_${DATE_STR}.txt"
echo "last"
