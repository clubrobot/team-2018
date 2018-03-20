#include "instructions.h"

void UPDATE_ANCHOR_NUMBER(SerialTalks &talks, Deserializer &input, Serializer &output){
    talks.out << "update anchor number\n";
    output.write<int>(23456);
}


void UPDATE_CONFIGURATION(SerialTalks &talks, Deserializer &input, Serializer &output){
    talks.out << "update configuration\n";
}


void CALIBRATION_ROUTINE(SerialTalks &talks, Deserializer &input, Serializer &output){
    talks.out << "calibration routine\n";
}