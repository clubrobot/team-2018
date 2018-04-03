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

byte currentBeaconNumber = 3;

void newRange()
{
  Serial.print("from: ");
  Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
  Serial.print("\t Range: ");
  Serial.print(DW1000Ranging.getDistantDevice()->getRange());
  Serial.print(" m");
  Serial.print("\t RX power: ");
  Serial.print(DW1000Ranging.getDistantDevice()->getRXPower());
  Serial.println(" dBm");

  display.clear();
  float distance = DW1000Ranging.getDistantDevice()->getRange()*100;
  switch (currentBeaconNumber){
    case 0: // TODO : mettre les adresses dans configuration.h
    case 1:
    case 2: // balises fixes
      distance = sqrt(distance * distance - ((z_anchor - z_tag) * (z_anchor - z_tag))); // projection dans le plan des tags
      break;
    case 3: // balise centrale
      distance = sqrt(distance * distance - ((z_central - z_tag) * (z_central - z_tag))); // projection dans le plan des tags
      break;
  }
    

  String toDisplay = "Distance : \n";
  toDisplay += distance;
  toDisplay += "cm";
  display.drawString(64, 0, toDisplay);
  display.display();
  digitalWrite(PIN_LED_OK, HIGH);
  digitalWrite(PIN_LED_FAIL, LOW);
}

void newBlink(DW1000Device *device)
{
  Serial.print("blink; 1 device added ! -> ");
  Serial.print(" short:");
  Serial.println(device->getShortAddress(), HEX);
}

void inactiveDevice(DW1000Device *device)
{
  Serial.print("delete inactive device: ");
  Serial.println(device->getShortAddress(), HEX);

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

  /*if (!EEPROM.begin(EEPROM_SIZE))   // Already done in serialtalks lib
  {
    Serial.println("failed to initialise EEPROM");
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
  DW1000Ranging.attachInactiveDevice(inactiveDevice);
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
  
  int antennaDelay = 16530;
  #if 0
  EEPROM.write(EEPROM_ANTENNA_DELAY, antennaDelay >> 8);
  EEPROM.write(EEPROM_ANTENNA_DELAY + 1, antennaDelay % 256);
  EEPROM.commit();
  #endif
  antennaDelay = (EEPROM.read(50)<<8) + EEPROM.read(51);
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
  toDisplay += replyTime;
  display.drawString(64, 64/4, toDisplay);
  display.display();

  display.setFont(ArialMT_Plain_24);
}

void loop() {
  DW1000Ranging.loop();
  talks.execute();
}


