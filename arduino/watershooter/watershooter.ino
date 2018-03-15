#include <Arduino.h>
#include <Servo.h>
//#include <Wire.h>
#include "PIN.h"
#include "instructions.h"
#include "../common/BrushlessMotor.h"
#include "../common/SerialTalks.h"
#include "../common/Adafruit_TCS34725.h"
#include "../common/Wire.h"


BrushlessMotor motor;
Servo indoor;
Servo outdoor;
Servo trash;
Adafruit_TCS34725 waterSensor = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);

#define DOOR_CLOSED 90
#define TRASH_CLOSED 25

void resetVelocity();

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
	talks.bind(_SET_LED_OFF_OPCODE, SET_LED_OFF);
	talks.bind(_SET_LED_ON_OPCODE, SET_LED_ON);
	talks.bind(_FORCE_PULSEWIDTH, FORCE_PULSEWIDTH);


	pinMode(SERVO1, OUTPUT);
    pinMode(SERVO2, OUTPUT);
	pinMode(SERVO3, OUTPUT);
	pinMode(SERVO4, OUTPUT);
	pinMode(SERVO5, OUTPUT);
	pinMode(SERVO6, OUTPUT);
	pinMode(BRUSHLESS, OUTPUT);
	pinMode(SWITCH1, INPUT_PULLUP);

	attachInterrupt(digitalPinToInterrupt(SWITCH1), resetVelocity, FALLING);
	
	motor.attach(BRUSHLESS);
	motor.setVelocity(MIN_VELOCITY);
	motor.enableMotor();

	indoor.attach(SERVO2);
	outdoor.attach(SERVO3);
	trash.attach(SERVO1);

	trash.write(TRASH_CLOSED);
	outdoor.write(DOOR_CLOSED);
	indoor.write(DOOR_CLOSED);
	waterSensor.begin();
}

void resetVelocity(){
	motor.enableStartup();
}

void loop(){
    talks.execute();
	motor.updateStartup();
}




