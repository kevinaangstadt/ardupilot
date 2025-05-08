from pymavlink import mavutil
import os
import sys
import time
from I2CSwitch import I2CSwitch 

def initAir(mav):
    mav.recv_match(
                        type='STATUSTEXT',
                        condition=
#                       'STATUSTEXT.text.strip() == "EKF3 IMU0 is using GPS"',
                        'STATUSTEXT.text.strip() == "Timing Position Acquired"',
                        blocking=True
    )


    file = open("initAir.txt", "x")
    
    #time.sleep(1)
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
    switch = I2CSwitch()
    start_time = time.time()
    mesToArm = 0
    armToBrake = 0
    while time.time() - start_time < 60:  # 60-second timeout
        msg = mav.recv_match( blocking=True)
        if not msg:
            continue
        msg_type = msg.get_type()
        
        if msg_type == 'STATUSTEXT' and msg and "Brakes ON" in msg.text:
            timeBeforeSwitch = int(time.monotonic() * 1000)
            switch.choose_device(0)
            timeAfterSwitch = int(time.monotonic() * 1000)  # Milliseconds since boot
            switchTime = timeAfterSwitch - timeBeforeSwitch
            #print("Time for I2cSwitch: " + switchTime)
            #print(f"lua: time {current_time} ms - Lua script confirmed brakes are ON!", file=sys.stderr)
            #print("Lua script confirmed brakes are ON!", file=sys.stderr)
            os.remove("initAir.txt")
        if msg_type == 'STATUSTEXT' and "Message Received to Armed" in msg.text:
            mesToArmStr = ""
            for char in msg.text:
                if char.isdigit():
                    mesToArmStr += char
            mesToArm = int(mesToArmStr)
        if msg_type == 'STATUSTEXT' and 'Arm to Brake' in msg.text:
            armToBrakeStr = ""
            for char in msg.text:
                if char.isdigit():
                    armToBrakeStr += char
            armToBrake = int(armToBrakeStr)


        if mesToArm > 0 and armToBrake > 0:
            with open("Timing_log.txt", "a") as f:
                message = f'Message recieved to arm: {mesToArm}'
                f.write(message + "\n")
                message = f'Arm to Brake: {armToBrake}'
                f.write(message + "\n")
                message = f'Switch Time: {switchTime}'
                f.write(message + "\n")
                exit(0)

    print("Timeout: Did not receive Lua confirmation!", file=sys.stderr)

    os.remove("initAir.txt")
    print("all done", file=sys.stderr)
    exit(1)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="udp:localhost:14552", help="device uri; default: udp:localhost:14550")
    parser.add_argument("--baud", type=int, default=115200, help="baud rate, default: 115200")

    print("ready", file=sys.stderr)
    args = parser.parse_args()

    mav = mavutil.mavlink_connection(args.device, baud=args.baud)

    initAir(mav)


