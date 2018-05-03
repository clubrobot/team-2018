#ifndef OLED_DISPLAY_H
#define OLED_DISPLAY_H

#include "Arduino.h"
#include "SSD1306.h"
#include <Wire.h>

#define NB_MSG_MAX 5
#define DEFAULT_DURATION 0
#define DEFAULT_PERSISTENCE 1000

class OLEDdisplay;

class Text {
public:
  Text(const String text = "",const int id = -1, const int16_t x = 0, const int16_t y = 0) :_id(id), _x(x), _y(y), _value(text) {}
  void clear();

private:
    int16_t _x;
    int16_t _y;
    String _value;
    int _id;

    friend class OLEDdisplay;
};

class OLEDdisplay : public SSD1306{
public:
  OLEDdisplay(uint8_t address, uint8_t pin_sda, uint8_t pin_scl) : SSD1306(address, pin_sda, pin_scl),
                                                                   _duration(DEFAULT_DURATION),
                                                                   _msgPersistence(DEFAULT_PERSISTENCE),
                                                                   _index(0)
    { 
        _displayStartTime = millis();
        _logStartTime = millis();
    }

  void drawString(int16_t x, int16_t y, String text);

  void update();
  void log(String text, unsigned long duration = 10000);
  void displayMsg(Text msg);
  void clearMsg(int id);
  void clearAll();

private:
  unsigned long _logStartTime;
  unsigned long _duration;
  unsigned long _displayStartTime;
  unsigned long _msgPersistence;

  Text _log;
  Text _msg[NB_MSG_MAX];
  int _msgNumber; // number of msg
  int _index;

};

#endif