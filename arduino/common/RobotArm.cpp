#include "RobotArm.h"
#include "AX12.h"


extern AX12 servoax;

RobotArm::RobotArm(double x, double y, double z, double theta)
{
	m_x = x * -1; //revert x
	m_y = y;
	m_z = z;
	m_theta = theta;
}

void RobotArm::attach(int A1_id, int A2_id, int A3_id)
{
	m_A1_id = A1_id;
	m_A2_id = A2_id;
	m_A3_id = A3_id;
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

void RobotArm::solve_angles(double x, double y)
{
	double D1,D2;
	//First, get the length of line dist.	
	double dist = distance(x, y);
	//Calculating angle D1 is trivial. Atan2 is a modified arctan() function that returns unambiguous results.	
	D1 = atan2(y, x);
	//D2 can be calculated using the law of cosines where a = dist, b = len1, and c = len2.	
	D2 = lawOfCosines(dist, ARM_LEN_1, ARM_LEN_2);
	//Then A1 is simply the sum of D1 and D2.	
	m_A1 = convert_deg(D1 + D2);
	//A2 can also be calculated with the law of cosine, but this time with a = len1, b = len2, and c = dist.	
	m_A2 = convert_deg(lawOfCosines(ARM_LEN_1, ARM_LEN_2, dist));
}

void RobotArm::ReachPosition(double x, double y, double z, double theta)
{
	m_x = x *-1; //revert x
	m_y = y;
	m_z = z;

	double t1,t2,t3;

	solve_angles(m_x,m_y);

	//calculate gripper angle
	m_A3 = (360-(m_A1+m_A2)) + theta;

	//calculate real position with offset
	t1 = m_A1 + ARM1_OFFSET;

	t2 = m_A2 - ARM2_OFFSET;

	t3 = m_A3 - ARM3_OFFSET;

	// send pos to AX12 servos
	servoax.attach(m_A1_id);
	servoax.moveSpeed((float)t1,50);

	servoax.attach(m_A2_id);
	servoax.moveSpeed((float)t2,50);

	servoax.attach(m_A3_id);
	servoax.moveSpeed((float)t3,50);

	//TODO : add pap Z axis

}

void RobotArm::set_x(double x)
{
	m_x = x;
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

double RobotArm::lawOfCosines(double a, double b, double c)
{
	return acos((a*a + b*b - c*c) / (2 * a * b));
}

double RobotArm::distance(double x, double y)
{
	return sqrt(x*x + y*y);
}

double RobotArm::convert_deg(double rad)
{
	return rad * 180 / M_PI;
}