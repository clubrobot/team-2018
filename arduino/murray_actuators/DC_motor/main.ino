#include <Arduino.h>

#include "PIN.h"
#include "instructions.h"

#include "../../common/SerialTalks.h"
#include "../../common/ShiftRegDCMotor.h"
#include "../../common/ShiftRegister.h"

ShiftRegDCMotorsDriver driver;
ShiftRegDCMotor motor_1;
ShiftRegDCMotor motor_2;

ShiftRegister reg;

void setup()
{
	Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);

    reg.attach(LATCHPIN, CLOCKPIN, DATAPIN);

	driver.attach(RST_DRV, 999);
	driver.reset();

  	motor_1.attach(EN_MOTOR_1, PWM_MOTOR_1, SELECT_MOTOR1);
  	motor_2.attach(EN_MOTOR_2, PWM_MOTOR_2, SELECT_MOTOR2);
}

void loop()
{
	talks.execute();
}
