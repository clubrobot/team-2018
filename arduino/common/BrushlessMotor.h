#ifndef __BRUSHLESSMOTOR_H__
#define __BRUSHLESSMOTOR_H__

#include <Arduino.h>
#include <Servo.h>

#define MIN_PULSEWIDTH   (int)   1000     // the shortest pulse sent to a ESC  
#define MAX_PULSEWIDTH   (int)   2000     // the longest pulse sent to a ESC
#define MIN_VELOCITY             37

class BrushlessMotor{

public:
	BrushlessMotor(): m_enabled(false), m_velocity(0), m_wheelRadius(1 / (2 * M_PI)), m_constant(1){}

	void attach(int PIN);
    void detach();

    void setVelocity   (float velocity){m_velocity = velocity; update();}

    void setConstant   (float constant)   {m_constant    = constant;    update();}
    void setWheelRadius(float wheelRadius){m_wheelRadius = wheelRadius; update();}


	void enable();
	void disable();

    float getVelocity   () const {return m_velocity;}
    float getConstant   () const {return m_constant;}
    float getWheelRadius() const {return m_wheelRadius;}
    bool  isEnabled     () const {return m_enabled;}

    int retour();

    float getMaxVelocity() const;

    void load(int address);
    void save(int address) const;

private:

	void update();

    Servo m_esc;
    bool  m_enabled ;

    float m_velocity; // in mm/s (millimeters per second)
    float m_wheelRadius; // in mm
    float m_constant; // (60 * reduction_ratio / velocity_constant_in_RPM) / supplied_voltage_in_V

};

#endif // __BRUSHLESSMOTOR_H__