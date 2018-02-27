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

bool BrushlessMotor::setVelocity(int velocity)
{
    if(velocity >= MIN_VELOCITY && velocity <= MAX_VELOCITY){
        m_velocity = (int) map(velocity,0,100,MIN_PULSEWIDTH,MAX_PULSEWIDTH);
    } else {
        m_velocity = velocity > MAX_VELOCITY ? MAX_PULSEWIDTH : MIN_PULSEWIDTH;
    }
    if (m_enabled == true) {
        return this->setPulsewidth(m_velocity);
    }
    else {
        return this->setPulsewidth(MIN_PULSEWIDTH);
    }
}

bool BrushlessMotor::setPulsewidth(int pulsewidth) {
    if(processingSetup){
    	m_esc.writeMicroseconds(pulsewidth);
        return true;
    } else {
        return false;
    }
}

void BrushlessMotor::setupRise(bool start){
    processingSetup = true;
    if(start){ 
        timeDelay = millis();           //ESC just went back on -> start counting time
    } else {
        if(timeDelay > 3000){
            m_esc.writeMicroseconds(MIN_PULSEWIDTH);   //After 5 seconds, write MIN_PULSEWIDTH to setup ESC min
        }
        if(timeDelay > 4200){
            this->disableSetup();        //End of setup
            processingSetup = false;
        }
    }
}

void BrushlessMotor::setupFall(){
    processingSetup = true;
    m_esc.writeMicroseconds(MAX_PULSEWIDTH);
}

void BrushlessMotor::enableSetup(){
	enable();
}

void BrushlessMotor::disableSetup(){
	disable();
}

void BrushlessMotor::updateSetup(){
	PeriodicProcess::update();
}

void BrushlessMotor::process(float timestep){
    this->setupRise(false);
}