#ifndef __BRUSHLESSMOTOR_H__
#define __BRUSHLESSMOTOR_H__

#include <Arduino.h>
#include <Servo.h>
#include "SerialTalks.h"


#define MIN_PULSEWIDTH   (int)   1450     // the shortest pulse sent to a ESC  
#define MAX_PULSEWIDTH   (int)   2400     // the longest pulse sent to a ESC
#define MIN_VELOCITY             0
#define MAX_VELOCITY             100

class BrushlessMotor{

public:
	BrushlessMotor(): m_enabled(false), m_velocity(0){}

	void attach(int PIN);
    void detach();

	void enable();
	void disable();
    void setVelocity   (float velocity);

    float getVelocity   () const {return m_velocity;}
    bool  isEnabled     () const {return m_enabled;}

    int readMicroseconds();

private:

    Servo m_esc;
    bool  m_enabled ;

    int m_velocity; // in %
};

#endif // __BRUSHLESSMOTOR_H__