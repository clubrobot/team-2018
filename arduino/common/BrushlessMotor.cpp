#include "BrushlessMotor.h"


void BrushlessMotor::attach(int pin)
{
    m_esc.attach(pin, MIN_PULSEWIDTH, MAX_PULSEWIDTH);
    PeriodicProcess::setTimestep(0.001);
}

void BrushlessMotor::detach()
{
    m_esc.detach();
}

void BrushlessMotor::enableMotor()
{
    m_enabled = true;
    m_esc.write(m_velocity);
}

void BrushlessMotor::disableMotor()
{
    m_enabled = false;
    m_esc.write(MIN_PULSEWIDTH);
}

int BrushlessMotor::readMicroseconds()
{
    return m_esc.readMicroseconds();
}

void BrushlessMotor::setVelocity(int velocity)
{
    if(velocity >= MIN_VELOCITY && velocity <= MAX_VELOCITY){
        m_velocity = (int) map(velocity,0,100,MIN_PULSEWIDTH,MAX_PULSEWIDTH);
    } else {
        m_velocity = velocity > MAX_VELOCITY ? MAX_PULSEWIDTH : MIN_PULSEWIDTH;
    }
    if (m_enabled == true) {
        m_esc.writeMicroseconds(m_velocity);
    }
    else {
        m_esc.writeMicroseconds(MIN_PULSEWIDTH);
    }
}

void BrushlessMotor::setPulsewidth(int pulsewidth) {
	m_esc.writeMicroseconds(pulsewidth);
}

void BrushlessMotor::setupRise(bool start){
    if(start){ 
        timeDelay = millis();           //ESC just went back on -> start counting time
    } else {
        if(timeDelay > 5000){
            this.setPulsewidth(MIN_PULSEWIDTH);   //After 5 seconds, write MIN_PULSEWIDTH to setup ESC min
        }
        if(timeDelay > 6200){
            this.disableSetup();        //End of setup
        }
    }
}

void BrushlessMotor::setupFall(){
    this.setPulsewidth(MAX_PULSEWIDTH);
}

void BrushlessMotor::enableSetup(){
	PeriodicProcess::enable();
}

void BrushlessMotor::disableSetup(){
	PeriodicProcess::disable();
}

void BrushlessMotor::updateSetup(){
	PeriodicProcess::update();
}

void BrushlessMotor::process(){
    this.setupRise(false);
}