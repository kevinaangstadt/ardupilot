from pymavlink import mavutil
import logging
import sys

logger = logging.getLogger(__name__)

def request_data(mav):
    """
    Request a set of EKF data
    :param mav: mavlink object
    :return: list of list of floats
    """
    # wait for a hearbeat to know we are connected
    mav.wait_heartbeat()

    logger.info("sending message")

    # DEBUG
    print("got connection")

    # access mav message
    mav.mav.command_long_send(
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        0, 
        5000000,
        0, 0, 0, 0, 0, 0
    )

    logger.info("message sent")

    print("before ack")

    mav.recv_match(
                        type='STATUSTEXT',
                        condition=
                        'STATUSTEXT.text.strip() == "CORE DUMPED"',
                        blocking=True
    )

    print("done.")

    return


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="udp:localhost:14551", help="device uri; default: udp:localhost:14551")
    parser.add_argument("--baud", type=int, default=115200, help="baud rate, default: 115200")

    args = parser.parse_args()

    mav = mavutil.mavlink_connection(args.device, baud=args.baud)

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    logger.info(request_data(mav))
