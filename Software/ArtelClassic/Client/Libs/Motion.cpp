#include "Motion.h"


void DeltaRobot::Motion::move(int motor_id, int steps){

}

void DeltaRobot::Motion::move(int motor_id, int steps, int speed, int acceleration){

}

void DeltaRobot::Motion::setupMotors(int maxSpeed, int maxAcceleration){
	AccelStepper motorA = AccelStepper(AccelStepper::DRIVER, Pins::motorAStep, Pins::motorADir);
	AccelStepper motorB = AccelStepper(AccelStepper::DRIVER, Pins::motorBStep, Pins::motorBDir);
	AccelStepper motorC = AccelStepper(AccelStepper::DRIVER, Pins::motorCStep, Pins::motorCDir);

    motorA.setMaxSpeed(maxSpeed);
    motorA.setAcceleration(maxAcceleration);

    motorB.setMaxSpeed(maxSpeed);
    motorB.setAcceleration(maxAcceleration);

    motorC.setMaxSpeed(maxSpeed);
    motorC.setAcceleration(maxAcceleration);
}