#include "BrushlessMotor.h"


void BrushlessMotor::attach(int pin)
{
    m_esc.attach(pin, MIN_PULSEWIDTH, MAX_PULSEWIDTH);
}

void BrushlessMotor::detach()
{
    m_esc.detach();
}

void BrushlessMotor::enable()
{
    m_enabled = true;
    m_esc.write(m_velocity);
}

void BrushlessMotor::disable()
{
    m_enabled = false;
    m_esc.write(MIN_VELOCITY);
}

int BrushlessMotor::readMicroseconds()
{
    return m_esc.readMicroseconds();
}

void BrushlessMotor::setVelocity(int velocity)
{
    if(m_velocity >= MIN_VELOCITY && m_velocity <= MAX_VELOCITY){
        m_velocity = (int) map(m_velocity,0,100,0,180);
    } else {
        m_velocity = velocity > MAX_VELOCITY ? MAX_VELOCITY : MIN_VELOCITY;
    }
    if (m_enabled == true) {
        m_esc.write(m_velocity);
    }
    else {
        m_esc.write(MIN_VELOCITY);
    }
    //delay(100);
}