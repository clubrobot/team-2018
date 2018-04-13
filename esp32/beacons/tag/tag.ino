/**
 * 
 * @todo
 *  - move strings to flash (less RAM consumption)
 *  - fix deprecated convertation form string to char* startAsTag
 *  - give example description
 */
#include "pin.h"
#include <EEPROM.h>

#include <SPI.h>
#include "DW1000Ranging.h"

#include "SSD1306.h"
#include <Wire.h>
#include "MatrixMath.h"

#include "../../common/SerialTalks.h"
#include "instructions.h"

SSD1306 display(0x3C, PIN_SDA, PIN_SCL);

static float d1 = 0;
static float d2 = 0;
static float d3 = 0;
static float d4 = 0;
bool a1Connected = false;
bool a2Connected = false;
bool a3Connected = false;
bool a4Connected = false;

float p[2] = {-1,-1}; // Target point

void newRange()
{
  uint8_t color = DW1000Ranging.getColor();
  const float x_1 = 5;
  float y_1 = -49;
  const float x_2 = 1000;
  float y_2 = 3049;
  const float x_3 = 1950;
  float y_3 = -49;
  const float x_4 = 21.18;
  float y_4 = 1326;
  const float z_tag = 484.3;
  const float z_anchor = 438.3;
  const float z_central = 1016.3;

  if(color == 1){ // ORANGE
    y_1 = 3049;
    y_2 = -49;
    y_3 = 3049;
    y_4 = 1674;
  } 
  

  static String toDisplay;


  //Serial.print("from: ");
  //Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
  //Serial.print("\t Range: ");
  //Serial.print(DW1000Ranging.getDistantDevice()->getRange());
  //Serial.print(" m");
  //Serial.print("\t RX power: ");
  //Serial.print(DW1000Ranging.getDistantDevice()->getRXPower());
  //Serial.println(" dBm");

  byte id = DW1000Ranging.getDistantDevice()->getShortAddress();

  float distance = DW1000Ranging.getDistantDevice()->getRange() * 1000;
  float projection;

  switch(id){
    case 35:    //TODO : should be 0
      projection = distance * distance - ((z_anchor - z_tag) * (z_anchor - z_tag));
      if(projection > 0)
        d1 = sqrt(projection); // projection dans le plan des tags
      else
        d1 = 0;
      break;
    case 36: //TODO : should be 1
      projection = distance * distance - ((z_anchor - z_tag) * (z_anchor - z_tag));
      if (projection > 0)
        d2 = sqrt(projection); // projection dans le plan des tags
      else
        d2 = 0;
      break;
    case 37: //TODO : should be 2
      projection = distance * distance - ((z_anchor - z_tag) * (z_anchor - z_tag));
      if (projection > 0)
        d3 = sqrt(projection); // projection dans le plan des tags
      else
        d3 = 0;
      break;
    case 38: //TODO : should be 3
      projection = distance * distance - ((z_central - z_tag) * (z_central - z_tag));
      if(projection > 0)
        d4 = sqrt(projection); // projection dans le plan des tags
      else
        d4 = 0;
      break;
  }

  display.clear();
  int nbDevices = a1Connected + a2Connected + a3Connected + a4Connected;
  switch(nbDevices){
    case 0:
     {
      toDisplay = "(0)";
      display.drawString(64, 0, toDisplay);
      display.display();
      p[0] = -1000;
      p[1] = -1000;
     }
      break;
    case 1:
      {
      toDisplay = "(1)";
      display.drawString(64, 0, toDisplay);
      display.display();
      p[0] = -1000;
      p[1] = -1000;
      }
      break;
    case 2:
    {
      toDisplay = "(2)";
      display.drawString(64, 0, toDisplay);
      display.display();
      p[0] = -1000;
      p[1] = -1000;
    }
      break;
    case 3:
    {
      int count = 0;
      float x[3];
      float y[3];
      float z[3];
      float d[3];
      if(a1Connected){
        x[count] = x_1;
        y[count] = y_1;
        z[count] = z_anchor;
        d[count] = d1;
        count++;
      }
      if (a2Connected)
      {
        x[count] = x_2;
        y[count] = y_2;
        z[count] = z_anchor;
        d[count] = d2;
        count++;
      }
      if (a3Connected)
      {
        x[count] = x_3;
        y[count] = y_3;
        z[count] = z_anchor;
        d[count] = d3;
        count++;
      }
      if (a4Connected && count < 3)
      {
        x[count] = x_4;
        y[count] = y_4;
        z[count] = z_central;
        d[count] = d4;
        count++;
      }
      // 3D Trilateration algorithm
      float A[2][2] = {{-2 * (x[0] - x[2]), -2 * (y[0] - y[2])},
                       {-2 * (x[1] - x[2]), -2 * (y[1] - y[2])}};

      float b[2] = {d[0] * d[0] - x[0] * x[0] - y[0] * y[0] - d[2] * d[2] + x[2] * x[2] + y[2] * y[2], d[1] * d[1] - x[1] * x[1] - y[1] * y[1] - d[2] * d[2] + x[2] * x[2] + y[2] * y[2]};
      float Ainv[2][2];
      memcpy(&Ainv[0][0], &A[0][0], sizeof(float) * 4);
      Matrix.Invert(&Ainv[0][0], 2);
      Matrix.Multiply(&Ainv[0][0], &b[0], 2, 2, 1, &p[0]);
      toDisplay = "(";
      toDisplay += round(p[0]/10);
      toDisplay += ",";
      toDisplay += round(p[1]/10);
      toDisplay += ")\n(3)";
      display.drawString(64, 0, toDisplay);
      display.display();
    }
      break;
    case 4:
    {
      // 4D Trilateration algorithm
      
      float A[3][2] = {{-2 * (x_1 - x_4), -2 * (y_1 - y_4)},
                       {-2 * (x_2 - x_4), -2 * (y_2 - y_4)},
                       {-2 * (x_3 - x_4), -2 * (y_3 - y_4)}};

      float b[3] = {d1 * d1 - x_1 * x_1 - y_1 * y_1 - d4 * d4 + x_4 * x_4 + y_4 * y_4, d2 * d2 - x_2 * x_2 - y_2 * y_2 - d4 * d4 + x_4 * x_4 + y_4 * y_4, d3 * d3 - x_3 * x_3 - y_3 * y_3 - d4 * d4 + x_4 * x_4 + y_4 * y_4};
      float Atr[2][3];
      Matrix.Transpose(&A[0][0], 3, 2, &Atr[0][0]);
      float Ainv[2][2];
      Matrix.Multiply(&Atr[0][0], &A[0][0], 2, 3, 2, &Ainv[0][0]);
      Matrix.Invert(&Ainv[0][0], 2);
      float Atemp[2][3];
      Matrix.Multiply(&Ainv[0][0], &Atr[0][0], 2, 2, 3, &Atemp[0][0]);
      Matrix.Multiply(&Atemp[0][0], &b[0], 2, 3, 1, &p[0]);
      toDisplay = "(";
      toDisplay += round(p[0] / 10);
      toDisplay += ",";
      toDisplay += round(p[1] / 10);
      toDisplay += ")\n(4)";
      display.drawString(64, 0, toDisplay);
      display.display();
      

     // 3D Trilateration algorithm without the nearest anchor distance

    }/*
      int count = 0;
      float x[3];
      float y[3];
      float z[3];
      float d[3];
      String nAnch = "";
      if (d1>d2 || d1>d3 || d1>d4)
      {
        x[count] = x_1;
        y[count] = y_1;
        z[count] = z_anchor;
        d[count] = d1;
        count++;
        nAnch += "A1";
      }
      if (d2>d1 || d2>d3 || d2>d4)
      {
        x[count] = x_2;
        y[count] = y_2;
        z[count] = z_anchor;
        d[count] = d2;
        count++;
        nAnch += "A2";
      }
      if (d3>d1 || d3>d2 || d3>d4)
      {
        x[count] = x_3;
        y[count] = y_3;
        z[count] = z_anchor;
        d[count] = d3;
        count++;
        nAnch += "A3";
      }
      if (count < 3 && (d4>d1 || d4>d2 || d4>d3))
      {
        x[count] = x_4;
        y[count] = y_4;
        z[count] = z_central;
        d[count] = d4;
        count++;
        nAnch += "A4";
      }
      // 3D Trilateration algorithm
      float A[2][2] = {{-2 * (x[0] - x[2]), -2 * (y[0] - y[2])},
                       {-2 * (x[1] - x[2]), -2 * (y[1] - y[2])}};

      float b[2] = {d[0] * d[0] - x[0] * x[0] - y[0] * y[0] - d[2] * d[2] + x[2] * x[2] + y[2] * y[2], d[1] * d[1] - x[1] * x[1] - y[1] * y[1] - d[2] * d[2] + x[2] * x[2] + y[2] * y[2]};
      float Ainv[2][2];
      memcpy(&Ainv[0][0], &A[0][0], sizeof(float) * 4);
      Matrix.Invert(&Ainv[0][0], 2);
      Matrix.Multiply(&Ainv[0][0], &b[0], 2, 2, 1, &p[0]);
      toDisplay = "(";
      toDisplay += round(p[0] / 10);
      toDisplay += ",";
      toDisplay += round(p[1] / 10);
      toDisplay += ")\n(";
      toDisplay += nAnch;
      toDisplay += ")";
      display.drawString(64, 0, toDisplay);
      display.display();*/
      break;
  }
  
  DW1000Ranging.setPosX(p[0]);
  DW1000Ranging.setPosY(p[1]);

  digitalWrite(PIN_LED_OK, HIGH);
  digitalWrite(PIN_LED_FAIL, LOW);
}

void newDevice(DW1000Device *device)
{
  //Serial.print("ranging init; 1 device added ! -> ");
  //Serial.print(" short:");
  //Serial.println(device->getShortAddress(), HEX);
  byte id = device->getShortAddress();
  switch (id)
  {
  case 35: //TODO : should be 0
    a1Connected = true;
    break;
  case 36: //TODO : should be 1
    a2Connected = true;
    break;
  case 37: //TODO : should be 2
    a3Connected = true;
    break;
  case 38: //TODO : should be 3
    a4Connected = true;
  }
}

void inactiveDevice(DW1000Device *device)
{
  //Serial.print("delete inactive device: ");
  //Serial.println(device->getShortAddress(), HEX);
  byte id = device->getShortAddress();
  switch (id)
  {
  case 35: //TODO : should be 0
    a1Connected = false;
    break;
  case 36: //TODO : should be 1
    a2Connected = false;
    break;
  case 37: //TODO : should be 2
    a3Connected = false;
    break;
  case 38: //TODO : should be 3
    a4Connected = false;
  }
  if (!(a1Connected || a2Connected || a3Connected || a4Connected))
  {
    display.clear();
    display.drawString(64, 0, "INACTIVE");
    display.display();
    digitalWrite(PIN_LED_OK, LOW);
    digitalWrite(PIN_LED_FAIL, HIGH);
    p[0] = -1;
    p[1] = -1;
  }
}

void setup() {
  Serial.begin(SERIALTALKS_BAUDRATE);
  talks.begin(Serial);

  talks.bind(GET_POSITION_OPCODE, GET_POSITION);

  //init the configuration
  DW1000Ranging.initCommunication(PIN_UWB_RST, PIN_SPICSN, PIN_IRQ, PIN_SPICLK, PIN_SPIMISO, PIN_SPIMOSI); //Reset, CS, IRQ pin
  //define the sketch as anchor. It will be great to dynamically change the type of module
  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachNewDevice(newDevice);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);
  //Enable the filter to smooth the distance
  DW1000Ranging.useRangeFilter(true);
  DW1000Ranging.setRangeFilterValue(5);

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

  display.setFont(ArialMT_Plain_24);
}

void loop() {
  static unsigned long trilaterationReportTime = millis();
  DW1000Ranging.loop();
  talks.execute();
 /* if (millis() - trilaterationReportTime > 1000){
    trilaterationReportTime = millis();
    DW1000Ranging.transmitTrilaterationReport();
  }*/
}


