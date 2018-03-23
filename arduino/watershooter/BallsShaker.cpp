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
    if(shaking){
        shakerVertical.write(SHAKER_VERTICAL_1);
        shakerHorizontal.write(SHAKER_HORIZONTAL_1);
    } else {
        shakerVertical.write(SHAKER_VERTICAL_2);
        shakerHorizontal.write(SHAKER_HORIZONTAL_2);
    }
    shaking = !shaking;
}

void BallsShaker::enableShaker(){
    enable();
}

void BallsShaker::disableShaker(){
    disable();
}

void BallsShaker::updateShaker(){
	PeriodicProcess::update();
}

void BallsShaker::process(float timestep){
    this->shake();
}
