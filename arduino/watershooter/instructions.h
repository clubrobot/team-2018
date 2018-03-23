#ifndef __INSTRUCTIONS_H__
#define __INSTRUCTIONS_H__

#include "../common/SerialTalks.h"

#define _WRITE_INDOOR_OPCODE			0x11
#define _GET_INDOOR_OPCODE				0x12
#define _WRITE_OUTDOOR_OPCODE			0x13
#define _GET_OUTDOOR_OPCODE				0X14
#define _WRITE_TRASH_OPCODE        		0x15
#define _GET_TRASH_OPCODE				0x16
#define _SET_MOTOR_VELOCITY_OPCODE		0x17
#define _GET_MOTOR_VELOCITY_OPCODE		0x18
#define _GET_WATER_COLOR_OPCODE			0x19
#define _SET_MOTOR_PULSEWIDTH_OPCODE    0x1A
#define _GET_MOTOR_PULSEWIDTH_OPCODE    0x1B
#define _SET_LED_ON_OPCODE              0x1C
#define _SET_LED_OFF_OPCODE             0x1D
#define _FORCE_PULSEWIDTH_OPCODE               0x1E
#define _GET_SHAKER_HORIZONTAL_OPCODE          0x1F
#define _WRITE_SHAKER_HORIZONTAL_OPCODE        0x20
#define _GET_SHAKER_VERTICAL_OPCODE            0x21
#define _WRITE_SHAKER_VERTICAL_OPCODE          0x22

void WRITE_INDOOR(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_INDOOR(SerialTalks &inst, Deserializer &input, Serializer &output);

void WRITE_OUTDOOR(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_OUTDOOR(SerialTalks &inst, Deserializer &input, Serializer &output);

void WRITE_TRASH(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_TRASH(SerialTalks &inst, Deserializer &input, Serializer &output);

void WRITE_SHAKER_HORIZONTAL(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_SHAKER_HORIZONTAL(SerialTalks &inst, Deserializer &input, Serializer &output);

void WRITE_SHAKER_VERTICAL(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_SHAKER_VERTICAL(SerialTalks &inst, Deserializer &input, Serializer &output);

void SET_MOTOR_VELOCITY(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_MOTOR_VELOCITY(SerialTalks &inst, Deserializer &input, Serializer &output);

void GET_WATER_COLOR(SerialTalks &inst, Deserializer &input, Serializer &output);

void SET_MOTOR_PULSEWIDTH(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_MOTOR_PULSEWIDTH(SerialTalks &inst, Deserializer &input, Serializer &output);

void FORCE_PULSEWIDTH(SerialTalks &inst, Deserializer &input, Serializer &output);

void SET_LED_ON(SerialTalks& inst, Deserializer& input, Serializer& output);
void SET_LED_OFF(SerialTalks& inst, Deserializer& input, Serializer& output);

#endif
