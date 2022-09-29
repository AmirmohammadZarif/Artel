//
// Created by Amirmohammad on 9/29/22.
//

#include "Robot.h"

int Connect(){
    serial::Serial my_serial("/dev/ttyACM0", 19200, serial::Timeout::simpleTimeout(3000));

}