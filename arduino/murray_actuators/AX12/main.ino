#include <Arduino.h>
#include <Servo.h>
#include "../../common/SoftwareSerial.h"
#include "../../common/SerialTalks.h"
#include "../../common/ShiftRegister.h"
#include "../../common/ShiftRegAX12.h"
#include "../../common/RobotArm.h"
#include "PIN.h"
#include "instructions.h"

#define USE_SHIFTREG 1

//#include "../../common/StepByStepMotor.h"
SoftwareSerial SoftSerial(RX_AX12,TX_AX12);

ShiftRegister shift;

ShiftRegAX12 servoax;
//            X |  Y  |  Z  | Th | SPEED
RobotArm arm(0.0, 30.0, 10.0, 90.0, 1000);

void setup()
{
	// //Starting SerialTalks
	Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);

    /*****************bind set pos FUNC*****************/
    talks.bind(BEGIN_OPCODE,BEGIN);

    talks.bind(SET_POS_OPCODE,SET_POSITION);

    talks.bind(SET_X_OPCODE,SET_X);
    talks.bind(SET_Y_OPCODE,SET_Y);
    talks.bind(SET_Z_OPCODE,SET_Z);
    talks.bind(SET_THETA_OPCODE,SET_THETA);
    talks.bind(SET_SPEED_OPCODE,SET_SPEED);

    talks.bind(GET_POS_OPCODE,GET_POSITION);
    talks.bind(GET_POS_THEO_OPCODE,GET_POSITION_THEO);

    talks.bind(OPEN_GRIPPER_OPCODE,OPEN_GRIPPER);
    talks.bind(CLOSE_GRIPPER_OPCODE,CLOSE_GRIPPER);
    /***************************************************/

    //initialise ShiftRegister
    shift.attach(LATCHPIN,CLOCKPIN,DATAPIN);

    ShiftRegAX12::SerialBegin(9600, RX_AX12, TX_AX12, AX12_DATA_CONTROL);
    
    //arm.set_angles(150.0, 150.0, 150.0);

    arm.attach(2,1,3,SERVO1);
    
    arm.begin();
}

void loop()
{
	talks.execute();
}