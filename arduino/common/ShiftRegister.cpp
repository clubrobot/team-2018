#include "ShiftRegister.h"

void ShiftRegister::attach(int latchpin, int clockpin, int datapin)
{
	m_LATCH = latchpin;
	m_CLOCK = clockpin;
	m_DATA  = datapin;

	pinMode(m_LATCH, OUTPUT);
	pinMode(m_CLOCK, OUTPUT);
	pinMode(m_DATA , OUTPUT);
}

void ShiftRegister::SetHigh(int pos)
{
	m_register |= (1 << pos); 
	update();
}

void ShiftRegister::SetLow(int pos)
{
	m_register &= ~(1 << pos); 
	update();
}

void ShiftRegister::update()
{
	digitalWrite(m_LATCH, LOW);
    shiftOut(m_DATA, m_DATA, LSBFIRST, m_register);
    digitalWrite(m_LATCH, HIGH);
}