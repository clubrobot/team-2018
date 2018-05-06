#include <Arduino.h>
#include <Servo.h>
#include "../../common/SoftwareSerial.h"
#include "../../common/SerialTalks.h"
#include "../../common/ShiftRegister.h"
#include "../../common/ShiftRegAX12.h"
#include "../../common/StepByStepMotor.h"
#include "../../common/RobotArm.h"
#include "PIN.h"
#include "instructions.h"

#define USE_SHIFTREG 1

//#include "../../common/StepByStepMotor.h"
SoftwareSerial SoftSerial(RX_AX12,TX_AX12);

ShiftRegister shift;

StepByStepMotor motor;

ShiftRegAX12 servoax;

//            X |  Y  |  Z  | Th | SPEED
RobotArm arm(15.0, 15.0, 10.0, 0.0, 100);

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

    motor.attach(STEP_PAP, DIR_PAP, ENABLE_PAP, RST_PAP, SLEEP_PAP);

    ShiftRegAX12::SerialBegin(9600, RX_AX12, TX_AX12, AX12_DATA_CONTROL);

}

void loop()
{
	talks.execute();

}