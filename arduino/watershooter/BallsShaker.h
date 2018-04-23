#ifndef __BALLSHAKER_H__
#define __BALLSHAKER_H__

#include <Arduino.h>
#include <Servo.h>
#include "../common/SerialTalks.h"
#include "../common/PeriodicProcess.h"

#define SHAKER_HORIZONTAL_1 0
#define SHAKER_HORIZONTAL_2 135

#define SHAKER_VERTICAL_1 155
#define SHAKER_VERTICAL_2 60

#define FREQ_VERTICAL       4
#define FREQ_HORIZONTAL     3

class BallsShaker: public PeriodicProcess {

public:
	BallsShaker(): shaking(false){
        setTimestep(0.1);
    }

	void attachVertical(int PIN);
    void attachHorizontal(int PIN);
    void detach();
    void writeHorizontal(int angle);
    void writeVertical(int angle);
    int getVertical();
    int getHorizontal();

	void enableShaker();
	void disableShaker();
    void updateShaker();
    void shake();

private:
    Servo shakerVertical;
    Servo shakerHorizontal;
    bool count_clock_horizontal;
    bool count_clock_vertical;

protected:
    virtual void process(float timestep);
};

#endif // __BRUSHLESSMOTOR_H__
