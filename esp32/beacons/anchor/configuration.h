#ifndef CONFIGURATION_H
#define CONFIGURATION_H

#define CURRENT_BEACON_NUMBER 0 // Numéro courant de la balise à uploader. compris entre 0 et MAX_ANCHORS

#define MAX_ANCHORS 4   // nombre maximum de balises fixes

const byte ANCHOR_SHORT_ADDRESS[MAX_ANCHORS] = {35, 36, 37, 38};
const uint16_t ANTENNA_DELAY[MAX_ANCHORS] = {16530, 16530, 16530, 16530};



/**
 * EEPROM addresses
 */

#define EEPROM_BASE_ADDRESS 49

#define EEPROM_NUM_ANCHOR       EEPROM_BASE_ADDRESS         // 1 octet
#define EEPROM_ANTENNA_DELAY    (EEPROM_NUM_ANCHOR+1)       // 2 octets
//#define EEPROM_SHORT_ADDRESS    (EEPROM_ANTENNA_DELAY+2)    // 1 octet
//#define EEPROM_LONG_ADDRESS     (EEPROM_SHORT_ADDRESS+1)    // 16 octets


#endif