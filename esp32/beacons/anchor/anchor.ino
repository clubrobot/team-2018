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

  byte currentBeaconNumber = 2;
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
  unsigned int replyTime = 35000;
  #if 0
  EEPROM.write(EEPROM_REPLY_DELAY, replyTime >> 8);
  EEPROM.write(EEPROM_REPLY_DELAY + 1, replyTime % 256);
  EEPROM.commit();
  #endif
  replyTime = (EEPROM.read(EEPROM_REPLY_DELAY) << 8) + EEPROM.read(EEPROM_REPLY_DELAY);
  DW1000Ranging.setReplyTime(replyTime);
  //Enable the filter to smooth the distance
  DW1000Ranging.useRangeFilter(true);
  
  //we start the module as an anchor
  DW1000Ranging.startAsAnchor("82:17:FC:87:0D:71:DC:75", DW1000.MODE_LONGDATA_RANGE_ACCURACY, ANCHOR_SHORT_ADDRESS[currentBeaconNumber]);

  int antennaDelay = (EEPROM.read(50)<<8) + EEPROM.read(51);
  DW1000Class::setAntennaDelay(antennaDelay); //16384 for tag, approximately 16530 for anchors


  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_CENTER );

  pinMode(PIN_LED_FAIL,OUTPUT);
  pinMode(PIN_LED_OK,OUTPUT);
  digitalWrite(PIN_LED_OK,HIGH);
  digitalWrite(PIN_LED_FAIL,HIGH);
  display.drawString(64, 24, "SYNCHRONISATION\n(anchor)");
  display.display();

  display.setFont(ArialMT_Plain_24);
}

void loop() {
  DW1000Ranging.loop();
  talks.execute();
}


