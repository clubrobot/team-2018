#include "instructions.h"
#include "configuration.h"
#include "EEPROM.h"

void UPDATE_ANCHOR_NUMBER(SerialTalks &talks, Deserializer &input, Serializer &output){
    talks.out << "update anchor number\n";
    byte number = input.read<byte>();
    EEPROM.write(EEPROM_NUM_ANCHOR,number);
    EEPROM.commit();
    // Restart to update current configuration
    talks.out << "restarting to update configuration\n";
    ESP.restart();
}


void UPDATE_ANTENNA_DELAY(SerialTalks &talks, Deserializer &input, Serializer &output){
    talks.out << "update antenna delay\n";
    int antennaDelay = input.read<int>();
    EEPROM.write(EEPROM_ANTENNA_DELAY, antennaDelay >> 8);
    EEPROM.write(EEPROM_ANTENNA_DELAY+1, antennaDelay % 256);
    EEPROM.commit();
    // Restart to update current configuration
    talks.out << "restarting to update configuration\n";
    ESP.restart();
}

 
void CALIBRATION_ROUTINE(SerialTalks &talks, Deserializer &input, Serializer &output){
    talks.out << "calibration routine\n";
    int realDistance = input.read<int>();
    // TODO autocalibration
}