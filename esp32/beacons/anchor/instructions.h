#ifndef INSTRUCTIONS_H
#define INSTRUCTIONS_H

#include "../common/SerialTalks.h"

#define UPDATE_ANCHOR_NUMBER_OPCODE 0x10
#define UPDATE_CONFIGURATION_OPCODE 0x11
#define CALIBRATION_ROUTINE_OPCODE 0x12

// Instructions prototypes

void UPDATE_ANCHOR_NUMBER(SerialTalks &talks, Deserializer &input, Serializer &output);
void UPDATE_CONFIGURATION(SerialTalks &talks, Deserializer &input, Serializer &output);
void CALIBRATION_ROUTINE(SerialTalks &talks, Deserializer &input, Serializer &output);

#endif //INSTRUCTIONS_H