#include <Arduino.h>
//#include "DomotiquePannel.h"
#include <FastLED.h>
#include "../common/Effects.h"
#include "../common/tcptalks.h"
#include "instructions.h"
#include "../common/PeriodicProcess.h"

Effects Eff;
TCPTalks talk;

void setup()
{
	Serial.begin(115200);
    talk.connect(10000);
    
    talk.bind(0X11 , SWITCH_LED);
    talk.bind(0X12 , SET_ENGR_ANIMATION);
    talk.bind(0X13 , SET_BAR_ANIMATION);

}

void loop()
{
	talk.execute();

	Eff.update();
}