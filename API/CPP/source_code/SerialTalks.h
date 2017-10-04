#ifndef __SERIALTALKS_H__
#define __SERIALTALKS_H__

#include <Arduino.h>
#include "serialutils.h"

#ifndef SERIALTALKS_BAUDRATE
#define SERIALTALKS_BAUDRATE 115200  /*!< Bauderate utiliser */
#endif

#ifndef SERIALTALKS_INPUT_BUFFER_SIZE
#define SERIALTALKS_INPUT_BUFFER_SIZE 64
#endif

#ifndef SERIALTALKS_OUTPUT_BUFFER_SIZE
#define SERIALTALKS_OUTPUT_BUFFER_SIZE 64
#endif

#ifndef SERIALTALKS_UUID_ADDRESS
#define SERIALTALKS_UUID_ADDRESS 0x0000000000
#endif

#ifndef SERIALTALKS_UUID_LENGTH
#define SERIALTALKS_UUID_LENGTH	32
#endif

#ifndef SERIALTALKS_MAX_OPCODE
#define SERIALTALKS_MAX_OPCODE 0x10
#endif

#define SERIALTALKS_MASTER_BYTE 'R'
#define SERIALTALKS_SLAVE_BYTE  'A'

#define SERIALTALKS_DEFAULT_UUID_LENGTH 9

#define SERIALTALKS_PING_OPCODE    0x0
#define SERIALTALKS_GETUUID_OPCODE 0x1
#define SERIALTALKS_SETUUID_OPCODE 0x2
#define SERIALTALKS_STDOUT_RETCODE 0xFFFFFFFF
#define SERIALTALKS_STDERR_RETCODE 0xFFFFFFFE









/** class SerialTalks
 *  \brief Object de communication serial avec un ordinateur.
 *
 *  est un outil permettant à l'arduino de pouvoir répondre aux requettes recu depuis le serial.
 *  Il utilise donc le port serial (usb) pour envoyer ou recevoir des données avec l'ordinateur ou la raspberry
 *  La classe est capable de lancer des methodes sur demande de l'ordinateur ou de la raspberry.
 */
class SerialTalks
{
public: 

	/** class ostream
	 * \brief Stream virtuel pour les erreurs et autre.
	 *
	 *	est un outils pour permettre de mieux transmettre les erreurs rencontrées et les STD::OUT
	 *
	 *
	*/
	class ostream : public Print
	{
	public:

		//! Ecrit sur le serial l'octet indiqué.
		/*!
			\param c octet à passer dans le serial.
			\return Nombre d'octet transmit.
		*/


		virtual size_t write(uint8_t c);

		//! Ecrit sur le serial le buffer indiqué (liste d'octets).
		/*!
			\param buffer à passer.
			\param size (taille) du buffer.
			\return Nombre d'octet transmit.
		*/

		virtual size_t write(const uint8_t *buffer, size_t size);

		//! Surcharge de l'opérateur '<<'.
		//! Cette méthode permet de passer plus facilement les objets dans le serial avec conversion en octets automatique.
		/*!
			\param object à passer dans le serial.

		*/

		template<typename T> ostream& operator<<(const T& object)
		{
			print(object);
			return *this;
		}

	protected:

		//! Initialise le ostream. C'est à dire expliciter le pointeur du SerialTalks et le retcode à associer.
		/*!
			\param parent SerialTalks à associer.
			\param retcode Code d'identification à utiliser pour l'utilisation du serial.

		*/

		void begin(SerialTalks& parent, long retcode);

		SerialTalks* m_parent; /*!< SerialTalks parent  */
		long         m_retcode; /*!< RetCode à associer au flux virtuel */

		friend class SerialTalks;
	};


	/*! \var typedef *Instruction
	 * \brief Instruction est un pointeur de fonction dont la signature doit être de la forme : (SerialTalks& inst, Deserializer& input, Serializer& output).
	 *
	 */

	typedef void (*Instruction)(SerialTalks& inst, Deserializer& input, Serializer& output);


	//! Initialise le SerialTalks avec un Stream d'<arduino.h>.
	/*!
		\param stream Flux à associer pour la communication de SerialTalks.
	*/

	void begin(Stream& stream);


	//! Associe une Instruction à un OPCODE.
	/*!
		\param opcode Code à associer à la fonction.
		\param instruction Fonction à répertorier dans SerialTalks.
	*/

	void bind(byte opcode, Instruction instruction);

	//! Lance la fonction à partir des octets reçus. La méthode lit l'OPCode et transmet à la bonne fonction l'objet Deserializer avec le reste les octets reçu non traités et un Serialiser pour la réponse à transmettre. 
	/*!
		\param inputBuffer Liste des octets reçus pour cette requête.
		\return Vrai si la fonction à renvoyé des informations.
	*/

	bool execinstruction(byte* inputBuffer);

	//! Lit les octets reçus et les traites quand ils forment une requête complête.
	/*!
		\return Vrai si une requête à renvoyé une information.
	*/

	bool execute();

	//! Indique si le stream de SerialTalks est bien connecté.
	/*!
		\return Vrai si le stream est connecté.
	*/


	bool isConnected() const {return m_connected;}

	//! Méthode bloquante jusqu'a la connexion du Stream ou jusqu'au timeout.
	/*!
		\param timeout Timeout pour la méthode 
		\return Vrai si le Stream est connecté.
	*/



	bool waitUntilConnected(float timeout = -1);

	//! Ecrit sur le pointeur l'UUID enregistré dans l'EEPROM de l'Arduino.
	/*!
		\param uuid Pointeur à utiliser.
		\return Vrai si il existe bien un UUID.
	*/


	bool getUUID(char* uuid);

	//! Enregistre l'UUID dans l'EEPROM de l'Arduino.
	/*!
		\param uuid Pointeur de l'UUID à enregistrer.
	*/


	void setUUID(const char* uuid);

	//! Génère un UUID
	/*!
		\param uuid Pointeur pour renvoyer l'UUID.
		\param length Longueur en octet de l'UUID à générer.
	*/


	static void generateRandomUUID(char* uuid, int length);

	// Public attributes (yes we dare!)

	ostream     out; /*!< Flux virtuel pour les STD:OUT.  */
	ostream     err;/*!< Flux virtuel pour les STD:ERR ou erreur.  */

protected: // Protected methods

	int sendback(long retcode, const byte* buffer, int size);

	// Attributes

	Stream*     m_stream; /*!< Stream de communication utilisé par SerialTalks.*/
	bool		m_connected;/*!< Représente l'état de connection.*/

	Instruction	m_instructions[SERIALTALKS_MAX_OPCODE];/*!< Listes des instructions enregistrées avec un OPCode associé.*/

	byte        m_inputBuffer [SERIALTALKS_INPUT_BUFFER_SIZE];/*!< Buffer d'entrée d'informations.*/
	byte        m_outputBuffer[SERIALTALKS_OUTPUT_BUFFER_SIZE];/*!< Buffer de sortie d'informations.  */


	/// Différents états de réception.
	enum 
	{
		SERIALTALKS_WAITING_STATE, ///<En attente de l'arrivé d'un octet.
		SERIALTALKS_INSTRUCTION_STARTING_STATE, ///< En attente du prochain octet de la requête correspondant à la taille de celle-ci.
		SERIALTALKS_INSTRUCTION_RECEIVING_STATE, ///< Réception des derniers octet de la requête.
	}           m_state;/// Différents états de réception.
	
	byte        m_bytesNumber; /*!< Variable pour la réception de données qui correspond à la longueur de la requête en bytes (valeur donnée dans le deuxième byte d'une requête).*/
	byte        m_bytesCounter;/*!< Variable d'incrementation pour la réception de données.*/
	long        m_lastTime;/*!< Timeout pour la réception d'octets d'une même requête.*/

private:

	//! Méthode pour la requête de ping.
	static void PING   (SerialTalks& talks, Deserializer& input, Serializer& output);

	//! Méthode pour la requête d'UUID.
	static void GETUUID(SerialTalks& talks, Deserializer& input, Serializer& output);
	//! Méthode pour la requête de changement d'UUID.
	static void SETUUID(SerialTalks& talks, Deserializer& input, Serializer& output);
};

extern SerialTalks talks;

#endif // __SERIALTALKS_H__
