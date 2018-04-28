#ifndef __ROBOTARM_H__
#define __ROBOTARM_H__

#include <Arduino.h>
#include <math.h>
#include <Servo.h>
#include "ShiftRegAX12.h" 
#include "SoftwareSerial.h"

#define ARM_LEN_1 15.0
#define ARM_LEN_2 15.0

#define ARM1_OFFSET 60
#define ARM2_OFFSET 30
#define ARM3_OFFSET 4

#define GRIPPER_OPEN 50
#define GRIPPER_CLOSE 110

#define AX1_MAX_ANGLE 250
#define AX1_MIN_ANGLE 70

#define AX2_MAX_ANGLE 0
#define AX2_MIN_ANGLE 300

class RobotArm
{
	public:

		RobotArm(double x, double y, double z, double theta, float speed);

		void attach(unsigned char A1_id, unsigned char A2_id, unsigned char A3_id, unsigned char servo);

		void begin();

		bool solve_angles(double x, double y);

		bool solve_coords(double *x, double*y, double *th);

		void ReachPosition(double x, double y, double z, double theta);

		void set_gripper_angle(double a);

		void close_gripper();

		void open_gripper();

		void set_angles(float A1, float A2, float A3);

		void set_x(double x);
		void set_y(double y);
		void set_z(double z);
		void set_theta(double theta);

		void set_speed(float speed);

		double get_A1theo();
		double get_A2theo();
		double get_A3theo();

		double get_A1();
		double get_A2();
		double get_A3();


	protected :

		bool lawOfCosines(double a, double b, double c, double *A);

		double distance(double x, double y);

		double convert_deg(double rad);

		float m_speed;

		double m_x;
		double m_y;
		double m_z;

		double m_x_max;
		double m_y_max;
		double m_z_max;


		double m_theta;
		double m_theta_max;

		double m_D1;
		double m_D2;

		double m_A1;
		double m_A2;
		double m_A3;

		unsigned char m_A1_id;
		unsigned char m_A2_id;
		unsigned char m_A3_id;

		Servo m_gripper;;
};
#endif