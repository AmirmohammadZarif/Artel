#include "Artel.h"

Artel::Artel(){

}

void Artel::setup(int serialRate){
    Serial.begin(9600);

    pinMode(Pins::motorADir, OUTPUT);
    pinMode(Pins::motorAStep, OUTPUT);

    pinMode(Pins::motorBDir, OUTPUT);
    pinMode(Pins::motorBStep, OUTPUT);

    pinMode(Pins::motorCDir, OUTPUT);
    pinMode(Pins::motorCStep, OUTPUT);

    pinMode(Pins::sensorA, INPUT);
    pinMode(Pins::sensorB, INPUT);
    pinMode(Pins::sensorC, INPUT);

    pinMode(Pins::estop, INPUT);
}