-- Example of receiving MAVLink commands
local mavlink_msgs = require("MAVLink/mavlink_msgs")
delay_start = 0
timing_position_time = 0
motors_time = 0
brakes_time = 0
timPosAcqToArm = 0
ArmToBrake = 0

local waiting_for_delay = false
local COMMAND_ACK_ID = mavlink_msgs.get_msgid("COMMAND_ACK")
local COMMAND_LONG_ID = mavlink_msgs.get_msgid("COMMAND_LONG")
local do_brakes = false
local did_brakes = false
local msg_map = {}
msg_map[COMMAND_ACK_ID] = "COMMAND_ACK"
msg_map[COMMAND_LONG_ID] = "COMMAND_LONG"

-- Initialize MAVLink rx with number of messages, and buffer depth
mavlink:init(1, 10)

-- Register message ID to receive
mavlink:register_rx_msgid(COMMAND_LONG_ID)

local MAV_CMD_DO_SET_MODE = 176
local MAV_CMD_WAYPOINT_USER_1 = 31000

-- Block AP parsing user1 so we can deal with it in the script
-- Prevents "unsupported" ack
mavlink:block_command(MAV_CMD_WAYPOINT_USER_1)

local RC3 = rc:get_channel(3)
-- Flag to track if we should check motor status
local checking_motor = false


function turn_brakes()
    vehicle:set_mode(17)
    copter:set_land_status(false)
    brakes_time = millis()
--    checking_motor = true
    did_brakes = true
    do_brakes = false
    gcs:send_text(0, "Brakes ON")

    return 0
end


function handle_command_long(cmd)
    if cmd.command == 227 then
        timing_position_time = millis()
        arming:arm()
        gcs:send_text(0, "Got command long")
        
        -- Override throttle and change flight mode
        RC3:set_override(1800)
        delay_start = millis() + 4000
        do_brakes = true
--        local time_now = millis()
--        local new_time = millis()
--        vehicle:set_mode(17)
--        copter:set_land_status(false)

        -- Enable motor checking in update()
        checking_motor = true

        return 0  -- Return valid number for MAVLink acknowledgment
    end
    return 0
end

function update()
    local msg, chan = mavlink:receive_chan()
    if msg then
        local parsed_msg = mavlink_msgs.decode(msg, msg_map)
        if parsed_msg then
            local result
            if parsed_msg.msgid == COMMAND_LONG_ID then
                result = handle_command_long(parsed_msg)
            end

            if result then
                -- Send acknowledgment for the received command
                local ack = {
                    command = parsed_msg.command,
                    result = result,
                    progress = 0,
                    result_param2 = 0,
                    target_system = parsed_msg.sysid,
                    target_component = parsed_msg.compid
                }

                mavlink:send_chan(chan, mavlink_msgs.encode("COMMAND_ACK", ack))
            end
        end
    end


    if do_brakes and  millis() >= delay_start and not did_brakes then
        turn_brakes()
        --brakes_time = millis()
    end



    -- If we're checking for motor status, look at PWM values
    if checking_motor then
        for i = 33, 38 do  -- Check all six motor outputs
--            local channel = servo.find_channel(i + 32)  -- Function numbers start from 33 for motor 1 (SERVO1_FUNCTION = 33)
            local pwm = SRV_Channels:get_output_pwm(i)
--            gcs:send_text(0, "Motor " .. i .. " PWM: " .. pwm)
            if pwm and pwm > 1100 then
                motors_time = millis()
--                local time_now = millis()  -- Get system time in milliseconds
                -- Print to standard output
--                print("lua")
 --               print(tostring(time_now))
                checking_motor = false  -- Stop checking once confirmed
                waiting_for_delay = true
                break
            end
        end
    end


  
    if waiting_for_delay and did_brakes then
        timPosAcqToArm = motors_time - timing_position_time
        ArmToBrake = brakes_time - motors_time
        
        --gcs:send_text(0, "motors_time=" .. tostring(motors_time))
        --gcs:send_text(0, "time_pos" .. tostring(timing_position_time))
        --gcs:send_text(0, "brakes" .. tostring(brakes_time))
--      
--  gcs:send_named_float("motors", tonumber(motors_time / 1000))
--        gcs:send_named_float("timing posititon", tonumber(timing_position_time / 1000))
        --gcs:send_named_float("brakes", tonumber(brakes_time / 1000))
        gcs:send_text(0, "Message Received to Armed: " .. tostring(timPosAcqToArm))
        gcs:send_text(0, "Arm to Brake: " .. tostring(ArmToBrake))

        waiting_for_delay = false
    end
    

    return update, 500  -- Schedule update function every 500ms
end

return update()
