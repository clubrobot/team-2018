#include <Arduino.h>
#include "BrushlessMotor.h"
#include <Servo.h>
#include <EEPROM.h>

#include "SerialTalks.h"


void BrushlessMotor::attach(int PIN)
{
    m_esc.attach(PIN, MIN_PULSEWIDTH, MAX_PULSEWIDTH);
}

void BrushlessMotor::detach()
{
    m_esc.detach();
}

void BrushlessMotor::enable()
{
    m_enabled = true;
    update();
}

void BrushlessMotor::disable()
{
    m_enabled = false;
    update();
}

int BrushlessMotor::retour()
{
    return m_esc.readMicroseconds();
}
void BrushlessMotor::update()
{
    if ((m_velocity >= MIN_VELOCITY) && (m_enabled == true))
    {
        //int SPEED = m_velocity / (2 * M_PI * m_wheelRadius) * m_constant * 180;
        //if (SPEED > 180) SPEED = 180;
        int SPEED = map(m_velocity,0,100,0,180);
        m_esc.write(SPEED);
    }
    else
    {
        m_esc.write(MIN_VELOCITY);
    }
    delay(30);
}

float BrushlessMotor::getMaxVelocity() const
{
    //return abs((2 * M_PI * m_wheelRadius) / m_constant);
    return 100;
}

void BrushlessMotor::load(int address)
{
    EEPROM.get(address, m_wheelRadius); address += sizeof(m_wheelRadius);
}

void BrushlessMotor::save(int address) const
{
    EEPROM.put(address, m_wheelRadius); address += sizeof(m_wheelRadius);
}