#ifndef DELTAROBOT
#define DELTAROBOT

// Namespace Delta Robot
namespace DeltaRobot
{
	// Prototype
	class Artel;
}

#include "Arduino.h"
#include "Motion.h"
#include "Pins.h"


namespace DeltaRobot
{

    class Artel
    {
        public:
            Artel();
            void setup();

            bool is_running;
            bool is_homing;
            bool is_idle;

            DeltaRobot::Motion motion;
    };
}
#endif

// Using Namespace Delta Robot
using namespace DeltaRobot;
