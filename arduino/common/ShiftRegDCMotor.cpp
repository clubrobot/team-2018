#include <Arduino.h>
#include <EEPROM.h>

#include "ShiftRegDCMotor.h"
#include "ShiftRegister.h"

#define FORWARD  0
#define BACKWARD 1

extern ShiftRegister reg;

void ShiftRegDCMotor::attach(int EN, int PWM, int DIRPOS)
{
	m_EN  = EN;
	m_PWM = PWM;
	m_DIRPOS = DIRPOS;

	pinMode(m_EN, OUTPUT);
	pinMode(m_PWM, OUTPUT);
}

void ShiftRegDCMotor::update()
{
	if (m_velocity != 0)
	{
		int PWM = m_velocity / (2 * M_PI * m_wheelRadius) * m_constant * 255;
		if (PWM <   0) PWM *= -1;
		if (PWM > 255 * m_maxPWM) PWM = 255 * m_maxPWM;
		digitalWrite(m_EN, HIGH);
		analogWrite(m_PWM, PWM);

		if(m_velocity * m_constant * m_wheelRadius > 0)
			reg.SetHigh(m_DIRPOS);
		else 
			reg.SetLow(m_DIRPOS);
	}
	else
	{
		digitalWrite(m_EN, LOW);
	}
}

float ShiftRegDCMotor::getMaxVelocity() const
{
	return abs((2 * M_PI * m_wheelRadius) / m_constant) * m_maxPWM;
}

void ShiftRegDCMotor::load(int address)
{
	EEPROM.get(address, m_wheelRadius); address += sizeof(m_wheelRadius);
	EEPROM.get(address, m_constant);    address += sizeof(m_constant);
	EEPROM.get(address, m_maxPWM);      address += sizeof(m_maxPWM);
}

void ShiftRegDCMotor::save(int address) const
{
	EEPROM.put(address, m_wheelRadius); address += sizeof(m_wheelRadius);
	EEPROM.put(address, m_constant);    address += sizeof(m_constant);
	EEPROM.put(address, m_maxPWM);      address += sizeof(m_maxPWM);
}

void ShiftRegDCMotorsDriver::attach(int RESET, int FAULT)
{
	m_RESET = RESET;
	m_FAULT = FAULT;
}

void ShiftRegDCMotorsDriver::reset()
{
	reg.SetLow(m_RESET);
	delayMicroseconds(10); // One may adjust this value.
	reg.SetHigh(m_RESET);
}

bool ShiftRegDCMotorsDriver::isFaulty()
{
	return (digitalRead(m_FAULT) == LOW);
}
