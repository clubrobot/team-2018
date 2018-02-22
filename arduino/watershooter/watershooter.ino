#include <Arduino.h>
#include <Servo.h>
//#include <Wire.h>
#include "PIN.h"
#include "instructions.h"
#include "../common/BrushlessMotor.h"
#include "../common/SerialTalks.h"
//#include "../common/ColorSensor.h"


BrushlessMotor motor;
Servo indoor;
Servo outdoor;
Servo trash;
//ColorSensor waterSensor;

#define DOOR_CLOSED 90
#define TRASH_CLOSED 25


void setup(){
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
	talks.bind(_GET_INDOOR_OPCODE, GET_INDOOR);
	talks.bind(_WRITE_INDOOR_OPCODE, WRITE_INDOOR);
	talks.bind(_GET_OUTDOOR_OPCODE, GET_OUTDOOR);
	talks.bind(_WRITE_OUTDOOR_OPCODE, WRITE_OUTDOOR);
	talks.bind(_GET_TRASH_OPCODE, GET_TRASH);
	talks.bind(_WRITE_TRASH_OPCODE, WRITE_TRASH);
	talks.bind(_GET_MOTOR_VELOCITY_OPCODE, GET_MOTOR_VELOCITY);
    talks.bind(_SET_MOTOR_VELOCITY_OPCODE, SET_MOTOR_VELOCITY);
	talks.bind(_GET_WATER_COLOR_OPCODE, GET_WATER_COLOR);
	talks.bind(_SET_MOTOR_PULSEWIDTH_OPCODE, SET_MOTOR_PULSEWIDTH);
	talks.bind(_GET_MOTOR_PULSEWIDTH_OPCODE, GET_MOTOR_PULSEWIDTH);

	pinMode(SERVO1, OUTPUT);
    pinMode(SERVO2, OUTPUT);
	pinMode(SERVO3, OUTPUT);
	pinMode(SERVO4, OUTPUT);
	pinMode(SWITCH1 INPUT_PULLUP);

	attachInterrupt(digitalPinToInterrupt(SWITCH1), setupESC, CHANGE);
	
	motor.attach(SERVO4);
	motor.enable();
	motor.setVelocity(MIN_VELOCITY);

	indoor.attach(SERVO2);
	outdoor.attach(SERVO3);
	trash.attach(SERVO1);

	trash.write(TRASH_CLOSED);
	outdoor.write(DOOR_CLOSED);
	indoor.write(DOOR_CLOSED);

	//waterSensor.setup();
}

void setupESC(){
	if(digitalRead(SWITCH1)==HIGH){
		motor.setupRise(true);
		motor.enableSetup();
	} else {
		motor.setupFall();
	}
}

void loop(){
     talks.execute();
	 motor.updateSetup();
}




