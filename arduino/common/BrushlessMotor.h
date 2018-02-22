#ifndef __BRUSHLESSMOTOR_H__
#define __BRUSHLESSMOTOR_H__

#include <Arduino.h>
#include <Servo.h>
#include "SerialTalks.h"
#include "PeriodicProcess.h"


#define MIN_PULSEWIDTH           1000     // the shortest pulse sent to a ESC  
#define MAX_PULSEWIDTH           2000     // the longest pulse sent to a ESC
#define MIN_VELOCITY             0
#define MAX_VELOCITY             100

class BrushlessMotor: public PeriodicProcess {

public:
	BrushlessMotor(): m_enabled(false), m_velocity(0), timeDelay(0){}

	void attach(int PIN);
    void detach();

	void enableSetup();
	void disableSetup();
    void updateSetup();
    void enableMotor();
    void disableMotor();
    void setVelocity(int velocity);
	void setPulsewidth(int pulsewidth);
    void update();
    void setupRise();
    void setupFall();

    float getVelocity() const {return map(m_velocity,0,180,0,100);}
    bool  isEnabled() const {return m_enabled;}

    int readMicroseconds();

private:

    Servo m_esc;
    bool  m_enabled ;
    unsigned long timeDelay;
    int m_velocity; // in %
    virtual void process(float timestep);
};

#endif // __BRUSHLESSMOTOR_H__