#include <Arduino.h>
#include <math.h>

#define ARM_LEN_1 15.0
#define ARM_LEN_2 15.0

class IK
{
	public:

		IK();

		void solve_angles(double x, double y, double z, double *A1, double *A2, double *A3);

		void set_gripper_angle(double a);

		void close_gripper();

		void open_gripper();

		double convert_deg(double rad);

	private :

		double lawOfCosines(double a, double b, double c);

		double distance(double x, double y);
	
};