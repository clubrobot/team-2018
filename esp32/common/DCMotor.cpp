#include <Arduino.h>
#include <EEPROM.h>

#include "DCMotor.h"

#define PWM_BIT 8      
#define FORWARD  0
#define BACKWARD 1


void DCMotor::attach(int EN, int PWM, int PWMChanel,int freq, int DIR)
{
	m_EN  = EN;
	m_PWM = PWM;
	m_PWMChanel = PWMChanel;
	m_DIR = DIR;
	pinMode(m_EN, OUTPUT);

	ledcSetup(m_PWMChanel, freq, PWM_BIT);
	ledcAttachPin(m_PWM, m_PWMChanel);
	pinMode(m_DIR, OUTPUT);
}

void DCMotor::update()
{
	if (m_velocity != 0)
	{
		int PWM = m_velocity / (2 * M_PI * m_wheelRadius) * m_constant * 255;
		if (PWM <   0) PWM *= -1;
		if (PWM > 255 * m_maxPWM) PWM = 255 * m_maxPWM;
		digitalWrite(m_EN, HIGH);
		ledcWrite(m_PWMChanel, PWM);
		digitalWrite(m_DIR, (m_velocity * m_constant * m_wheelRadius > 0) ? FORWARD : BACKWARD);
	}
	else
	{
		digitalWrite(m_EN, LOW);
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
	EEPROM.commit();
}

void DCMotorsDriver::attach(int RESET, int FAULT)
{
	m_RESET = RESET;
	m_FAULT = FAULT;
	pinMode(m_RESET, OUTPUT);
	pinMode(m_FAULT, INPUT);
}

void DCMotorsDriver::reset()
{
	digitalWrite(m_RESET, LOW);
	delayMicroseconds(10); // One may adjust this value.
	digitalWrite(m_RESET, HIGH);
}

bool DCMotorsDriver::isFaulty()
{
	return (digitalRead(m_FAULT) == LOW);
}
