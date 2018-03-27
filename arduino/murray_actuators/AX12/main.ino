#include <Arduino.h>

#include "PIN.h"
#include "instructions.h"

#include "../../common/SerialTalks.h"
#include "../../common/ShiftRegister.h"

ShiftRegister reg;

void setup()
{
	Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
}

void loop()
{
	talks.execute();
}