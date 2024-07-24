from pymavlink import mavutil
import os
import sys
import time


def initAir(mav):
    file = open("initAir.txt", "x")
    
    time.sleep(1)
    # wait for a hearbeat to know we are connected
    mav.recv_match(type='HEARTBEAT', blocking=True)
    print("recieved heartbeat", file=sys.stderr)

    # This one tells the scripting to start
    mav.mav.command_long_send(
    mav.target_system, 
    mav.target_component, 
    227,
    0, 
    42,
    0, 0, 0, 0, 0, 0)

    #time.sleep(.2)
    # turns on brakes
#    mav.mav.command_long_send(
#        mav.target_system,
#        mav.target_component,
#        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
#        0,
#        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
#        17,
#        0, 0, 0, 0, 0
#    )
# brake mode is 17
    time.sleep(5)

#    mav.mav.rc_channels_override_send(
#        mav.target_system,
#       mav.target_component,
#        0, 0, 1600, 0, 0, 0, 0, 0
#    )
#    while True:
#        rc_channels = mav.recv_match(type = 'RC_CHANNELS', blocking=True)
#        if rc_channels:
#            print(rc_channels.chan3_raw)
#            if rc_channels.chan3_raw == 1600:

#                print("OHYEAAAAAAA")
#                break

    time.sleep(5)
    

    os.remove("initAir.txt")
    print("all done", file=sys.stderr)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="udp:localhost:14550", help="device uri; default: udp:localhost:14550")
    parser.add_argument("--baud", type=int, default=115200, help="baud rate, default: 115200")

    print("ready", file=sys.stderr)
    args = parser.parse_args()

    mav = mavutil.mavlink_connection(args.device, baud=args.baud)

    initAir(mav)

