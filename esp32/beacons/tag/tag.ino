/**
 * 
 * @todo
 *  - move strings to flash (less RAM consumption)
 *  - fix deprecated convertation form string to char* startAsTag
 *  - give example description
 */
#include "pin.h"
#include "configuration.h"
#include <EEPROM.h>

#include <SPI.h>
#include "DW1000Ranging.h"
#include "MatrixMath.h"

#include "../../common/SerialTalks.h"
#include "instructions.h"

#include "SSD1306.h"
#include <Wire.h>
#include "OLED_display.h"

OLEDdisplay display(0x3C, PIN_SDA, PIN_SCL);
byte currentBeaconNumber = 1;

static float d1 = 0;
static float d2 = 0;
static float d3 = 0;
static float d4 = 0;
bool a1Connected = false;
bool a2Connected = false;
bool a3Connected = false;
bool a4Connected = false;

float p[2] = {-1,-1}; // Target point

void loopCore0(void *pvParameters)  // loop on core 0
{
  for(;;){
    display.update();
    delay(10);
  }
}

void newRange()
{
  uint8_t color = DW1000Ranging.getColor();
  const float x_1 = 5;
  float y_1 = -73;
  const float x_2 = 1000;
  float y_2 = 3073;
  const float x_3 = 1950;
  float y_3 = -73;
  const float x_4 = (21.18-24);
  float y_4 = 1326;
  const float z_tag = 503.3;
  const float z_anchor = 458.3;
  const float z_central = 1036.3;

  if(color == 1){ // ORANGE
    y_1 = 3073;
    y_2 = -73;
    y_3 = 3073;
    y_4 = 1674;
  } 
  

  static String toDisplay;

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

  int nbDevices = a1Connected + a2Connected + a3Connected + a4Connected;
  switch(nbDevices){
    case 0:
     {
      toDisplay = "(0) ";
      toDisplay += DW1000Ranging.getFrameRate();
      toDisplay += "Hz";
      display.clearMsg(5);
      // display.display();
      p[0] = -1000;
      p[1] = -1000;
     }
      break;
    case 1:
      {
      toDisplay = "(1) ";
      toDisplay += DW1000Ranging.getFrameRate();
      toDisplay += "Hz";
      display.clearMsg(5);
      // display.display();
      p[0] = -1000;
      p[1] = -1000;
      }
      break;
    case 2:
    {
      toDisplay = "(2) ";
      toDisplay += DW1000Ranging.getFrameRate();
      toDisplay += "Hz";
      display.clearMsg(5);
     // display.display();
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
      toDisplay += ")\n(3) ";
      toDisplay += DW1000Ranging.getFrameRate();
      toDisplay += "Hz";
      display.displayMsg(Text(toDisplay, 5, 64, 0));
      // display.display();
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
      toDisplay += ")\n(4) ";
      toDisplay += DW1000Ranging.getFrameRate();
      toDisplay += "Hz";
      display.displayMsg(Text(toDisplay, 5, 64, 0));
      //display.display();
      

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
  
  DW1000Ranging.setPosX(p[0],0);
  DW1000Ranging.setPosY(p[1],0);

  uint8_t c = DW1000Ranging.getColor();
  toDisplay = c;
  toDisplay += c==0?" : green":" : orange";
  display.log(toDisplay);


  digitalWrite(PIN_LED_OK, HIGH);
  digitalWrite(PIN_LED_FAIL, LOW);
}

void newDevice(DW1000Device *device)
{
  int networkNumber = DW1000Ranging.getNetworkDevicesNumber();
  int tagNumber = DW1000Ranging.getTagDevicesNumber();

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

  String toDisplay = "ANC : ";
  toDisplay += networkNumber;
  toDisplay += "\nTAG : ";
  toDisplay += tagNumber;
  display.displayMsg(Text(toDisplay, 3, 64, 0));

  digitalWrite(PIN_LED_OK, HIGH);
  digitalWrite(PIN_LED_FAIL, LOW);
}

void inactiveAncDevice(DW1000Device *device)
{
  int networkNumber = DW1000Ranging.getNetworkDevicesNumber() -1;
  int tagNumber = DW1000Ranging.getTagDevicesNumber();

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

  String toDisplay = "ANC : ";
  toDisplay += networkNumber;
  toDisplay += "\nTAG : ";
  toDisplay += tagNumber;
  display.displayMsg(Text(toDisplay, 3, 64, 0));

  if (!(a1Connected || a2Connected || a3Connected || a4Connected))
  {
    p[0] = -1;
    p[1] = -1;
  }

  if(tagNumber + networkNumber == 0){
    digitalWrite(PIN_LED_OK, LOW);
    digitalWrite(PIN_LED_FAIL, HIGH);
  }
}

void inactiveTagDevice(DW1000Device *device)
{
  int networkNumber = DW1000Ranging.getNetworkDevicesNumber();
  int tagNumber = DW1000Ranging.getTagDevicesNumber() -1;

  String toDisplay = "ANC : ";
  toDisplay += networkNumber;
  toDisplay += "\nTAG : ";
  toDisplay += tagNumber;

  display.displayMsg(Text(toDisplay, 3, 64, 0));

  if (tagNumber + networkNumber == 0)
  {
    digitalWrite(PIN_LED_OK, LOW);
    digitalWrite(PIN_LED_FAIL, HIGH);
  }
}

void blinkDevice(DW1000Device *device){
  int networkNumber = DW1000Ranging.getNetworkDevicesNumber();
  int tagNumber = DW1000Ranging.getTagDevicesNumber();
 
  String toDisplay = "ANC : ";
  toDisplay += networkNumber;
  toDisplay += "\nTAG : ";
  toDisplay += tagNumber;

  display.displayMsg(Text(toDisplay, 3, 64, 0));

  digitalWrite(PIN_LED_OK, HIGH);
  digitalWrite(PIN_LED_FAIL, LOW);
}

void setup() {
  Serial.begin(SERIALTALKS_BAUDRATE);
  talks.begin(Serial);

  talks.bind(GET_POSITION_OPCODE, GET_POSITION);

#if 0
  EEPROM.write(EEPROM_NUM_TAG, currentBeaconNumber);
  EEPROM.commit();
#endif
  currentBeaconNumber = EEPROM.read(EEPROM_NUM_TAG);

  //init the configuration
  DW1000Ranging.initCommunication(PIN_UWB_RST, PIN_SPICSN, PIN_IRQ, PIN_SPICLK, PIN_SPIMISO, PIN_SPIMOSI); //Reset, CS, IRQ pin
  //define the sketch as anchor. It will be great to dynamically change the type of module
  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachNewDevice(newDevice);
  DW1000Ranging.attachInactiveAncDevice(inactiveAncDevice);
  DW1000Ranging.attachInactiveTagDevice(inactiveTagDevice);
  DW1000Ranging.attachBlinkDevice(blinkDevice);
  //Enable the filter to smooth the distance
  DW1000Ranging.useRangeFilter(true);
  DW1000Ranging.setRangeFilterValue(5);

  //we start the module as a tag
  DW1000Ranging.startAsTag("7D:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY, TAG_SHORT_ADDRESS[currentBeaconNumber], MASTER_TAG_ADDRESS == TAG_SHORT_ADDRESS[currentBeaconNumber]);

  display.init();
  display.flipScreenVertically();
  display.setTextAlignment(TEXT_ALIGN_CENTER);

  xTaskCreatePinnedToCore(
      loopCore0,   /* Function to implement the task */
      "loopCore0", /* Name of the task */
      10000,       /* Stack size in words */
      NULL,        /* Task input parameter */
      0,           /* Priority of the task */
      NULL,        /* Task handle. */
      0);   /* Core where the task should run */

  pinMode(PIN_LED_FAIL, OUTPUT);
  pinMode(PIN_LED_OK, OUTPUT);
  digitalWrite(PIN_LED_OK, HIGH);
  digitalWrite(PIN_LED_FAIL, HIGH);
  display.displayMsg(Text("SYNC", 3, 64, 0));
  if (TAG_SHORT_ADDRESS[currentBeaconNumber] == MASTER_TAG_ADDRESS)
    display.displayMsg(Text("GROS\nROBOT", 4, 64, 0));
  else
    display.displayMsg(Text("PETIT\nROBOT", 4, 64, 0));
}

void loop() {   // loop on core 1
  DW1000Ranging.loop();
  talks.execute();
}


