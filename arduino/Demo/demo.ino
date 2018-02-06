#include <Arduino.h>
#include <Servo.h>
#include "PIN.h"
#include "instructions.h"
#include "../common/BrushlessMotor.h"
#include "../common/SerialTalks.h"


BrushlessMotor motor;
Servo inDoor;
Servo outDoor;
Servo trash;


void setup(){
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
    talks.bind(_SET_MOTOR_VELOCITY_OPCODE, SET_MOTOR_VELOCITY);
	talks.bind(_WRITE_INDOOR_OPCODE, WRITE_INDOOR);
	talks.bind(_WRITE_OUTDOOR_OPCODE, WRITE_OUTDOOR);
	talks.bind(_WRITE_TRASH_OPCODE, WRITE_TRASH);

	pinMode(SERVO1, OUTPUT);
    pinMode(SERVO2, OUTPUT);
	pinMode(SERVO3, OUTPUT);

	motor.attach(SERVO4);
	motor.setVelocity(MIN_VELOCITY);

	inDoor.attach(SERVO2);
	outDoor.attach(SERVO3);
	trash.attach(SERVO1);
    // Miscellanous
	TCCR2B = (TCCR2B & 0b11111000) | 1; // Set Timer2 frequency to 16MHz instead of 250kHz
}

void loop(){
     talks.execute();
}




