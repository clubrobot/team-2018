#ifndef INSTRUCTIONS_H
#define INSTRUCTIONS_H

#include "../common/SerialTalks.h"

#define UPDATE_ANCHOR_NUMBER_OPCODE 0x10
#define UPDATE_ANTENNA_DELAY_OPCODE 0x11
#define CALIBRATION_ROUTINE_OPCODE  0x12
#define UPDATE_COLOR_OPCODE         0x13
#define GET_COORDINATE_OPCODE       0x14
#define GET_BOT1_COORDINATE_OPCODE  0x15
#define GET_BOT2_COORDINATE_OPCODE  0x16

// Instructions prototypes

void UPDATE_ANCHOR_NUMBER(SerialTalks &talks, Deserializer &input, Serializer &output);
void UPDATE_ANTENNA_DELAY(SerialTalks &talks, Deserializer &input, Serializer &output);

/**
 * Purpose : Start the auto calibration algorithm
 * args : 
 *          - real distance in mm (INT)
 *          - timeout autocalibration delay in ms (UNSIGNED LONG)
 */ 
void CALIBRATION_ROUTINE(SerialTalks &talks, Deserializer &input, Serializer &output);
void UPDATE_COLOR(SerialTalks &talks, Deserializer &input, Serializer &output);
void GET_COORDINATE(SerialTalks &talks, Deserializer &input, Serializer &output);
void GET_BOT1_COORDINATE(SerialTalks &talks, Deserializer &input, Serializer &output);
void GET_BOT2_COORDINATE(SerialTalks &talks, Deserializer &input, Serializer &output);

#endif //INSTRUCTIONS_H