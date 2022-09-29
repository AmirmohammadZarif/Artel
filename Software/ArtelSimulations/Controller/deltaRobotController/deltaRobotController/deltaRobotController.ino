#include <Servo.h>
#include <stdio.h>
//It's whaat you're gonna need with PCA9685.
#include <Wire.h>
//Add this to your Library (I sent the lib)
#include "PCA9685.h"

PCA9685 driver;
PCA9685_ServoEvaluator pwmServo(102, 470);

const int channels = 3;

//Configuration
bool isUsingDriver = 1; // 0 for if servos connected to Arduino directly, 1 if you're using PCA9685

//Pins Setup in Direct Mode
const int M1Pin = 8;
const int M2Pin = 9;
const int M3Pin = 10;

//Channels in Driver Mode
const int M1Channel = 0;
const int M2Channel = 1;
const int M3Channel = 2;

//Variables
String Command;
String Value;
String inData;
int Error;
int mappedVal;

//Servo Setup for Direct Mode
Servo XServo;
Servo YServo;
Servo ZServo;

void setup()
{
    //PCA 9685 Driver Setup
    Wire.begin();
    Wire.setClock(400000);
    driver.resetDevices();
    driver.init(B000000);
    driver.setPWMFrequency(50);

    //Serial Setup
    Serial.begin(57600);

    //Direct Setup
    XServo.attach(M1Pin);
    YServo.attach(M2Pin);
    ZServo.attach(M3Pin);
}

void loop()
{

    while (Serial.available() > 0)
    {

        Command = Serial.readStringUntil(',');
        Value = Serial.readStringUntil('\n');
        Serial.read();

        if (Command == "X")
        {
            if (isUsingDriver)
            {
                mappedVal = map(Value.toInt(), 0, 180, -90, 90);
                driver.setChannelPWM(M1Channel, pwmServo.pwmForAngle(mappedVal));
            }
            else
            {
                XServo.write(Value.toInt());
            }
        }
        else if (Command == "Y")
        {
            if (isUsingDriver)
            {
                mappedVal = map(Value.toInt(), 0, 180, -90, 90);
                driver.setChannelPWM(M2Channel, pwmServo.pwmForAngle(mappedVal));
            }
            else
            {
                YServo.write(Value.toInt());
            }
        }
        else if (Command == "Z")
        {
            if (isUsingDriver)
            {
                mappedVal = map(Value.toInt(), 0, 180, -90, 90);
                driver.setChannelPWM(M3Channel, pwmServo.pwmForAngle(mappedVal));
            }
            else
            {
                ZServo.write(Value.toInt());
            }
        }
        else
        {
            Serial.println("Not Found");
        }
    }
}
