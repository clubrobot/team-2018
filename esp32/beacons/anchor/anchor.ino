/**
 * 
 * @todo
 *  - move strings to flash (less RAM consumption)
 *  - fix deprecated convertation form string to char* startAsAnchor
 *  - give example description
 */

#include "pin.h"
#include "configuration.h"
#include <EEPROM.h>

#include <SPI.h>
#include "DW1000Ranging.h"
#include "DW1000.h"

#include "SSD1306.h"
#include <Wire.h>

#include "../../common/SerialTalks.h"
#include "instructions.h"



SSD1306 display(0x3C, PIN_SDA, PIN_SCL);

byte currentBeaconNumber = 1;
boolean calibrationRunning = false;

void newRange()
{

  DW1000Ranging.setRangeFilterValue(5);

  String toDisplay;

  if(calibrationRunning==true){
    display.setFont(ArialMT_Plain_16);
    toDisplay = "timeOut";
  } else {
    display.setFont(ArialMT_Plain_24);
    // get master tag coordinates
    float x = DW1000Ranging.getPosX(TAG_SHORT_ADDRESS[0]) / 10;
    float y = DW1000Ranging.getPosY(TAG_SHORT_ADDRESS[0]) / 10;
    toDisplay = "(";
    toDisplay += (int)x;
    toDisplay += ", ";
    toDisplay += (int)y;
    toDisplay += ")\n";
    // get slave tag coordinates
    x = DW1000Ranging.getPosX(TAG_SHORT_ADDRESS[1]) / 10;
    y = DW1000Ranging.getPosY(TAG_SHORT_ADDRESS[1]) / 10;
    toDisplay += "(";
    toDisplay += (int)x;
    toDisplay += ", ";
    toDisplay += (int)y;
    toDisplay += ")\n";
  }

  display.clear();
  display.drawString(64, 0, toDisplay);
  display.display();
  digitalWrite(PIN_LED_OK, HIGH);
  digitalWrite(PIN_LED_FAIL, LOW);
}

void calibration(int realDistance, int mesure){
  static int lastErrors[3] = {100,100,100};
  static int errorIndex = 0;
  static uint16_t antennaDelay ;
  if(calibrationRunning==false){
    antennaDelay = DW1000.getAntennaDelay();
    calibrationRunning = true;
  }
  DW1000Ranging.setRangeFilterValue(15);
  mesure = sqrt(mesure * mesure - ((Z_HEIGHT[currentBeaconNumber] - Z_TAG) * (Z_HEIGHT[currentBeaconNumber] - Z_TAG))); // projection dans le plan des tags
  
  lastErrors[errorIndex++] = realDistance - mesure;
  
  if(errorIndex > 2){
    errorIndex = 0;
    int meanError = (lastErrors[0] + lastErrors[1] + lastErrors[2]) / 3;

    if (abs(meanError) < 1)
    { // end of calibration
      DW1000Ranging.stopCalibration();
      calibrationRunning = false;
      lastErrors[0] = 100;
      lastErrors[1] = 100;
      lastErrors[2] = 100;
      //EEPROM.write(EEPROM_ANTENNA_DELAY, antennaDelay >> 8);    // TODO bug potentiel ici (valeurs incohérentes à la relecture de l'eeprom)
      //EEPROM.write(EEPROM_ANTENNA_DELAY + 1, antennaDelay % 256);
      //EEPROM.commit();
      //ESP.restart();
    } else if (meanError < 0) {
      antennaDelay++;
      DW1000Class::setAntennaDelay(antennaDelay);
    } else {
      antennaDelay--;
      DW1000Class::setAntennaDelay(antennaDelay);
    }
  }
  
  display.clear();
  display.setFont(ArialMT_Plain_16);
  String toDisplay = "target: ";
  toDisplay += realDistance;
  toDisplay += "mm\nmesure: ";
  toDisplay += mesure;
  toDisplay += "mm\ndelay: ";
  toDisplay += antennaDelay;
  display.drawString(64, 0, toDisplay);
  display.display();
}

void newBlink(DW1000Device *device)
{

}

void inactiveDevice(DW1000Device *device)
{
  display.clear();
  display.drawString(64, 0, "INACTIVE");
  display.display();
  digitalWrite(PIN_LED_OK, LOW);
  digitalWrite(PIN_LED_FAIL, HIGH);
}

void setup() {
  
  Serial.begin(SERIALTALKS_BAUDRATE);
  talks.begin(Serial);
  
  talks.bind(UPDATE_ANCHOR_NUMBER_OPCODE, UPDATE_ANCHOR_NUMBER);
  talks.bind(UPDATE_ANTENNA_DELAY_OPCODE, UPDATE_ANTENNA_DELAY);
  talks.bind(CALIBRATION_ROUTINE_OPCODE, CALIBRATION_ROUTINE);
  talks.bind(UPDATE_COLOR_OPCODE, UPDATE_COLOR);
  talks.bind(GET_COORDINATE_OPCODE,GET_COORDINATE);
  talks.bind(GET_BOT1_COORDINATE_OPCODE, GET_BOT1_COORDINATE);
  talks.bind(GET_BOT2_COORDINATE_OPCODE, GET_BOT2_COORDINATE);

  /*if (!EEPROM.begin(EEPROM_SIZE))   // Already done in serialtalks lib
  {
    //Serial.println("failed to initialise EEPROM");
    delay(1000000);
  }*/

  #if 0
  EEPROM.write(EEPROM_NUM_ANCHOR, currentBeaconNumber);
  EEPROM.commit();
  #endif
  currentBeaconNumber = EEPROM.read(EEPROM_NUM_ANCHOR);

  // init communication
  DW1000Ranging.initCommunication(PIN_UWB_RST, PIN_SPICSN, PIN_IRQ, PIN_SPICLK, PIN_SPIMISO, PIN_SPIMOSI); //Reset, CS, IRQ pin
  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachBlinkDevice(newBlink);
  DW1000Ranging.attachInactiveAncDevice(inactiveDevice);  // TODO : rename func
  DW1000Ranging.attachAutoCalibration(calibration);

  unsigned int replyTime;
  switch (currentBeaconNumber){
    case 0 :
      replyTime = 7000;
      break;
    case 1:
      replyTime = 21000;
      break;
    case 2:
      replyTime = 35000;
      break;
    case 3:
      replyTime = 49000;
      break;
  }
  
  DW1000Ranging.setReplyTime(replyTime);
  //Enable the filter to smooth the distance
  DW1000Ranging.useRangeFilter(true);
  DW1000Ranging.setRangeFilterValue(5);

  int antennaDelay = ANTENNA_DELAY[currentBeaconNumber];
  #if 0
  EEPROM.write(EEPROM_ANTENNA_DELAY, antennaDelay >> 8);
  EEPROM.write(EEPROM_ANTENNA_DELAY + 1, antennaDelay % 256);
  EEPROM.commit();
  #endif
 // antennaDelay = (EEPROM.read(EEPROM_ANTENNA_DELAY) << 8) + EEPROM.read(EEPROM_ANTENNA_DELAY+1);
  DW1000Class::setAntennaDelay(antennaDelay); //16384 for tag, approximately 16530 for anchors

  //we start the module as an anchor
  DW1000Ranging.startAsAnchor("82:17:FC:87:0D:71:DC:75", DW1000.MODE_LONGDATA_RANGE_ACCURACY, ANCHOR_SHORT_ADDRESS[currentBeaconNumber]);

  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_CENTER );

  pinMode(PIN_LED_FAIL,OUTPUT);
  pinMode(PIN_LED_OK,OUTPUT);
  digitalWrite(PIN_LED_OK,HIGH);
  digitalWrite(PIN_LED_FAIL,HIGH);

  String toDisplay = "SYNCHRONISATION\n(anchor : ";
  toDisplay += DW1000Ranging.getCurrentShortAddress()[0]; //currentBeaconNumber;
  toDisplay += ")\n";
  toDisplay += antennaDelay;
  display.drawString(64, 64/4, toDisplay);
  display.display();

  display.setFont(ArialMT_Plain_24);
}

void loop() {
  DW1000Ranging.loop();
  talks.execute();
}


