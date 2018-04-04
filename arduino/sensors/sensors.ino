#include <Arduino.h>

#include "../common/UltrasonicSensor.h"
#include "../common/SensorListener.h"
#include "../common/SerialTalks.h"
#include "instructions.h"
#include "PIN.h"
 

bool activated = true;

UltrasonicSensor SensorAv;
UltrasonicSensor SensorAr;
SensorListener   ListenerAv;
SensorListener   ListenerAr;

void setup() {
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
    talks.bind(GET_MESURE_OPCODE, GET_MESURE);
    SensorAv.attach(TRIGGPIN7, ECHOPIN2);
    SensorAr.attach(TRIGGPIN8, ECHOPIN3);
    SensorAv.trig();
    SensorAr.trig();
    ListenerAv.attach(SensorAv,1000);
    ListenerAr.attach(SensorAr,1000);

}


void loop() {
  talks.execute(); 
  SensorAv.update();
  SensorAr.update();
  ListenerAv.update();
  ListenerAr.update();

  if (SensorAv.getReady() && activated) {
    SensorAv.trig();
  }
  if (SensorAr.getReady() && activated){
      SensorAr.trig();
  }
}


