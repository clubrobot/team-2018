#include "StepByStepMotor.h"
#include "ShiftRegister.h"

#define FORWARD  0
#define BACKWARD 1

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
	set_speed(100);

	m_en = true;
}

void StepByStepMotor::step(int dir)
{
	shift.write(m_dir,(dir == 1 ? FORWARD : BACKWARD));

	/************************comment to disable ***************************/
	digitalWrite(m_step, LOW);
    delayMicroseconds(5);
    digitalWrite(m_step, HIGH); 
    

    //adjust tempo:  
  	if(m_speed < 31)
  	{
    	delay(1000 / m_speed);
    	delayMicroseconds(1000 * (1000 / m_speed - int(1000 / m_speed)) - 110);
  	}
  	else
    	delayMicroseconds(1000000 / m_speed - 110);

    /**************************************************************************/

    /****************** Uncomment : safe version ******************************/
	// digitalWrite(m_step, LOW);
 //    delayMicroseconds(m_speed/2);
 //    digitalWrite(m_step, HIGH); 
	// delayMicroseconds(m_speed/2);
	/**************************************************************************/
}

void StepByStepMotor::update()
{
	long abssteps, pAcc, pDec, p, steps;

	m_current_pos = m_pos;

	steps = (m_current_pos - m_last_pos) * P_MM;

	/***********************comment to disable*******************************/
	abssteps = (steps>0 ? steps : -steps);

	pAcc = long(abssteps / (1.0 + ACC/DEC) + 0.5);
	pDec = steps - pAcc;

	for(p=1; p<=pAcc; p++)
  	{
	    m_speed = sqrt((2*p-1)*ACC);
	    if(m_speed > PLAT)
	    	m_speed = PLAT;

		step(steps > 0 ? FORWARD : BACKWARD);
	    
  	}
	for(p = pDec; p >=0 ; p--)
	{
		m_speed = sqrt(2*p*DEC);
		if(m_speed > PLAT)
			m_speed = PLAT;

		step(steps > 0 ? FORWARD : BACKWARD);
	}
	/****************************************************************************/

	/***********************Uncomment : safe version****************************/
	// while(steps != 0)
	// {
	// 	if(steps > 0)
	// 	{
	// 		step(FORWARD);
	// 		steps--;
	// 	}
	// 	else
	// 	{
	// 		step(BACKWARD);
	// 		steps++;
	// }
	/***************************************************************************/

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