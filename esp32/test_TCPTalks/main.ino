#include <Arduino.h>
#include "../common/Pickle.h"
#include "../common/SerialTalks.h"
#include "../common/tcptalks.h"


int size;
double num = 1.11;
int numm = 10;

uint8_t tab;

TCPTalks talk;


void setup() {
    Serial.begin(115200);

    talk.connect(5000);

    talk.bind(0x05, SWITCH_LED);

}

void loop() 
{
	talk.execute();

	// uint8_t frame[50];

	// Pickler pickle(frame);
	// UnPickler Unpickle(frame);


	// pickle.dump_byte(0X01);
	// pickle.end_frame();

	// Serial.print('\n');

	// tab = Unpickle.load_byte();

	// Serial.print(tab,HEX);


	// delay(10000);

}

