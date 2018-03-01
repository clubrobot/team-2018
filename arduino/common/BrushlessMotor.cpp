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
    m_esc.writeMicroseconds(MIN_PULSEWIDTH);
}

int BrushlessMotor::readMicroseconds()
{
    return m_esc.readMicroseconds();
}

int BrushlessMotor::setVelocity(int velocity)
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

int BrushlessMotor::setPulsewidth(int pulsewidth) {
    if(!processingSetup){
    	m_esc.writeMicroseconds(pulsewidth);
        return 1;
    } else {
        return 0;
    }
}

void BrushlessMotor::startupProcess(bool start){
    processingStartup = true;
    if(start){
        m_esc.writeMicroseconds(MIN_PULSEWIDTH);
        timeDelay = millis();           //ESC just went back on -> start counting time
    } else {
        if(millis() - timeDelay > 5000){
            m_esc.writeMicroseconds(MIN_PULSEWIDTH);
            this->disableStartup();        //Stay at min velocity for correct ESC startup
            processingStartup = false;
        }
    }
}

void BrushlessMotor::enableStartup(){
	enable();
}

void BrushlessMotor::disableStartup(){
	disable();
}

void BrushlessMotor::updateStartup(){
	PeriodicProcess::update();
}

void BrushlessMotor::process(float timestep){
    this->setupRise(false);
}