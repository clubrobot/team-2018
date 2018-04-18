#include <Arduino.h>
#include "../../common/SoftwareSerial.h"

#include "PIN.h"
#include "instructions.h"

#include "../../common/SerialTalks.h"
#include "../../common/ShiftRegister.h"
#include "../../common/AX12.h"

#define USE_SHIFTREG 1

ShiftRegister shift;

SoftwareSerial SoftSerial(RX_AX12,TX_AX12);

AX12 servoax;

void setup()
{
	Serial.begin(SERIALTALKS_BAUDRATE);
    //talks.begin(Serial);
    shift.attach(LATCHPIN,CLOCKPIN,DATAPIN);
   
    servoax.SerialBegin(9600, RX_AX12, TX_AX12, AX12_DATA_CONTROL);

    servoax.attach(254);
	//servoax.setSRL(1); // Respond only to READ_DATA instructions
	 //servoax.setLEDAlarm(32); // max torque only
	 //servoax.setShutdownAlarm(32); // max torque only
	 //servoax.setMaxTorque(1023);
	//servoax.setEndlessMode(OFF);
	//servoax.hold(OFF);


}

void loop()
{
	//talks.execute();
	//servoax.setMaxTorqueRAM(1023);
	servoax.move(150.0);

	//Serial.println(servoax.ping());

	delay(1000);
}