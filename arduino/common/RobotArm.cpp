#include <Arduino.h>
#include <Servo.h>
#include "RobotArm.h"
#include "ShiftRegAX12.h" 
#include "SoftwareSerial.h"

extern ShiftRegAX12 servoax;

RobotArm::RobotArm(double x, double y, double z, double theta, float speed)
{
	m_x = x * -1; //revert x
	m_y = y;
	m_z = z;
	m_theta = theta;

	m_speed = speed;
}

void RobotArm::attach(unsigned char A1_id, unsigned char A2_id, unsigned char A3_id, unsigned char servo)
{
	m_A1_id = A1_id;
	m_A2_id = A2_id;
	m_A3_id = A3_id;

	m_gripper.attach(servo);
}

void RobotArm::begin()
{
	//Set AX config
	//Broadcast address
	servoax.attach(254);
	servoax.setSRL(1); // Respond only to READ_DATA instructions
	servoax.setLEDAlarm(32); // max torque only
	servoax.setShutdownAlarm(32); // max torque only
	servoax.setMaxTorque(1023);
	servoax.setEndlessMode(OFF);
	servoax.hold(OFF);

	//Set start position
	ReachPosition(m_x, m_y, m_z, m_theta);
}

bool RobotArm::solve_angles(double x, double y)
{
	double D1,D2,R2;
	//First, get the length of line dist.	
	double dist = distance(x, y);
	//Calculating angle D1 is trivial. Atan2 is a modified arctan() function that returns unambiguous results.	
	D1 = atan2(y, x);
	//D2 can be calculated using the law of cosines where a = dist, b = len1, and c = len2.	
	if(!lawOfCosines(dist, ARM_LEN_1, ARM_LEN_2, &D2)) return false;
	//Then A1 is simply the sum of D1 and D2.	
	m_A1 = convert_deg(D1 + D2);
	if(!lawOfCosines(ARM_LEN_1, ARM_LEN_2, dist, &R2)) return false;
	//A2 can also be calculated with the law of cosine, but this time with a = len1, b = len2, and c = dist.	
	m_A2 = convert_deg(R2);

	return true;
}
bool solve_coords(double x, double y, double th)
{

	m_x_max = (ARM_LEN_1*cos(AX1_MAX_ANGLE)) + ARM_LEN_2*cos(AX1_MAX_ANGLE + AX2_MAX_ANGLE);
	m_y_max = (ARM_LEN_1*sin(AX1_MAX_ANGLE)) + ARM_LEN_2*sin(AX1_MAX_ANGLE + AX2_MAX_ANGLE);
	m_theta_max = 0;

	m_x_min = (ARM_LEN_1*cos(AX1_MIN_ANGLE)) + ARM_LEN_2*cos(AX1_MIN_ANGLE + AX2_MIN_ANGLE);
	m_y_min = (ARM_LEN_1*sin(AX1_MIN_ANGLE)) + ARM_LEN_2*sin(AX1_MIN_ANGLE + AX2_MIN_ANGLE);
	m_theta_min = 0;
}

void RobotArm::ReachPosition(double x, double y, double z, double theta)
{
	m_x = x; //revert x
	m_y = y;
	m_z = z;

	double t1,t2,t3;

	if(solve_angles(m_x,m_y))
	{
		//calculate gripper angle
		m_A3 = (360-(m_A1+m_A2)) + theta;

		//calculate real position with offset
		t1 = m_A1 + ARM1_OFFSET;

		t2 = m_A2 - ARM2_OFFSET;

		t3 = m_A3 + ARM3_OFFSET;

		// send pos to AX12 servos
		servoax.attach(m_A1_id);
		servoax.setMaxTorqueRAM(1023);
		servoax.moveSpeed((float)t1, m_speed);
		servoax.detach();

		servoax.attach(m_A2_id);
		servoax.setMaxTorqueRAM(1023);
		servoax.moveSpeed((float)t2, m_speed);
		servoax.detach();

		servoax.attach(m_A3_id);
		servoax.setMaxTorqueRAM(1023);
		servoax.moveSpeed((float)t3, 50);
		servoax.detach();
		//TODO : add pap Z axis
	}

}

void RobotArm::set_angles(float A1, float A2, float A3)
{
	// send pos to AX12 servos
	servoax.attach(m_A1_id);
	servoax.moveSpeed((float)A1, m_speed);

	servoax.attach(m_A2_id);
	servoax.moveSpeed((float)A2, m_speed);

	servoax.attach(m_A3_id);
	servoax.moveSpeed((float)A3, m_speed);
}


void RobotArm::set_x(double x)
{
	m_x = x*-1;
	ReachPosition(m_x, m_y, m_z,m_theta);
}

void RobotArm::set_y(double y)
{
	m_y = y;
	ReachPosition(m_x, m_y, m_z, m_theta);
}

void RobotArm::set_z(double z)
{
	m_z = z;	
	//TODO : add pap 
}

void RobotArm::set_theta(double theta)
{
	m_theta = theta;
	ReachPosition(m_x, m_y, m_z, m_theta);
}

void RobotArm::set_speed(float speed)
{
	m_speed = speed;
}

void RobotArm::close_gripper()
{
	m_gripper.write(GRIPPER_CLOSE);
}

void RobotArm::open_gripper()
{
	m_gripper.write(GRIPPER_OPEN);
}

double RobotArm::get_A1theo()
{
	return m_A1;
}

double RobotArm::get_A2theo()
{
	return m_A2;
}

double RobotArm::get_A3theo()
{
	return m_A3;
}

double RobotArm::get_A1()
{
	servoax.attach(m_A1_id);
	return servoax.readPosition();
}

double RobotArm::get_A2()
{
	servoax.attach(m_A2_id);
	return servoax.readPosition();
}

double RobotArm::get_A3()
{
	servoax.attach(m_A3_id);
	return servoax.readPosition();
}

bool RobotArm::lawOfCosines(double a, double b, double c, double *A)
{
	double den,cc;
	den = 2*a*b;

	if(den == 0) return false;

	cc =(a*a + b*b - c*c) / den;

	if(cc>1 || cc<-1) return false;

	*A = acos(cc);

	return true;
}

double RobotArm::distance(double x, double y)
{
	return sqrt(x*x + y*y);
}

double RobotArm::convert_deg(double rad)
{
	return rad * 180 / M_PI;
}