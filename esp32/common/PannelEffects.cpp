#include "PannelEffects.h"

/* Constuctor */
PannelEffects::PannelEffects()
{
	/* Led matrix initialisation */
	  LEDS.addLeds<CHIPSET, ENGR_PIN, COLOR_ORDER>(leds_engr,NUM_LEDS_ENGR);

  	LEDS.addLeds<CHIPSET, LOGO_PIN, COLOR_ORDER>(leds_logo,NUM_LEDS_LOGO);

  	LEDS.addLeds<CHIPSET, BAR_PIN, COLOR_ORDER>(leds_bar,NUM_LEDS_BAR);

  	LEDS.setBrightness(BRIGHTNESS);
}


/* public methodes */







/* Private methods */

void PannelEffects::fire_effect(CRGB * led_matrix, const int size)
{
	// Array of temperature readings at each simulation cell
   byte heat[size];

  // Step 1.  Cool down every cell a little
    for( int i = 0; i < size; i++) 
    {
      heat[i] = qsub8( heat[i],  random8(0, ((COOLING * 10) / size) + 2));
    }
  
    // Step 2.  Heat from each cell drifts 'up' and diffuses a little
    for( int k= size - 1; k >= 2; k--) {
      heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2] ) / 3;
    }
    
    // Step 3.  Randomly ignite new 'sparks' of heat near the bottom
    if( random8() < SPARKING ) 
    {
      int y = random8(7);
      heat[y] = qadd8( heat[y], random8(160,255) );
    }

    // Step 4.  Map from heat cells to LED colors
    for( int j = 0; j < size; j++) 
    {
      CRGB color = HeatColor( heat[j]);
      int pixelnumber;
      if( gReverseDirection ) {
        pixelnumber = (size-1) - j;
      } else {
        pixelnumber = j;
      }
      led_matrix[pixelnumber] = color;
    }
    FastLED.show(); // display this frame
    FastLED.delay(1000 / FRAMES_PER_SECOND);
}

void PannelEffects::fadeall(CRGB *led_matrix, const int size)
{ 
	for(int i = 0; i < size; i++) 
	{ 
		led_matrix[i].nscale8(250); 
	}
}

void PannelEffects::cylon(CRGB * led_matrix, const int size)
{
	static uint8_t hue = 0;

  	// First slide the led in one direction
  	for(int i = 0; i < size; i++) 
  	{
    	// Set the i'th led to red 
    	led_matrix[i] = CHSV(hue++, 255, 255);
    	// Show the leds
    	FastLED.show(); 
    	// now that we've shown the leds, reset the i'th led to black
    	// leds[i] = CRGB::Black;
    	fadeall(led_matrix, size);
    	// Wait a little bit before we loop around and do it again
    	delay(10);
  	}

  	// Now go in the other direction.  
  	for(int i = (size)-1; i >= 0; i--) 
  	{
    	// Set the i'th led to red 
    	led_matrix[i] = CHSV(hue++, 255, 255);
    	// Show the leds
    	FastLED.show();
    	// now that we've shown the leds, reset the i'th led to black
    	// leds[i] = CRGB::Black;
    	fadeall(led_matrix, size);
    	// Wait a little bit before we loop around and do it again
    	delay(10);
  	}
}

/* MATRIX METHODS */

uint16_t PannelEffects::XY(uint8_t x, uint8_t y)
{
	uint16_t i;

	if( y & 0x01) 
	{
		// Odd rows run backwards
		uint8_t reverseX = (KMATRIXWIDTH - 1) - x;
		i = (y * KMATRIXWIDTH) + reverseX;
	} 
	else 
	{
		// Even rows run forwards
		i = (y * KMATRIXWIDTH) + x;
	}
		  
	return i;
}