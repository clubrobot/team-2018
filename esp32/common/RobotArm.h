#include <Arduino.h>
#include <math.h>

#define ARM_LEN_1 15.0
#define ARM_LEN_2 15.0

class RobotArm
{
	public:

		RobotArm(double x, double y, double z, double theta);

		void solve_angles(double x, double y, double z, double *A1, double *A2, double *A3);

		void set_gripper_angle(double a);

		void close_gripper();

		void open_gripper();



		void set_x(double x);
		void set_y(double y);
		void set_z(double z);

		double get_A1();
		double get_A2();
		double get_A3();


	private :

		double lawOfCosines(double a, double b, double c);

		double distance(double x, double y);

		double convert_deg(double rad);

		double m_x = 0;
		double m_y = 0;
		double m_z = 0;

		double m_theta = 0;

		double m_D1 = 0;
		double m_D2 = 0;

		double m_A1 = 0;
		double m_A2 = 0;
		double m_A3 = 0;
};