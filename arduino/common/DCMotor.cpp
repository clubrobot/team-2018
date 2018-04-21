#include <Arduino.h>
#include <EEPROM.h>

#include "DCMotor.h"
#include "ShiftRegister.h"

#define FORWARD  0
#define BACKWARD 1

#ifdef USE_SHIFTREG
	extern ShiftRegister shift;
	#define SwitchPin(EN_pin,Mode) (shift.write(DirPin,Mode))
#else
	#define SwitchPin(EN_pin,Mode) (digitalWrite(EN_pin, Mode))
#endif



void DCMotor::attach(int EN, int PWM, int DIR)
{
	m_EN  = EN;
	m_PWM = PWM;
	m_DIR = DIR;
#ifndef USE_SHIFTREG
	pinMode(m_EN, OUTPUT);
#endif
	pinMode(m_PWM, OUTPUT);
	pinMode(m_DIR, OUTPUT);
}

void DCMotor::update()
{
	if (m_velocity != 0)
	{
		int PWM = m_velocity / (2 * M_PI * m_wheelRadius) * m_constant * 255;
		if (PWM <   0) PWM *= -1;
		if (PWM > 255 * m_maxPWM) PWM = 255 * m_maxPWM;
		SwitchPin(m_EN, HIGH);
		analogWrite(m_PWM, PWM);
		digitalWrite(m_DIR, (m_velocity * m_constant * m_wheelRadius > 0) ? FORWARD : BACKWARD);
	}
	else
	{
		SwitchPin(m_EN, LOW);
	}
}

float DCMotor::getMaxVelocity() const
{
	return abs((2 * M_PI * m_wheelRadius) / m_constant) * m_maxPWM;
}

void DCMotor::load(int address)
{
	EEPROM.get(address, m_wheelRadius); address += sizeof(m_wheelRadius);
	EEPROM.get(address, m_constant);    address += sizeof(m_constant);
	EEPROM.get(address, m_maxPWM);      address += sizeof(m_maxPWM);
}

void DCMotor::save(int address) const
{
	EEPROM.put(address, m_wheelRadius); address += sizeof(m_wheelRadius);
	EEPROM.put(address, m_constant);    address += sizeof(m_constant);
	EEPROM.put(address, m_maxPWM);      address += sizeof(m_maxPWM);
}

void DCMotorsDriver::attach(int RESET, int FAULT)
{
	m_RESET = RESET;
	m_FAULT = FAULT;
#ifndef USE_SHIFTREG
	pinMode(m_RESET, OUTPUT);
	pinMode(m_FAULT, INPUT);
#endif
}

void DCMotorsDriver::reset()
{
	SwitchPin(m_RESET, LOW);
	delayMicroseconds(10); // One may adjust this value.
	SwitchPin(m_RESET, HIGH);
}

bool DCMotorsDriver::isFaulty()
{
#ifndef USE_SHIFTREG
	return (digitalRead(m_FAULT) == LOW);
#else
	return -1;
#endif
}
