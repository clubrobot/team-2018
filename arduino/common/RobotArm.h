#include <Arduino.h>
#include <math.h>

#define ARM_LEN_1 15.0
#define ARM_LEN_2 15.0

#define ARM1_OFFSET 60
#define ARM2_OFFSET 30
#define ARM3_OFFSET 30

class RobotArm
{
	public:

		RobotArm(double x, double y, double z, double theta);

		void attach(int A1_id, int A2_id, int A3_id);

		void begin();

		void solve_angles(double x, double y);

		void ReachPosition(double x, double y, double z, double theta);

		void set_gripper_angle(double a);

		void close_gripper();

		void open_gripper();



		void set_x(double x);
		void set_y(double y);
		void set_z(double z);

		double get_A1theo();
		double get_A2theo();
		double get_A3theo();

		double get_A1();
		double get_A2();
		double get_A3();


	private :

		double lawOfCosines(double a, double b, double c);

		double distance(double x, double y);

		double convert_deg(double rad);

		double m_x;
		double m_y;
		double m_z;

		double m_theta;

		double m_D1;
		double m_D2;

		double m_A1;
		double m_A2;
		double m_A3;

		int m_A1_id;
		int m_A2_id;
		int m_A3_id;
};