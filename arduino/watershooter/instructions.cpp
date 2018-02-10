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
	motor.setVelocity(input.read<float>());
}

void GET_MOTOR_VELOCITY(SerialTalks &inst, Deserializer &input, Serializer &output){
	output.write<int>(motor.getVelocity());
}

void GET_WATER_COLOR(SerialTalks &inst, Deserializer &input, Serializer &output){
	int red = waterSensor.getRed();
	int green = waterSensor.getGreen();
	int blue = waterSensor.getBlue();

	output.write<int>(red, green, blue);
}
