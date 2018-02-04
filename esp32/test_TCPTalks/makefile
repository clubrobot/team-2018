BOARD = esp32
CHIP = esp32

#Arduino file
SKETCH = main.ino

BOARD_UUID = esp32
COMMON = ../common
#Setup all libs used !
LIBS = $(ESP_LIBS)/EEPROM \
	   $(COMMON)/SerialTalks.cpp \
	   $(COMMON)/tcptalks.cpp \
	   $(COMMON)/WiFi/src/WiFi.cpp \
	   $(COMMON)/WiFi/src/ETH.cpp \
	   $(COMMON)/WiFi/src/WiFiAP.cpp \
	   $(COMMON)/WiFi/src/WiFiClient.cpp \
	   $(COMMON)/WiFi/src/WiFiGeneric.cpp \
	   $(COMMON)/WiFi/src/WiFiMulti.cpp \
	   $(COMMON)/WiFi/src/WiFiSTA.cpp \
	   $(COMMON)/WiFi/src/WiFiScan.cpp \
	   $(COMMON)/WiFi/src/WiFiServer.cpp \
	   $(COMMON)/WiFi/src/WiFiUdp.cpp \
	   $(COMMON)/Pickle.cpp 

CPPFLAGS = -fexceptions
# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk

