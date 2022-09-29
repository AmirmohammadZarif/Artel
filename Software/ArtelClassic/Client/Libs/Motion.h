#ifndef MOTION
#define MOTION

#include "Arduino.h"
#include "Pins.h"
#include <AccelStepper.h>


namespace DeltaRobot
{
	class Motion
	{
	private:
        int status;
	public:
		// Motion();
    

        struct pos{
            double x;
            double y;
            double z;
        }

        // void setupMotors(int maxSpeed, int maxAcceleration);
        // void move(AccelStepper motor, int steps);
        // void move(AccelStepper motor, int steps, int speed, int acceleration);
        // void reset(AccelStepper motor);
		// void ptp(DeltaRobot::MotionData &servoA, DeltaRobot::MotionData &servoB, DeltaRobot::MotionData &servoC, float speed);
	};

     
}
#endif