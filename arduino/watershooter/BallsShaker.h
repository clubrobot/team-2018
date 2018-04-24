#ifndef __BALLSHAKER_H__
#define __BALLSHAKER_H__

#include <Arduino.h>
#include <Servo.h>
#include "../common/SerialTalks.h"
#include "../common/PeriodicProcess.h"

#define SHAKER_HORIZONTAL_1 3
#define SHAKER_HORIZONTAL_2 142
#define SHAKER_VERTICAL_1 160
#define SHAKER_VERTICAL_2 70

#define PER_VERTICAL       (int)(82)
#define PER_HORIZONTAL     (int)(64)
#define PER_EQUAL          (int)(100)

class BallsShaker: public PeriodicProcess {
    int EQUAL_FREQ = 0;
    int DIFF_FREQ = 1;
public:
	BallsShaker(){
        count_clock_horizontal = 0;
        count_clock_vertical = 0;
        mode = 0;
        setTimestep(0.015);
    }

	void attachVertical(int PIN);
    void attachHorizontal(int PIN);
    void detach();
    void writeHorizontal(int angle);
    void writeVertical(int angle);
    int getVertical();
    int getHorizontal();

	void enableShakerEqualFreq();
	void enableShakerDiffFreq();
	void disableShaker();
    void updateShaker();
    void shake();

private:
    Servo shakerVertical;
    Servo shakerHorizontal;
    int count_clock_horizontal;
    int count_clock_vertical;
    int mode;

protected:
    virtual void process(float timestep);
};

#endif // __BRUSHLESSMOTOR_H__
