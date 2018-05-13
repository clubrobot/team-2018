#include <Arduino.h>

#include "../common/SerialTalks.h"


void TEST_LED(SerialTalks& inst, Deserializer& input, Serializer& output)
{

		if(input.read<bool>())
		{
			pinMode(2, OUTPUT);
        	digitalWrite(2, HIGH);
		}
		else
		{
			pinMode(2, OUTPUT);
        	digitalWrite(2, LOW);	
		}
		

}

void setup() {
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
    talks.bind(0X11,TEST_LED);

}
void loop() {
	talks.execute();
}

