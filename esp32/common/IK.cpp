#include "IK.h"

IK::IK()
{
	
}

void IK::solve_angles(double x, double y, double z, double *A1, double *A2, double *A3)
{
	double D1,D2;
	//First, get the length of line dist.	
	double dist = distance(x, y);
	//Calculating angle D1 is trivial. Atan2 is a modified arctan() function that returns unambiguous results.	
	D1 = atan2(y, x);
	//D2 can be calculated using the law of cosines where a = dist, b = len1, and c = len2.	
	D2 = lawOfCosines(dist, ARM_LEN_1, ARM_LEN_2);
	//Then A1 is simply the sum of D1 and D2.	
	*A1 = D1 + D2;
	//A2 can also be calculated with the law of cosine, but this time with a = len1, b = len2, and c = dist.	
	*A2 = lawOfCosines(ARM_LEN_1, ARM_LEN_2, dist);

	*A3 = z;
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