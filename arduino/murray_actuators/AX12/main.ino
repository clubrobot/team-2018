#include <Arduino.h>
#include "../../common/SoftwareSerial.h"

#include "PIN.h"
#include "instructions.h"

#include "../../common/SerialTalks.h"
#include "../../common/ShiftRegister.h"
#include "../../common/AX12.h"
#include "../../common/RobotArm.h"

#define USE_SHIFTREG 1

ShiftRegister shift;

SoftwareSerial SoftSerial(RX_AX12,TX_AX12);

AX12 servoax;

RobotArm arm(0.0, 30.0, 10.0, 90.0, 50);

void setup()
{
	// //Starting SerialTalks
	Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);

    // //bind set pos FUNC
    talks.bind(BEGIN_OPCODE,BEGIN);

    talks.bind(SET_POS_OPCODE,SET_POSITION);

    talks.bind(SET_X_OPCODE,SET_X);
    talks.bind(SET_Y_OPCODE,SET_Y);
    talks.bind(SET_Z_OPCODE,SET_Z);
    talks.bind(SET_THETA_OPCODE,SET_THETA);
    talks.bind(SET_SPEED_OPCODE,SET_SPEED);

    talks.bind(GET_POS_OPCODE,GET_POSITION);
    talks.bind(GET_POS_THEO_OPCODE,GET_POSITION_THEO);

    //initialise ShiftRegister
    shift.attach(LATCHPIN,CLOCKPIN,DATAPIN);
   
   	//initialise AX14
    servoax.SerialBegin(9600, RX_AX12, TX_AX12, AX12_DATA_CONTROL);

	arm.attach(2,1,3);
	arm.begin();

    arm.set_angles(150.0, 150.0, 150.0);
}

void loop()
{
	talks.execute();
}