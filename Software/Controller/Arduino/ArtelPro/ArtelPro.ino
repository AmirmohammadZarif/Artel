#include <DeltaKinematics.h>
#include <AccelStepper.h>
#include <string.h>
#include <math.h>

#define ROBOT_f 150.0  // base radius
#define ROBOT_rf 150.0 // shoulder length
#define ROBOT_re 480.0 // arm length
#define ROBOT_e 45.0   // end effector radius

DeltaKinematics ArtelK(150, 480, 45, 150);

// Create a new instance of the AccelStepper class:
AccelStepper stepper1 = AccelStepper(1, 3, 2);
AccelStepper stepper2 = AccelStepper(1, 5, 4);
AccelStepper stepper3 = AccelStepper(1, 7, 6);

int pos_d = 100;

const int estop_pin = 17;

const int sensorA = 14;
const int sensorB = 16;
const int sensorC = 15;

bool A_is_home = false;
bool B_is_home = false;
bool C_is_home = false;

int stepsPerRevolution = 6400;

bool is_home = false;
bool is_running = true;

// ============= Category: Setup
void setup()
{
    pinMode(sensorA, INPUT);
    pinMode(sensorB, INPUT);
    pinMode(sensorC, INPUT);
    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);

    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);

    pinMode(6, OUTPUT);
    pinMode(7, OUTPUT);

    Serial.begin(19200);

    stepper1.setMaxSpeed(6000);
    // stepper1.setAcceleration(7200);

    stepper2.setMaxSpeed(6000);
    // stepper2.setAcceleration(7200);

    stepper3.setMaxSpeed(6000);
    // stepper3.setAcceleration(7200);
}

// ============= Category: Inputs
void check_is_running()
{
    if (analogRead(estop_pin) == 1023)
    {
        is_running = false;
    }
    else
    {
        is_running = true;
    }
}

bool getProximitySensor(int id)
{
    switch (id)
    {
    case 1:
        return analogRead(sensorA) < 10;
        break;
    case 2:
        return analogRead(sensorB) == 1023;
        break;
    case 3:
        return analogRead(sensorC) == 1023;
        break;

    default:
        break;
    }
}

// ============= Category: Motion
double ga;
double gb;
double gc;

double gx = 0;
double gy = 0;
double gz = -400;

double xd;
double yd;
double zd;

double a_off = -70;
double b_off = -70;
double c_off = -70;

double st_A_off = 0;
double st_B_off = 0;
double st_C_off = 0;

// robot geometry
const double e = 35.0;  // end effector
const double f = 150.0; // base
const double re = 480.0;
const double rf = 150.0;

// trigonometric constants
// const double sqrt3 = sqrt(3.0);
// const double pi = 3.141592653;    // PI
// const double sin120 = sqrt3 / 2.0;
// const double cos120 = -0.5;
// const double tan60 = sqrt3;
// const double sin30 = 0.5;
// const double tan30 = 1.0 / sqrt3;

int delta_calcAngleYZ(double x0, double y0, double z0, double &theta)
{
    double y1 = -0.5 * 0.57735 * f; // f/2 * tg 30
    // double y1 = yy1;
    y0 -= 0.5 * 0.57735 * e; // shift center to edge
    // z = a + b*y
    double a = (x0 * x0 + y0 * y0 + z0 * z0 + rf * rf - re * re - y1 * y1) / (2 * z0);
    double b = (y1 - y0) / z0;
    // discriminant
    double d = -(a + b * y1) * (a + b * y1) + rf * (b * b * rf + rf);
    if (d < 0)
        return -1;                                    // non-existing point
    double yj = (y1 - a * b - sqrt(d)) / (b * b + 1); // choosing outer point
    double zj = a + b * yj;
    theta = 180.0 * atan(-zj / (y1 - yj)) / pi + ((yj > y1) ? 180.0 : 0.0);
    if ((theta < -180) || (theta > 180))
        return -1;
    return 0;
}

// inverse kinematics: (x0, y0, z0) -> (theta1, theta2, theta3)
// returned status: 0=OK, negative=non-existing position, the negative number is the number of wrong angles
int inverse(double x0, double y0, double z0, double &theta1, double &theta2, double &theta3)
{
    theta1 = theta2 = theta3 = 0;
    int stat1 = delta_calcAngleYZ(x0, y0, z0, theta1);
    int stat2 = delta_calcAngleYZ(x0 * cos120 + y0 * sin120, y0 * cos120 - x0 * sin120, z0, theta2); // rotate coords to +120 deg
    int stat3 = delta_calcAngleYZ(x0 * cos120 - y0 * sin120, y0 * cos120 + x0 * sin120, z0, theta3); // rotate coords to -120 deg
    return stat1 + stat2 + stat3;
}

double deg2step(int deg)
{
    return deg / (360 / stepsPerRevolution);
}

double step2deg(int step)
{
    return step * (360 / stepsPerRevolution);
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

void homeAll()
{
    int i = 0;
    if (is_home)
    {
        return;
    }
    while (true)
    {
        i += 5;
        if (!A_is_home)
        {
            ga = -i;
            stepper1.moveTo(ga);
        }
        if (!B_is_home)
        {
            gb = i;
            stepper2.moveTo(gb);
        }
        if (!C_is_home)
        {
            gc = -i;
            stepper3.moveTo(gc);
        }

        if (analogRead(sensorA) < 10)
        {
            A_is_home = true;
            st_A_off = ga;
            ga = st_A_off;
        }
        if (analogRead(sensorB) == 1023)
        {
            B_is_home = true;
            st_B_off = gb;
            gb = st_B_off;
        }
        if (analogRead(sensorC) == 1023)
        {
            C_is_home = true;
            st_C_off = gc;
            gc = st_C_off;
        }

        stepper1.run();
        stepper2.run();
        stepper3.run();
        while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0 || stepper3.distanceToGo() != 0)
        {
            stepper1.run();
            stepper2.run();
            stepper3.run();
        }
        if (A_is_home == true && B_is_home == true && C_is_home == true)
        {
            Serial.println("There is no place like home!");
            delay(5000);
            is_home = true;
            break;
        }
    }
}

void moveMotors(int mot1deg, int mot2deg, int mot3deg)
{
    for (int i = 0; i < 500; i += 100)
    {
        stepper1.moveTo(i);

        stepper2.moveTo(-i);

        stepper3.moveTo(i);
        stepper1.run();
        stepper2.run();
        stepper3.run();
    }

    for (int i = 500; i > 0; i -= 100)
    {
        stepper1.moveTo(i);

        stepper2.moveTo(-i);

        stepper3.moveTo(i);
        stepper1.run();
        stepper2.run();
        stepper3.run();
    }
}

// ============= Category: Control
void move(AccelStepper &motor, double deg)
{
    motor.moveTo(deg2step(deg));
}

void moveSteps(AccelStepper &motor, int step)
{
    motor.moveTo(step2deg(step));
}

void p2p(double x, double y, double z)
{
    Serial.println("Lin Operation:");
    double x_d, y_d, z_d;
    double _t;
    Serial.println("Inital");
    Serial.println((String)gx + ' ' + (String)gy + ' ' + (String)gz + ' ');
    delay(5000);
    int t = 1;

    int r = sqrt((pow(x, 2) - pow(gx, 2)) + (pow(y, 2) - pow(gy, 2)) + (pow(z, 2) - pow(gz, 2)));
    r = r / 10;
    while (t <= r)
    {
        _t = (double)t / (double)r;
        x_d = gx + ((x - gx) * _t);
        y_d = gy + ((y - gy) * _t);
        z_d = gz + ((z - gz) * _t);
        Serial.println("Desired: XD, YD, ZD");
        Serial.println(_t);
        Serial.println((String)x_d + ' ' + (String)y_d + ' ' + (String)z_d + ' ');

        ArtelK.inverse(x_d, y_d, z_d);

        ga = ArtelK.a;
        gb = ArtelK.b;
        gc = ArtelK.c;

        stepper1.moveTo(-(double)ga / (double)((double)360 / (double)stepsPerRevolution));
        stepper2.moveTo((double)gb / (double)((double)360 / (double)stepsPerRevolution));
        stepper3.moveTo(-(double)gc / (double)((double)360 / (double)stepsPerRevolution));

        stepper1.runSpeed();
        stepper2.runSpeed();
        stepper3.runSpeed();
        s
        gx = x_d;
        gy = y_d;
        gz = z_d;

        Serial.println("Global Position: GX, GY, GZ");
        Serial.println((String)gx + ' ' + (String)gy + ' ' + (String)gz);

        Serial.println("Step: SA, SB, SC");
        Serial.println((String)stepper1.currentPosition() + ' ' + (String)stepper2.currentPosition() + ' ' + (String)stepper3.currentPosition());

        Serial.println("Steps");
        Serial.println((String) + ' ' + (String)gb + ' ' + (String)gc);
        if (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0 || stepper3.distanceToGo() != 0)
        {

            stepper1.runSpeed();
            stepper2.runSpeed();
            stepper3.runSpeed();
        }
        t++;
    }=
    Serial.println("Lin Finished");
    delay(5000);
}

void loop()
{
    while (true)
    {
        homeAll();

        Serial.println("Dadh");
        // 0, 0, -200
        p2p(100, 100, -450);
    }
    //  ArtelK.inverse(serial.readLine(), y_d, z_d);
}