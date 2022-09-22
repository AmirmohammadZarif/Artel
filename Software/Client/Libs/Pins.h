#ifndef PINS
#define PINS

#include "Arduino.h"

namespace Pins
{
	// Stepper Motors Pins
	const int motorAStep = 3;
	const int motorADir = 2;
	const int motorBStep = 5;
	const int motorBDir = 4;
	const int motorCStep = 7;
	const int motorCDir = 6;

	// Proximity Sensor Pins
	const int sensorA = 0;
	const int sensorB = 1;
	const int sensorC = 2;

	// Buttons
	const int estop = 3;


}
#endif