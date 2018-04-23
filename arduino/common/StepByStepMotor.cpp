#include "StepByStepMotor.h"
#include "ShiftRegister.h"

#define FORWARD  0
#define BACKWARD 1

extern ShiftRegister shift;

StepByStepMotor::StepByStepMotor(){}

void StepByStepMotor::attach(int step, int dir, int enable, int rst, int sleep)
{
	m_step    = step;
	m_dir     = dir;
	m_enable  = enable;
	m_rst 	  = rst;
	m_sleep	  = sleep;

	pinMode(m_step, OUTPUT);

}

void StepByStepMotor::begin()
{
	shift.SetLow(m_enable);
	shift.SetHigh(m_dir);
	shift.SetHigh(m_sleep);
	shift.SetHigh(m_rst);

	m_current_pos = 0;
	m_last_pos = 0;

	//set_speed in rpm
	set_speed(50);

	m_en = true;
}

void StepByStepMotor::step(int dir)
{
	if(dir == FORWARD)
		shift.SetHigh(m_dir);
	else
		shift.SetLow(m_dir);

	digitalWrite(m_step, LOW);
    delayMicroseconds(m_speed/2);
    digitalWrite(m_step, HIGH); 
    delayMicroseconds(m_speed/2);
}

void StepByStepMotor::update()
{
	m_current_pos = m_pos;

	int dist = ((m_current_pos - m_last_pos)/TURN_DIST) * STEP_BY_REV;

	while(dist != 0)
	{
		if(dist > 0)
		{
			step(FORWARD);
			dist--;
		}
		else
		{
			step(BACKWARD);
			dist++;
		}
	}

	m_last_pos = m_pos;

}

void StepByStepMotor::enable()
{
	shift.SetLow(m_enable);
	m_en = true;
}

void StepByStepMotor::disable()
{
	shift.SetHigh(m_enable);
	m_en = false;
}