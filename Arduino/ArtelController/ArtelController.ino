#include <AccelStepper.h>
#include "Kinematics.h"
//#include <iostream>
#include <string.h>
#include <math.h>
//#include <map.h>

#define ROBOT_f 150.0  // base radius
#define ROBOT_rf 150.0 // shoulder length
#define ROBOT_re 480.0 // arm length
#define ROBOT_e 45.0   // end effector radius

DeltaKinematics ArtelK(ROBOT_rf, ROBOT_re, ROBOT_f, ROBOT_e);

class IO
{
public:
    // Stepper Motors
    const int motorAStep = 3;
    const int motorADir = 2;
    const int motorBStep = 5;
    const int motorBDir = 4;
    const int motorCStep = 7;
    const int motorCDir = 6;

    // Proximity Sensor Pins
    const int sensorA = 14;
    const int sensorB = 16;
    const int sensorC = 15;

    // Buttons
    const int estop = 17;

    AccelStepper motorA;
    AccelStepper motorB;
    AccelStepper motorC;

    void setup()
    {
        Serial.begin(9600);

        motorA = AccelStepper(1, motorAStep, motorADir);
        motorB = AccelStepper(1, motorBStep, motorBDir);
        motorC = AccelStepper(1, motorCStep, motorCDir);

        pinMode(motorADir, OUTPUT);
        pinMode(motorAStep, OUTPUT);

        pinMode(motorBDir, OUTPUT);
        pinMode(motorBStep, OUTPUT);

        pinMode(motorCDir, OUTPUT);
        pinMode(motorCStep, OUTPUT);

        pinMode(sensorA, INPUT);
        pinMode(sensorB, INPUT);
        pinMode(sensorC, INPUT);

        pinMode(estop, INPUT);
    }
};

struct Pos
{
    float x;
    float y;
    float z;
};

struct Angle
{
    float a = 0;
    float b = 0;
    float c = 0;
};

class Inputs
{
private:
    IO io;
public:
    bool getStopToggle()
    {
        if (analogRead(io.estop) == 1023)
        {
            return true;
        }
        return false;
    }

    bool getProximitySensor(int id)
    {
        switch (id)
        {
        case 1:
            return analogRead(io.sensorA) == 0;
            break;
        case 2:
            return analogRead(io.sensorB) == 1023;
            break;
        case 3:
            return analogRead(io.sensorC) == 1023;
            break;

        default:
            break;
        }
    }
};

class Motion
{
private:
    const double stepPerRevolution = 3200;
    double resolution;
    IO io;
    Inputs inputs;
    
    bool A_is_home = false;
    bool B_is_home = false;
    bool C_is_home = false;

    int _maxSpeed;
    Angle angle;
    Angle steps;
    int _maxAcceleration;

public:
    Pos currentPosition;

    void init(int maxSpeed, int maxAcceleration)
    {
        io.motorA.setMaxSpeed(maxSpeed);
        io.motorA.setAcceleration(maxAcceleration);

        io.motorB.setMaxSpeed(maxSpeed);
        io.motorB.setAcceleration(maxAcceleration);

        io.motorC.setMaxSpeed(maxSpeed);
        io.motorC.setAcceleration(maxAcceleration);

        _maxSpeed = maxSpeed;
        _maxAcceleration = maxAcceleration;

        resolution = 360 / stepPerRevolution;
    }

    void move(AccelStepper &motor, float deg)
    {   
        motor.moveTo((long)deg / resolution);
    }

    void moveSteps(AccelStepper &motor, int step)
    {
        motor.moveTo((long)step / resolution);
    }

    void travel(float x, float y, float z)
    {
        ArtelK.inverse(x, y, z);
        move(io.motorA, ArtelK.a);
        move(io.motorB, ArtelK.b);
        move(io.motorC, ArtelK.c);

        io.motorA.run();
        io.motorB.run();
        io.motorC.run();

        currentPosition.x = x;
        currentPosition.y = y;
        currentPosition.z = z;
    }

    void ptp(float x, float y, float z, float feed = 1)
    {
        float x_d, y_d, z_d;
        float easing_t;

        int t = 0;

        while (t < 100)
        {
            if (!io.motorA.isRunning() && !io.motorB.isRunning() && !io.motorC.isRunning())
            {
                easing_t = easeInOutQuint(t);
                x_d = currentPosition.x + ((x - currentPosition.x) * easing_t);
                y_d = currentPosition.y + ((y - currentPosition.y) * easing_t);
                z_d = currentPosition.z + ((z - currentPosition.z) * easing_t);

                ArtelK.inverse(x, y, z);
                move(io.motorA, ArtelK.a);
                move(io.motorB, ArtelK.b);
                move(io.motorC, ArtelK.c);
                io.motorA.run();
                io.motorB.run();
                io.motorC.run();

                currentPosition.x = x;
                currentPosition.y = y;
                currentPosition.z = z;
                t++;
            }
        }
    }

    void homeAll(int feed)
    {
        for (int i = 0; i < 6400; i += 100)
        {
            if (!A_is_home)
            {
                io.motorA.moveTo(i);
            }
            if (!B_is_home)
            {
                io.motorB.moveTo(i);
            }
            if (!C_is_home)
            {
                io.motorC.moveTo(i);
            }

            if (inputs.getProximitySensor(1))
            {
                A_is_home = true;
            }
            if (inputs.getProximitySensor(2))
            {
                B_is_home = true;
            }
            if (inputs.getProximitySensor(3))
            {
                C_is_home = true;
            }
            while (io.motorA.distanceToGo() != 0 || io.motorB.distanceToGo() != 0 || io.motorC.distanceToGo() != 0)
            {
                io.motorA.run();
                io.motorB.run();
                io.motorC.run();
            }
        }
    }

    double easeInSine(double t)
    {
        return sin(1.5707963 * t);
    }

    double easeOutSine(double t)
    {
        return 1 + sin(1.5707963 * (--t));
    }

    double easeInOutSine(double t)
    {
        return 0.5 * (1 + sin(3.1415926 * (t - 0.5)));
    }

    double easeInQuad(double t)
    {
        return t * t;
    }

    double easeOutQuad(double t)
    {
        return t * (2 - t);
    }

    double easeInOutQuad(double t)
    {
        return t < 0.5 ? 2 * t * t : t * (4 - 2 * t) - 1;
    }

    double easeInCubic(double t)
    {
        return t * t * t;
    }

    double easeOutCubic(double t)
    {
        return 1 + (--t) * t * t;
    }

    double easeInOutCubic(double t)
    {
        return t < 0.5 ? 4 * t * t * t : 1 + (--t) * (2 * (--t)) * (2 * t);
    }

    double easeInQuart(double t)
    {
        t *= t;
        return t * t;
    }

    double easeOutQuart(double t)
    {
        t = (--t) * t;
        return 1 - t * t;
    }

    double easeInOutQuart(double t)
    {
        if (t < 0.5)
        {
            t *= t;
            return 8 * t * t;
        }
        else
        {
            t = (--t) * t;
            return 1 - 8 * t * t;
        }
    }

    double easeInQuint(double t)
    {
        double t2 = t * t;
        return t * t2 * t2;
    }

    double easeOutQuint(double t)
    {
        double t2 = (--t) * t;
        return 1 + t * t2 * t2;
    }

    double easeInOutQuint(double t)
    {
        double t2;
        if (t < 0.5)
        {
            t2 = t * t;
            return 16 * t * t2 * t2;
        }
        else
        {
            t2 = (--t) * t;
            return 1 + 16 * t * t2 * t2;
        }
    }

    double easeInExpo(double t)
    {
        return (pow(2, 8 * t) - 1) / 255;
    }

    double easeOutExpo(double t)
    {
        return 1 - pow(2, -8 * t);
    }

    double easeInOutExpo(double t)
    {
        if (t < 0.5)
        {
            return (pow(2, 16 * t) - 1) / 510;
        }
        else
        {
            return 1 - 0.5 * pow(2, -16 * (t - 0.5));
        }
    }

    double easeInCirc(double t)
    {
        return 1 - sqrt(1 - t);
    }

    double easeOutCirc(double t)
    {
        return sqrt(t);
    }

    double easeInOutCirc(double t)
    {
        if (t < 0.5)
        {
            return (1 - sqrt(1 - 2 * t)) * 0.5;
        }
        else
        {
            return (1 + sqrt(2 * t - 1)) * 0.5;
        }
    }

    double easeInBack(double t)
    {
        return t * t * (2.70158 * t - 1.70158);
    }

    double easeOutBack(double t)
    {
        return 1 + (--t) * t * (2.70158 * t + 1.70158);
    }

    double easeInOutBack(double t)
    {
        if (t < 0.5)
        {
            return t * t * (7 * t - 2.5) * 2;
        }
        else
        {
            return 1 + (--t) * t * 2 * (7 * t + 2.5);
        }
    }
};

class Artel
{
    Inputs inputs;

private:
    const float _version = 1.2;

public:
    bool is_running()
    {
        if (inputs.getStopToggle())
        {
            return false;
        }
        return true;
    }

    bool is_failure()
    {
    }

    void log()
    {
    }
};

class GCode
{
public:
    Motion motion;
    /* void executeLine(std::string line)
     {
         int number;
         char letter;
         std::istringstream iss(line);

         char result = ms.Match("([Gg]0?[01]) *(([XxYyZz]) *(-?\d+.?\d*)) *(([XxYyZz]) *(-?\d+.?\d*))? *(([XxYyZz]) *(-?\d+.?\d*))?");
         if (result == REGEXP_MATCHED)
         {
             char buf[100]; // large enough to hold expected string

             Serial.print("Captures: ");
             Serial.println(ms.level);

             for (int j = 0; j < ms.level; j++)
             {
                 Serial.print("Capture number: ");
                 Serial.println(j, DEC);
                 Serial.print("Text: '");
                 Serial.print(ms.GetCapture(buf, j));
                 Serial.println("'");

             }
         }
         else if (result == REGEXP_NOMATCH)
         {
         }
         else
         {
         }

 //        for (std::string code; iss >> code;)
 //        {
 //            letter = code[0];
 //            number = (code.substr(1, code.length())).toInt();
 //        }
     }
     */
};

Motion motion;
Artel artel;
Inputs inputs;
IO io;

void setup()
{
    io.setup();
    motion.init(6000, 6000);
}

void loop()
{
    motion.homeAll(1);
    io.motorA.currentPosition
}
