#include "DomotiquePannel.h"


DomotiquePannel::DomotiquePannel()
{
	/* Led matrix initialisation */
	LEDS.addLeds<CHIPSET, ENGR_PIN, COLOR_ORDER>(leds_engr,NUM_LEDS_ENGR);

  	LEDS.addLeds<CHIPSET, LOGO_PIN, COLOR_ORDER>(leds_logo,NUM_LEDS_LOGO);

  	LEDS.addLeds<CHIPSET, BAR_PIN, COLOR_ORDER>(leds_bar,NUM_LEDS_BAR);

  	LEDS.setBrightness(BRIGHTNESS);
}