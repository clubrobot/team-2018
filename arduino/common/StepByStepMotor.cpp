#include "StepByStepMotor.h"
#include "ShiftRegister.h"

#define FORWARD  0
#define BACKWARD 1

#define _BV(bit) (1 << (bit))

extern ShiftRegister shift;

StepByStepMotor::StepByStepMotor()
{}

void StepByStepMotor::attach(int step, int dir, int enable, int rst, int sleep)
{
	m_step    = step;
	m_dir     = dir;
	m_enable  = enable;
	m_rst 	  = rst;
	m_sleep	  = sleep;

	pinMode(m_step, OUTPUT);

	m_state = WATING_STATE;
}

void StepByStepMotor::begin()
{
	shift.SetLow(m_enable);
	shift.SetHigh(m_dir);
	shift.SetHigh(m_sleep);
	shift.SetHigh(m_rst);

	m_current_pos = 0;
	m_last_pos = 0;

	m_en = true;
	
	m_p = 1;
}

void StepByStepMotor::step()
{
	PORTB &= ~(_BV(5));
    delayMicroseconds(15);
    PORTB |= _BV(5);            

    if(m_speed < 31)
  	{
    	delay(1000 / m_speed);
    	delayMicroseconds(1000 * (1000 / m_speed - int(1000 / m_speed)) - 110);
  	}
  	else
    	delayMicroseconds(1000000 / m_speed - 110);
}
void StepByStepMotor::set_position(double position)
{
	long abssteps, steps;

	m_current_pos = position;

	steps = (m_current_pos - m_last_pos) * P_MM;

	abssteps = (steps>0 ? steps : -steps);

	m_pAcc = abssteps / (1.0 + ACC/DECC);
	m_pDec = abssteps - m_pAcc;

	if(steps > 0)
		shift.write(m_dir,FORWARD);
	else
		shift.write(m_dir,BACKWARD);

	m_state = ACC_STATE;
}

void StepByStepMotor::update()
{

	switch(m_state)
	{
		case ACC_STATE :
			if(m_p <= m_pAcc)
			{
				m_speed = sqrt((2*m_p-1)*ACC);
		   		if(m_speed > PLAT)
		    		m_speed = PLAT;

				step();
				m_p++;
			}
			else
			{
				m_state = DEC_STATE;
				m_p = m_pDec;
			}
			break;

		case DEC_STATE :
			if(m_p > 0)
			{
				m_speed = sqrt(2*m_p*DECC);
		   		if(m_speed > PLAT)
		    		m_speed = PLAT;

				step();
				m_p--;
			}
			else
			{
				m_state = WATING_STATE;
				m_p = 0;
				m_last_pos = m_pos;
			}
			break;

		case WATING_STATE :
			break;

	}
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