#ifndef CONFIGURATION_H
#define CONFIGURATION_H

#define CURRENT_BEACON_NUMBER 0 // Numéro courant de la balise à uploader. compris entre 0 et MAX_ANCHORS

#define MAX_ANCHORS 4   // nombre maximum de balises fixes

const byte ANCHOR_SHORT_ADDRESS[MAX_ANCHORS] = {35, 36, 37, 38};
const uint16_t ANTENNA_DELAY[MAX_ANCHORS] = {16530, 16530, 16530, 16530};

#endif