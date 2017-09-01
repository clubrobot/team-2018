############
SerialTalks
############

La librairie SerialTalks assure la comunication entre une ordinateur et un arduino.
On trouve dans cette librairie deux versions asymétriques pour chaque terminal.

*************
Préambule
*************

Cette librairie de communication se base sur des requettes et des retours. Chaque packet a une forme standardisé.

.. image:: tab_serialtalks.png

1. **Master Code**:
    Le Master code permet de faire la difference entre un packet esclave et maitre. Un packet maitre correspond a une demande alors que le packet esclave est un retour suite a une demande.
    Il vaut soit ``b'R'`` (maitre)  soit ``b'A'`` (esclave).
2. **Size number**:
    Le Size number correspond à la taille du message en nombre d'octets sans compter le premier octet dédié au master code. Remarque un message sous SerialTalks ne peux exeder 255 octets.
3. **OP Code**
    L'Op code est très important puisqu'il permet d'explicité la requette. On associe au préalable pour chaque requette de l'arduino un OP code. Une fois qu'il resoit un Op code et ces arguments, il execute la requtte paramétrée. Attention l'OP Code n'est pas présent dans les packets de retour.
4. **RET Code**
    Le RET code est utile pour les retours d'instructions. En effet si l'arduino a besoin de renvoyé des informations au programme python. il va utilisé ce code dans le packet retour pour permettre au programme python de bien associé avec quel requette ces informations sont reliés.
5. **args et kwargs**:
    Une requette peux avoir une infinité d'arguments suplémentaire du moment que la taille du packet est règlementaire. Il faut savoir que l'arduino tout comme les methodes en python ne peuvent pas d'eux même reconnaitrent la nature des arguments et leurs nombres. Ces information devront être renseigné au préalable.

Les requettes sont toujours à l'initiative de la parti python. L'arduino ne peux pas déclanché la moindre méthode python contrairement au code python.
Quand une requettes depuis l'ordinateur est envoyé à l'arduino, il y a deux cas de figure : 

 * Si notre requette ne require aucun retour, dans ce cas le packet va déclanché une fonction dans l'arduino.
 * Si notre requette require un retour, l'arduino après avoir executé la fonction associé à l'OP code reçu va renvoyé ça réponse grâce au code esclave et le retcode qui a été envoyé dans le packet recu.



**************
Python Object
**************

Cette parti correspond à la bibliothéque python destiné à la raspberry ou à l'ordinateur.

Préambule
-------------------------

Pour ouvrir les comunications avec un arduino, il faut creer un object SerialTalks et lancé la connexion avec les méthodes disponibles de celle-ci.


API
--------------------------


.. class:: SerialTalks

    .. method:: __init__(port)

        :param port:
            Adresse de l'arduino a connecter, le format de l'adresse dépend de l'OS utilisé.
            Sous Windows elle sera de la forme : ``COM3`` , Alors que sous Linux on aurra une adresse de la forme : ``/dev/ttyUSB0`` ou ``/dev/arduino/WheeledBase``

    .. method:: connect(timeout=5)

        Cette methode permet de connecter l'arduino avec l'ordinateur, si cette méthode s'execute sans erreur, il est ensuite possible d'envoyer des instructions

        :param int timeout:

            Choisi un timeout pour la connexion entre l'ordinateur et l'arduino (en seconde)

        :exception ConnectionFailedError:

             Dans le cas ou l'arduino n'est pas trouvé ou ne peux pas être configuré.

        :exception AlreadyConnectedError:

            Dans le cas ou l'arduino est déjà connecté.

    .. method:: disconnect()

        Permet de déconnecter l'arduino.

    .. method:: send(opcode, *args)

        Permet l'execution d'une requette sans retour d'information de la part de l'arduino, exemple définir une nouvelle position.

        :param hexa opcode: Code correspondant à la requette demandé. Généralement utilisé sous forme de nombre en hexadécimal ; example : ``0xF4``

        :param bytes args: Arguments à ajouter en fonction de la requette executé, toujours sous la forme de bytes. Pour la conversion utilisé SerialUtils.

        :return: Code d'indentification pour le retour des informations (retcode). Nombre entier généré aléatoirement entre 0 et 4294967295.

    .. method:: get_queue(retcode)

        :param int retcode: Code d'indentification donné lors de l'envoie de la requette pour avoir le retour de l'arduino a propos de cette meme requette.

        :return: Renvoie l'object |queue|_ relié avec le retcode.


    .. method:: delete_queue(retcode)

        Permet la suppression d'une |queue|_

        :param int retcode: Code d'indentification de la |queue|_ à supprimer.

    .. method:: reset_queues()

        Permet la suppression de toutes les |queue|_ .



    .. method:: poll(retcode, timeout=0)

        Methode pour récuper un message en attente dans une queue.

        :param int retcode: Code d'indentification de la queue à utiliser.

        :param int timeout: Timeout pour la reception du message.

        :return: Message en bytes.



    .. method:: flush( retcode)

        Méthode pour vider une queue

        :param int retcode: Code d'indentification de la queue à utiliser.

    .. method:: execute( opcode, *args, timeout=5)

        Methode pour executé une requette avec un retour. 

        :param int opcode: Code d'indentification de la requette à effectuer
        :param bytes args: Argument à transmettre à l'arduino, attention les convertir en bytes avant
        :param int  timeout: Timeout de la reception (en seconde).
        :return: Arguments recu de l'arduino sous l'object Deserialser voir 

    .. method:: getuuid(timeout=5)

        Methode pour demandé à l'arduin son indentification

        :param int timeout: Timeout de la reception (en seconde) de l'indentification.
        :return: L'indentification de l'arduino


    .. method:: setuuid( uuid)

        Methode pour définir un nouvelle indentification pour l'arduino

        :param uuid: Nouvelle indentification pour l'arduino


    .. method:: getlog( retcode, timeout=0)

    .. method:: getout(timeout=0)

    .. method:: geterr(timeout=0):


    .. warning:: Les methodes suivantes sont réservé à une utilisation interne

    .. method:: process(message)

        Methode qui permet de placer un message sous forme de bytes provenant de l'arduino dans une Queue grâce au retcode dans le message

        :param bytes message: Message a traité

    .. method:: rawsend()






Utilisation
--------------------------

ils exisitent deux possibilité pour utilisé cette librairie. Utiliser directement l'object seriatalks, ce qui peux être vite fastidieux pour réaliser des actions autre que la manipulation d'UUID. L'autre option est de creer une classe qui dérive de SerialTalks qui va permettre une utilisation de l'arduino très haut niveau.

Pour utilisé directement il faut d'abord importer la librairie :

.. code::

    from serialTalks import *

.. warning::

    Pour pouvoir faire l'importation depuis n'importe quel endroit utilisé le code suivant : 

.. code::

    import os, sys, glob
    home = os.path.expanduser("~")
    for directory in glob.iglob(os.path.join(home, '**/team-2018/raspberrypi'), recursive=True):
    	sys.path.append(directory)


Il suffit ensuite de creer l'objet de le connecter comme ceci : 

.. code::
    
    arduino = SerialTalks('ardresse')
    arduino.connect()

La création d'object est un peu plus compliqué. Pour commencé il faut faire hérité notre nouvelle object de SerialTalks comme ceci:

.. code::

    from serialtalks import *

    class Arduino(SerialTalks): 
        def __init__(self,adresse,..........):
            SerialTalks.__init__(self,adresse)
            .
            .

.. note:: Il est possible de ne pas écrire l'init si votre nouvelle object n'a pas besoin de variable pour son initialisation

Ensuite il faut ajouter à cette object des méthodes qui correspondrons à des OP code. 
Voici un exemple simple d'envoie d'une variable float à l'arduino.

.. code::

    def ordre(self, variable):

        self.send(OPCODE,FLOAT(variable))

On peut voir dans cette méthode l'utilisation de l'object FLOAT, cette object venu tous droit de la librairie permet la conversion en bytes. Les objects de conversions sont expliquer dans le chapitre SerialUtils.

Pour indiquer l'Op code, il est vivement conseillé d'utilisé des constantes à definir en haut de votre fichier python de préférence en hexadécimal. Comme dans l'exemple ci contre.

.. code:: 

    OPCODE = 0xF4

.. warning:: Les opcodes suivants sont réservé par la lib et ne doivent pas être utilisé par vos objects : ``0x00`` , ``0x01`` , ``0x02``

**************
Arduino Object
**************


``<cpr/SerialTalks.h>``

.. class:: serialTalks

    .. method:: void rawsend()
    
        :param ef: 
            test







.. |queue| replace:: Queue
.. _queue: https://docs.python.org/3.6/library/queue.html