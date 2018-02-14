#include "instructions.h"
#include <Servo.h>
#include "PIN.h"
#include "../common/SerialTalks.h"
#include "../common/BrushlessMotor.h"
#include "../common/ColorSensor.h"

extern BrushlessMotor motor;
extern Servo indoor;
extern Servo outdoor;
extern Servo trash;
extern ColorSensor waterSensor;


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

void SET_MOTOR_VELOCITY(SerialTalks &inst, Deserializer &input, Serializer &output){
	motor.setVelocity(input.read<int>());
}

void GET_MOTOR_VELOCITY(SerialTalks &inst, Deserializer &input, Serializer &output){
	output.write<int>(motor.getVelocity());
}

void GET_WATER_COLOR(SerialTalks &inst, Deserializer &input, Serializer &output){
	int red = 0;//waterSensor.getRed();
	int green = 0;//waterSensor.getGreen();
	int blue = 0;//waterSensor.getBlue();

	output.write<int>(red);
	output.write<int>(green);
	output.write<int>(blue);
}

void SET_MOTOR_PULSEWIDTH(SerialTalks &inst, Deserializer &input, Serializer &output) {
	motor.setPulsewidth(input.read<int>());
}

void GET_MOTOR_PULSEWIDTH(SerialTalks &inst, Deserializer &input, Serializer &output) {
	int pulsewidth = motor.readMicroseconds();
	output.write<int>(pulsewidth);
}