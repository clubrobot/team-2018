BOARD = esp32
CHIP = esp32

#Arduino file
SKETCH = Blink.ino

BOARD_UUID = esp32
COMMON = ../common
#Setup all libs used !
LIBS = $(ESP_LIBS)/EEPROM \
	   $(COMMON)/SerialTalks.cpp \
	   $(COMMON)/FastLED/FastLED.cpp \
	   $(COMMON)/FastLED/bitswap.cpp \
	   $(COMMON)/FastLED/colorpalettes.cpp \
	   $(COMMON)/FastLED/colorutils.cpp \
	   $(COMMON)/FastLED/hsv2rgb.cpp \
	   $(COMMON)/FastLED/lib8tion.cpp \
	   $(COMMON)/FastLED/noise.cpp \
	   $(COMMON)/FastLED/power_mgt.cpp \
	   $(COMMON)/FastLED/wiring.cpp \
	   $(COMMON)/DomotiquePannel.cpp \
	   $(COMMON)/PannelÈffects.cpp







CPPFLAGS = -fexceptions
# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk

