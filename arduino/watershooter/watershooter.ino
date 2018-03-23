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
Servo trashUnloader;
Servo shakerHorizontal;
Servo shakerVertical;

Adafruit_TCS34725 waterSensor = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);

#define OUTDOOR_DOOR_CLOSED 90
#define INDOOR_DOOR_CLOSED 20
#define TRASH_CLOSED 128
#define SHAKER_SIDE_HORIZONTAL 35
#define SHAKER_SIDE_VERTICAL 35


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

	talks.bind(_GET_SHAKER_HORIZONTAL_OPCODE, GET_SHAKER_HORIZONTAL);
	talks.bind(_WRITE_SHAKER_HORIZONTAL_OPCODE, WRITE_SHAKER_HORIZONTAL);

	talks.bind(_GET_SHAKER_VERTICAL_OPCODE, GET_SHAKER_VERTICAL);
	talks.bind(_WRITE_SHAKER_VERTICAL_OPCODE, WRITE_SHAKER_VERTICAL);

	talks.bind(_GET_MOTOR_VELOCITY_OPCODE, GET_MOTOR_VELOCITY);
    talks.bind(_SET_MOTOR_VELOCITY_OPCODE, SET_MOTOR_VELOCITY);
	talks.bind(_GET_WATER_COLOR_OPCODE, GET_WATER_COLOR);
	talks.bind(_SET_MOTOR_PULSEWIDTH_OPCODE, SET_MOTOR_PULSEWIDTH);
	talks.bind(_GET_MOTOR_PULSEWIDTH_OPCODE, GET_MOTOR_PULSEWIDTH);
	talks.bind(_SET_LED_OFF_OPCODE, SET_LED_OFF);
	talks.bind(_SET_LED_ON_OPCODE, SET_LED_ON);
	talks.bind(_FORCE_PULSEWIDTH_OPCODE, FORCE_PULSEWIDTH);


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

	indoor.attach(SERVO1);
	trashUnloader.attach(SERVO4);
	shakerHorizontal.attach(SERVO5);
	shakerVertical.attach(SERVO6);
	outdoor.attach(SERVO2);
	trash.attach(SERVO3);

	trash.write(TRASH_CLOSED);
	outdoor.write(OUTDOOR_DOOR_CLOSED);
	indoor.write(INDOOR_DOOR_CLOSED);
	shakerHorizontal.write(SHAKER_SIDE_HORIZONTAL);
	shakerVertical.write(SHAKER_SIDE_VERTICAL);
	waterSensor.begin();
}

void resetVelocity(){
	motor.enableStartup();
}

void loop(){
    talks.execute();
	motor.updateStartup();
}




