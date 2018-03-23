#include "instructions.h"
#include <Servo.h>
#include "PIN.h"
#include "../common/SerialTalks.h"
#include "../common/BrushlessMotor.h"
#include "../common/Adafruit_TCS34725.h"
#include "../common/Wire.h"

extern BrushlessMotor motor;
extern Servo indoor;
extern Servo outdoor;
extern Servo trash;
extern Servo shakerHorizontal;
extern Servo shakerVertical;
extern Adafruit_TCS34725 waterSensor;
uint16_t red, green, blue, clear;


void WRITE_INDOOR(SerialTalks &inst, Deserializer &input, Serializer &output){
	indoor.write(input.read<int>());
}

void GET_INDOOR(SerialTalks &inst, Deserializer &input, Serializer &output){
	output.write<int>(indoor.read());
}

void WRITE_OUTDOOR(SerialTalks &inst, Deserializer &input, Serializer &output){
	outdoor.write(input.read<int>());
}

void GET_OUTDOOR(SerialTalks &inst, Deserializer &input, Serializer &output){
	output.write<int>(outdoor.read());
}

void WRITE_TRASH(SerialTalks &inst, Deserializer &input, Serializer &output){
	trash.write(input.read<int>());
}

void GET_TRASH(SerialTalks &inst, Deserializer &input, Serializer &output){
	output.write<int>(trash.read());
}


void WRITE_SHAKER_VERTICAL(SerialTalks &inst, Deserializer &input, Serializer &output){
	shakerVertical.write(input.read<int>());
}

void GET_SHAKER_VERTICAL(SerialTalks &inst, Deserializer &input, Serializer &output){
	output.write<int>(shakerVertical.read());
}

void WRITE_SHAKER_HORIZONTAL(SerialTalks &inst, Deserializer &input, Serializer &output){
	shakerHorizontal.write(input.read<int>());
}

void GET_SHAKER_HORIZONTAL(SerialTalks &inst, Deserializer &input, Serializer &output){
	output.write<int>(shakerHorizontal.read());
}

void SET_MOTOR_VELOCITY(SerialTalks &inst, Deserializer &input, Serializer &output){
	output.write<int>(motor.setVelocity(input.read<int>()));
}

void GET_MOTOR_VELOCITY(SerialTalks &inst, Deserializer &input, Serializer &output){
	output.write<int>(motor.getVelocity());
}

void GET_WATER_COLOR(SerialTalks &inst, Deserializer &input, Serializer &output){
	waterSensor.setInterrupt(false);
    waterSensor.getRawData(&red, &green, &blue, &clear);
	output.write<int>(red);
	output.write<int>(green);
	output.write<int>(blue);
}

void SET_MOTOR_PULSEWIDTH(SerialTalks &inst, Deserializer &input, Serializer &output) {
	output.write<int>(motor.setPulsewidth(input.read<int>()));
}

void GET_MOTOR_PULSEWIDTH(SerialTalks &inst, Deserializer &input, Serializer &output) {
	int pulsewidth = motor.readMicroseconds();
	output.write<int>(pulsewidth);
}

void FORCE_PULSEWIDTH(SerialTalks &inst, Deserializer &input, Serializer &output){
	motor.forcePulsewidth(input.read<int>());
}

void SET_LED_ON(SerialTalks& inst, Deserializer& input, Serializer& output){
	digitalWrite(LED, HIGH);
}

void SET_LED_OFF(SerialTalks& inst, Deserializer& input, Serializer& output){
	digitalWrite(LED, LOW);
}