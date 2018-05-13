#include <Arduino.h>
#include "../common/RobotArm.h"
#include "../common/SerialTalks.h"

IK ik;
void setup()
{
	Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
}

void loop()
{
	talks.execute();

	double x = 2.0;
	double y = 10.0;
	double z = 5.0;

	Serial.println("Lets do some tests. First move to ():");
	double a1,a2,a3;

	ik.solve_angles(x, y, z, &a1, &a2, &a3);

	Serial.print("X: ");
	Serial.println(x);

	Serial.print("Y: ");
	Serial.println(y);

	Serial.print("Z: ");
	Serial.println(z);

	Serial.print("A1:");
	Serial.println(ik.convert_deg(a1));

	Serial.print("A2:");
	Serial.println(ik.convert_deg(a2));

	Serial.print("A3:");
	Serial.println(a3);

	delay(10000);
}