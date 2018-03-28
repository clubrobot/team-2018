/**
 * 
 * @todo
 *  - move strings to flash (less RAM consumption)
 *  - fix deprecated convertation form string to char* startAsTag
 *  - give example description
 */
#include <SPI.h>
#include "DW1000Ranging.h"
#include "pin.h"
#include "SSD1306.h"
#include <Wire.h>
#include "MatrixMath.h"

SSD1306 display(0x3C, PIN_SDA, PIN_SCL);

void newRange()
{
  const float x_1 = 5;
  const float y_1 = -49;
  const float x_2 = 1000;
  const float y_2 = 3049;
  const float x_3 = 1950;
  const float y_3 = -49;
  

  static String toDisplay[4];
  static float d1 = 1500;
  static float d2 = 2097;
  static float d3 = 1380;

  Serial.print("from: ");
  Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
  Serial.print("\t Range: ");
  Serial.print(DW1000Ranging.getDistantDevice()->getRange());
  Serial.print(" m");
  Serial.print("\t RX power: ");
  Serial.print(DW1000Ranging.getDistantDevice()->getRXPower());
  Serial.println(" dBm");

  byte id = DW1000Ranging.getDistantDevice()->getShortAddress();

  display.clear();
  float distance = DW1000Ranging.getDistantDevice()->getRange() * 1000;

  switch(id){
    case 35:    //TODO : should be 0
      d1 = distance;
      toDisplay[0] = "anch0 : ";
      toDisplay[0] += distance;
      toDisplay[0] += " mm";
      break;
    case 36: //TODO : should be 1
      d2 = distance;
      toDisplay[1] = "anch1 : ";
      toDisplay[1] += distance;
      toDisplay[1] += " mm";
      break;
    case 37: //TODO : should be 2
      d3 = distance;
      toDisplay[2] = "anch2 : ";
      toDisplay[2] += distance;
      toDisplay[2] += " mm";
      break;
    /*default:
      toDisplay[3] = "(";
      toDisplay[3] += id;
      toDisplay[3] += ") : ";
      toDisplay[3] += distance;
      toDisplay[3] += " mm";*/
  }

  // Trilateration algorithm
  float A[2][2] = {{-2 * (x_1 - x_3), -2 * (y_1 - y_3)},
                   {-2 * (x_2 - x_3), -2 * (y_2 - y_3)}};

  float b[2] = {d1 * d1 - x_1 * x_1 - y_1 * y_1 - d3 * d3 + x_3 * x_3 + y_3 * y_3, d2 * d2 - x_2 * x_2 - y_2 * y_2 - d3 * d3 + x_3 * x_3 + y_3 * y_3};
  float Ainv[2][2];
  memcpy(&Ainv[0][0], &A[0][0], sizeof(float) * 4);
  Matrix.Invert(&Ainv[0][0], 2);
  float p[2];
  Matrix.Multiply(&Ainv[0][0], &b[0], 2, 2, 1, &p[0]);

  toDisplay[3] = "position : (";
  toDisplay[3] += p[0];
  toDisplay[3] += ",";
  toDisplay[3] += p[1];
  toDisplay[3] += ")";

  display.drawString(64, 0, toDisplay[0]);
  display.drawString(64, 15, toDisplay[1]);
  display.drawString(64, 30, toDisplay[2]);
  display.drawString(64, 45, toDisplay[3]);
  display.display();
  digitalWrite(PIN_LED_OK, HIGH);
  digitalWrite(PIN_LED_FAIL, LOW);
}

void newDevice(DW1000Device *device)
{
  Serial.print("ranging init; 1 device added ! -> ");
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
  delay(1000);
  //init the configuration
  DW1000Ranging.initCommunication(PIN_UWB_RST, PIN_SPICSN, PIN_IRQ, PIN_SPICLK, PIN_SPIMISO, PIN_SPIMOSI); //Reset, CS, IRQ pin
  //define the sketch as anchor. It will be great to dynamically change the type of module
  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachNewDevice(newDevice);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);
  //Enable the filter to smooth the distance
  DW1000Ranging.useRangeFilter(true);
  
  //we start the module as a tag
  DW1000Ranging.startAsTag("7D:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY);

  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_CENTER);

  pinMode(PIN_LED_FAIL, OUTPUT);
  pinMode(PIN_LED_OK, OUTPUT);
  digitalWrite(PIN_LED_OK, HIGH);
  digitalWrite(PIN_LED_FAIL, HIGH);
  display.drawString(64, 24, "SYNCHRONISATION\n(tag)");
  display.display();

  //display.setFont(ArialMT_Plain_24);
}

void loop() {
  DW1000Ranging.loop();
}


