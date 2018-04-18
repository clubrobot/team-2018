#include <Arduino.h>
#include "PIN.h"
#include "../../common/ShiftRegister.h"

ShiftRegister shift;

void setup()
{
	shift.attach(LATCHPIN,CLOCKPIN,DATAPIN);
	shift.SetLow(ENABLE_PAP);
	shift.SetHigh(DIR_PAP);
	shift.SetHigh(SLEEP_PAP);
	shift.SetHigh(RST_PAP);
	pinMode(STEP_PAP, OUTPUT);
	delay(10);
}
void loop()
{
	 digitalWrite(STEP_PAP, LOW);
     delayMicroseconds(50);
     digitalWrite(STEP_PAP, HIGH); 
     delayMicroseconds(50);
}