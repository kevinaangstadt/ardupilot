#include "Copter.h"

// DEBUG
#include <iostream>

#ifdef USERHOOK_INIT
void Copter::userhook_init()
{
    // DEBUG

    // This arms the motors if they are not already
    if (!motors->armed()) {
        init_rc_out();
        enable_motor_output();
        motors->armed(true);
        hal.util->set_soft_armed(true);
    }

//     motors->set_desired_spool_state(AP_Motors::DesiredSpoolState::THROTTLE_UNLIMITED);

//     set_land_complete(false);

//     attitude_control->set_throttle_out(0.5f,
//                                        true,
//                                        g.throttle_filt);

//     std::cout << "in usercode.cpp" << std::endl;
}
#endif

#ifdef USERHOOK_FASTLOOP
void Copter::userhook_FastLoop()
{
    // put your 100Hz code here
}
#endif

#ifdef USERHOOK_50HZLOOP
void Copter::userhook_50Hz()
{
    // put your 50Hz code here
}
#endif

#ifdef USERHOOK_MEDIUMLOOP
void Copter::userhook_MediumLoop()
{
    // put your 10Hz code here
}
#endif

#ifdef USERHOOK_SLOWLOOP
void Copter::userhook_SlowLoop()
{
    // put your 3.3Hz code here
}
#endif

#ifdef USERHOOK_SUPERSLOWLOOP
void Copter::userhook_SuperSlowLoop()
{
    // put your 1Hz code here

    // DEBUG


    // This arms the motors if they are not already
    // if (!motors->armed()) {
    //     init_rc_out();
    //     enable_motor_output();
    //     motors->armed(true);
    //     hal.util->set_soft_armed(true);
    // }


    // motors->set_desired_spool_state(AP_Motors::DesiredSpoolState::THROTTLE_UNLIMITED);

    // set_land_complete(false);

    // attitude_control->set_throttle_out(0.5f,
    //                                    true,
    //                                    g.throttle_filt);

    // std::cout << "in usercode slowloop" << std::endl;
}
#endif

#ifdef USERHOOK_AUXSWITCH
void Copter::userhook_auxSwitch1(uint8_t ch_flag)
{
    // put your aux switch #1 handler here (CHx_OPT = 47)
}

void Copter::userhook_auxSwitch2(uint8_t ch_flag)
{
    // put your aux switch #2 handler here (CHx_OPT = 48)
}

void Copter::userhook_auxSwitch3(uint8_t ch_flag)
{
    // put your aux switch #3 handler here (CHx_OPT = 49)
}
#endif
