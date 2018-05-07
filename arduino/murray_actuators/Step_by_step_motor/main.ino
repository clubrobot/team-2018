#include <Arduino.h>
#include "PIN.h"
#include "../../common/ShiftRegister.h"
#include "../../common/StepByStepMotor.h"

ShiftRegister shift;
StepByStepMotor motor;

void setup()
{
	shift.attach(LATCHPIN,CLOCKPIN,DATAPIN);

	motor.attach(STEP_PAP, DIR_PAP, ENABLE_PAP, RST_PAP, SLEEP_PAP);
	motor.begin();


	motor.set_position(150);

	delay(200);

	motor.set_position(0);

	delay(200);

	motor.set_position(150);

	delay(200);

	motor.set_position(0);

	delay(200);

	motor.set_position(150);

	delay(200);

	motor.set_position(0);

	


	
}
void loop()
{
	//motor.set_position(50);

	//delay(2000);

}