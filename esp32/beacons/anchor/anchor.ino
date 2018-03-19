/**
 * 
 * @todo
 *  - move strings to flash (less RAM consumption)
 *  - fix deprecated convertation form string to char* startAsAnchor
 *  - give example description
 */
#include <SPI.h>
#include "DW1000Ranging.h"
#include "DW1000.h"
#include "pin.h"
#include "SSD1306.h"
#include <Wire.h>
#include <EEPROM.h>

#define EEPROM_SIZE 64

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
  Serial.begin(115200);
  if (!EEPROM.begin(EEPROM_SIZE))
  {
    Serial.println("failed to initialise EEPROM");
    delay(1000000);
  }
  delay(100);
  //init the configuration
  //initCommunication(uint8_t myRST = DEFAULT_RST_PIN, uint8_t mySS = DEFAULT_SPI_SS_PIN, uint8_t myIRQ = 2, int8_t sck = -1, int8_t miso = -1, int8_t mosi = -1)
  DW1000Ranging.initCommunication(PIN_UWB_RST, PIN_SPICSN, PIN_IRQ, PIN_SPICLK, PIN_SPIMISO, PIN_SPIMOSI); //Reset, CS, IRQ pin
  //define the sketch as anchor. It will be great to dynamically change the type of module
  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachBlinkDevice(newBlink);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);
  //Enable the filter to smooth the distance
  DW1000Ranging.useRangeFilter(true);
  
  //we start the module as an anchor
  DW1000Ranging.startAsAnchor("82:17:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY);
  int antennaDelay = 16560;
#if 0
  EEPROM.write(50, antennaDelay >> 8);
  EEPROM.write(51, antennaDelay % 256);
  EEPROM.commit();
#endif
  antennaDelay = (EEPROM.read(50)<<8) + EEPROM.read(51);
  Serial.println("antennaDelay : ");
  Serial.println(antennaDelay);
  Serial.println("EEPROM values :");
  Serial.println(EEPROM.read(50));
  Serial.println(EEPROM.read(51));
  DW1000Class::setAntennaDelay(antennaDelay); //16384 for tag, 16530 for anchor


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
}


