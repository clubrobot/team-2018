#include "DomotiquePannel.h"

/* Constuctor */
DomotiquePannel::DomotiquePannel()
{
	/* Led matrix initialisation */
	LEDS.addLeds<CHIPSET, ENGR_PIN, COLOR_ORDER>(leds_engr,NUM_LEDS_ENGR);

  	LEDS.addLeds<CHIPSET, LOGO_PIN, COLOR_ORDER>(leds_logo,NUM_LEDS_LOGO);

  	LEDS.addLeds<CHIPSET, BAR_PIN, COLOR_ORDER>(leds_bar,NUM_LEDS_BAR);

  	LEDS.setBrightness(BRIGHTNESS);
}


/* public methodes */







/* Private methods */

void DomotiquePannel::fire_effect(CRGB * led_matrix, const int size)
{
	// Array of temperature readings at each simulation cell
   byte heat[size];

  // Step 1.  Cool down every cell a little
    for( int i = 0; i < size; i++) {
      heat[i] = qsub8( heat[i],  random8(0, ((COOLING * 10) / size) + 2));
    }
  
    // Step 2.  Heat from each cell drifts 'up' and diffuses a little
    for( int k= size - 1; k >= 2; k--) {
      heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2] ) / 3;
    }
    
    // Step 3.  Randomly ignite new 'sparks' of heat near the bottom
    if( random8() < SPARKING ) {
      int y = random8(7);
      heat[y] = qadd8( heat[y], random8(160,255) );
    }

    // Step 4.  Map from heat cells to LED colors
    for( int j = 0; j < size; j++) {
      CRGB color = HeatColor( heat[j]);
      int pixelnumber;
      if( gReverseDirection ) {
        pixelnumber = (size-1) - j;
      } else {
        pixelnumber = j;
      }
      led_matrix[pixelnumber] = color;
    }
}

void DomotiquePannel::fadeall(CRGB *led_matrix, const int size)
{ 
	for(int i = 0; i < size; i++) 
	{ 
		led_matrix[i].nscale8(250); 
	}
}