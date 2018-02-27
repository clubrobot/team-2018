#ifndef __INSTRUCTIONS_H__
#define __INSTRUCTIONS_H__

#include <Arduino.h>
#include "../common/Effects.h"
#include "../common/tcptalks.h"

void SET_LOGO_ANIMATION(TCPTalks &inst, UnPickler& input, Pickler& output);

void SET_BAR_ANIMATION(TCPTalks &inst, UnPickler& input, Pickler& output);

void SET_ENGR_ANIMATION(TCPTalks &inst, UnPickler& input, Pickler& output);

#endif //__INSTRUCTIONS_H__