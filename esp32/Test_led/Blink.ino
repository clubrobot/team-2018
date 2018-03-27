#include <Arduino.h>
#include "../common/Pickle.h"
#include "../common/tcptalks.h"
#include "../common/PannelEffects.h"
#include "instructions.h"

TCPTalks talk;

PannelEffects Animation;

long current_time = 0;
long last_time = 0;

void setup()
{
    Serial.begin(115200);

    talk.connect(500);

    talk.bind(SET_BAR_OPCODE, SET_BAR);
    talk.bind(GET_BAR_OPCODE, GET_BAR);

    talk.bind(SET_LOGO_OPCODE, SET_LOGO);
    talk.bind(GET_LOGO_OPCODE, GET_LOGO);

    talk.bind(SET_ENGR_OPCODE, SET_ENGR);
    talk.bind(GET_ENGR_OPCODE, GET_ENGR);

    talk.bind(IS_CONNECTED_OPCODE, IS_CONNECTED);
}

void loop()
{
    talk.execute();
    Animation.execute();

    /* Auto re-connect step */
    current_time = millis();
    if((talk.is_connected() == false) && ((current_time - last_time)) > 500)
    {
        talk.connect(200);
        last_time = millis();
    }
}