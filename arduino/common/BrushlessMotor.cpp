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
        m_velocity = velocity > MAX_VELOCITY ? MAX_VELOCITY : MIN_VELOCITY;
    }
    if (m_enabled == true) {
        m_esc.writeMicroseconds(m_velocity);
    }
    else {
        m_esc.writeMicroseconds(MIN_PULSEWIDTH);
    }
    //delay(100);
}

void BrushlessMotor::setPulsewidth(int pulsewidth) {
	m_esc.writeMicroseconds(pulsewidth);
}
