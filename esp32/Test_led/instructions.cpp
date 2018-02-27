#include <Arduino.h>
#include "instructions.h"
#include "../common/tcptalks.h"
#include "../common/Pickle.h"

extern Effects Eff;

void SET_LOGO_ANIMATION(TCPTalks &inst, UnPickler& input, Pickler& output)
{
	long in = input.load<long>();

	Eff.select_logo_animation((int)in);

	output.dump<bool>(true);
}

void SET_BAR_ANIMATION(TCPTalks &inst, UnPickler& input, Pickler& output)
{
	long in = input.load<long>();

	Eff.select_bar_animation((int)in);

	output.dump<bool>(true);
}

void SET_ENGR_ANIMATION(TCPTalks &inst, UnPickler& input, Pickler& output)
{
	long in = input.load<long>();

	Eff.select_engr_animation((int)in);

	output.dump<bool>(true);
}