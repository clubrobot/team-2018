#include <Arduino.h>

#include "../common/SerialTalks.h"


void setup() {
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
}
void loop() {
	talks.execute();
}

