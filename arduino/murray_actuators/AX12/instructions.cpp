#include "instructions.h"
#include "../../common/RobotArm.h"

extern RobotArm arm;

void BEGIN(SerialTalks &inst, Deserializer &input, Serializer &output)
{
	arm.begin();
}

void SET_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output)
{
	float x = input.read<float>();
	float y = input.read<float>();
	float z = input.read<float>();
	float d = input.read<float>();

	arm.ReachPosition(x,y,z,d);
}

void SET_X(SerialTalks &inst, Deserializer &input, Serializer &output)
{
	arm.set_x(input.read<float>());
}

void SET_Y(SerialTalks &inst, Deserializer &input, Serializer &output)
{
	arm.set_y(input.read<float>());
}

void SET_Z(SerialTalks &inst, Deserializer &input, Serializer &output)
{
	arm.set_z(input.read<float>());
}

void SET_THETA(SerialTalks &inst, Deserializer &input, Serializer &output)
{
	arm.set_theta(input.read<float>());
}

void SET_SPEED(SerialTalks &inst, Deserializer &input, Serializer &output)
{
	arm.set_speed(input.read<float>());
}

void GET_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output)
{
	output.write<float>(arm.get_A2());

	output.write<float>(arm.get_A1());

	output.write<float>(arm.get_A3());
}

void GET_POSITION_THEO(SerialTalks &inst, Deserializer &input, Serializer &output)
{
	output.write<float>(arm.get_A2theo());

	output.write<float>(arm.get_A1theo());

	output.write<float>(arm.get_A3theo());
}


