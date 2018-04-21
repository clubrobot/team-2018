#include <Arduino.h>

#include "PIN.h"
#include "instructions.h"
#include "../../common/DCMotor.h"
#include "../../common/SerialTalks.h"
#include "../../common/ShiftRegister.h"
#define USE_SHIFTREG 1


DCMotorsDriver driver;
DCMotor motor_1;
DCMotor motor_2;

ShiftRegister shift;

void setup()
{
	Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);

    talks.bind(_RESET_DRIVER_OPCODE, RESET_DRIVER);

    talks.bind(_ENABLE_MOTOR1_OPCODE, ENABLE_MOTOR1);
    talks.bind(_ENABLE_MOTOR2_OPCODE, ENABLE_MOTOR2);

    talks.bind(_DISABLE_MOTOR1_OPCODE, DISABLE_MOTOR1);
    talks.bind(_DISABLE_MOTOR2_OPCODE, DISABLE_MOTOR2);

    talks.bind(_IS_ENABLED1_OPCODE, IS_ENABLED1);
    talks.bind(_IS_ENABLED2_OPCODE, IS_ENABLED1);

    talks.bind(_SET_VELOCITY1_OPCODE, SET_VELOCITY1);
    talks.bind(_SET_VELOCITY2_OPCODE, SET_VELOCITY1);

    shift.attach(LATCHPIN, CLOCKPIN, DATAPIN);

	driver.attach(RST_DRV, 999);
	driver.reset();

  	motor_1.attach(EN_MOTOR_1, PWM_MOTOR_1, SELECT_MOTOR1);
  	motor_2.attach(EN_MOTOR_2, PWM_MOTOR_2, SELECT_MOTOR2);
}

void loop()
{
	talks.execute();
}
