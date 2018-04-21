#include "RobotArm.h"


RobotArm::RobotArm(double x, double y, double z, double theta)
{
	m_x = x;
	m_y = y;
	m_z = z;
	m_theta = theta;

	//set start position
	ReachPosition(m_x, m_y, m_z, m_theta);
}

void IK::solve_angles(double x, double y, double z)
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

	m_A3 = z;
}

void IK::ReachPosition(double x, double y, double z, double theta)
{
	solve_angles(x,y,z);

	//AX12 1 = get_A1();
	//AX12 2 = get_A2();
	//pap    =  get_A3()
	//AX12 grip = theta;
}

void IK::set_x(double x)
{
	m_x = x;
	solve_angles(m_x, m_y, m_z);
	//AX12  
}

void IK::set_y(double y)
{
	m_y = y;
	solve_angles(m_x, m_y, m_z);
	//AX12  
}

void IK::set_z(double z)
{
	m_z = z;	
	solve_angles(m_x, m_y, m_z);
	//AX12  
}

double get_A1()
{
	return m_A1;
}

double get_A2()
{
	return m_A2;
}

double get_A3()
{
	return m_A3;
}

double IK::lawOfCosines(double a, double b, double c)
{
	return acos((a*a + b*b - c*c) / (2 * a * b));
}

double IK::distance(double x, double y)
{
	return sqrt(x*x + y*y);
}

double IK::convert_deg(double rad)
{
	return rad * 180 / M_PI;
}