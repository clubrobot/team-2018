#ifndef __INSTRUCTIONS_H__
#define __INSTRUCTIONS_H__

#include "../common/tcptalks.h"
#include "../common/Pickle.h"


#define SET_BAR_OPCODE	 0X11
#define GET_BAR_OPCODE	 0X12

#define SET_LOGO_OPCODE	 0X13
#define GET_LOGO_OPCODE  0X14

#define SET_ENGR_OPCODE	 0X15
#define GET_ENGR_OPCODE	 0X16


void SET_BAR(TCPTalks &inst, UnPickler& input, Pickler& output);

void GET_BAR(TCPTalks &inst, UnPickler& input, Pickler& output);

void SET_LOGO(TCPTalks &inst, UnPickler& input, Pickler& output);

void GET_LOGO(TCPTalks &inst, UnPickler& input, Pickler& output);

void SET_ENGR(TCPTalks &inst, UnPickler& input, Pickler& output);

void GET_ENGR(TCPTalks &inst, UnPickler& input, Pickler& output);

#endif //__INSTRUCTIONS_H__

