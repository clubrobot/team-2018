#ifndef __INSTRUCTIONS_H__
#define __INSTRUCTIONS_H__
#include "../../common/SerialTalks.h"
#include "../../common/AX12.h"


#define BEGIN_OPCODE 0X11
#define SET_POS_OPCODE 0X12

#define SET_X_OPCODE 0X13
#define SET_Y_OPCODE 0X14
#define SET_Z_OPCODE 0X15

#define GET_POS_OPCODE 0X16
#define GET_POS_THEO_OPCODE 0X17

void BEGIN(SerialTalks &inst, Deserializer &input, Serializer &output);

void SET_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output);

void SET_X(SerialTalks &inst, Deserializer &input, Serializer &output);

void SET_Y(SerialTalks &inst, Deserializer &input, Serializer &output);

void SET_Z(SerialTalks &inst, Deserializer &input, Serializer &output);

void GET_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output);

void GET_POSITION_THEO(SerialTalks &inst, Deserializer &input, Serializer &output);

#endif //__INSTRUCTIONS_H__

