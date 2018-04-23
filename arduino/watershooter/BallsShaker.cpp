#include "BallsShaker.h"


void BallsShaker::attachVertical(int pin)
{
    shakerVertical.attach(pin);
}

void BallsShaker::attachHorizontal(int pin)
{
    shakerHorizontal.attach(pin);
}

void BallsShaker::detach()
{
    shakerVertical.detach();
    shakerHorizontal.detach();
}

void BallsShaker::writeHorizontal(int angle)
{
    shakerHorizontal.write(angle);
}

void BallsShaker::writeVertical(int angle)
{
    shakerVertical.write(angle);
}

int BallsShaker::getVertical()
{
    return shakerVertical.read();
}

int BallsShaker::getHorizontal()
{
    return shakerHorizontal.read();
}

void BallsShaker::shake()
{
    if(count_clock_horizontal == FREQ_HORIZONTAL/2){
        shakerHorizontal.write(SHAKER_HORIZONTAL_1);
    }
    
    if(count_clock_horizontal == FREQ_HORIZONTAL){
        shakerHorizontal.write(SHAKER_HORIZONTAL_2);
        count_clock_horizontal = 0;
    }

    if(count_clock_vertical == FREQ_VERTICAL/2)
    {
        shakerVertical.write(SHAKER_VERTICAL_1);
    }
    if(count_clock_vertical == FREQ_VERTICAL){
        shakerVertical.write(SHAKER_VERTICAL_2);
        count_clock_vertical = 0;
    }
    count_clock_horizontal++;
    count_clock_vertical++;
}

void BallsShaker::enableShaker(){
    enable();
}

void BallsShaker::disableShaker(){
    this->writeHorizontal(SHAKER_HORIZONTAL_1);
    this->writeVertical(SHAKER_VERTICAL_1);
    disable();
}

void BallsShaker::updateShaker(){
	PeriodicProcess::update();
}

void BallsShaker::process(float timestep){
    this->shake();
}
