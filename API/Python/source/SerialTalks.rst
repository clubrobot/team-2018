############
SerialTalks
############

La librairie SerialTalks assure la communication entre ordinateur et arduino.
On trouve dans cette librairie deux versions differentes pour chaque terminal.

*************
Préambule
*************

Cette librairie de communication se base sur des requêtes et des retours. Chaque packet à une forme standardisé.
.. image:: tab_serialtalks.png

1. **Master Code**:
    Le Master code permet de faire la différence entre un packet esclave et maître. Un packet maître corresponds à une demande alors que le packet esclave est une réponse suite à une demande.    Le Master code permet de faire la difference entre un packet esclave et maitre. Un packet maitre correspond a une demande alors que le packet esclave est un retour suite a une demande.
    Il vaut soit ``b'R'`` (maitre)  soit ``b'A'`` (esclave).
2. **Size number**:
    Le Size number correspond à la taille du message en nombre d'octets sans compter le premier octet dédié au master code. Remarque un message sous SerialTalks ne peux exercer plus de 255 octets.
3. **OP Code**
    L'OP code est très important puisqu'il permet d'expliciter la requête. On associe au préalable pour chaque fonction de l’Arduino un OP code. Une fois qu'il reçoit un OP code et ces arguments, il exécute la fonction paramétrée. Attention l'OP Code n'est pas présent dans les packets de retour.
4. **RET Code**
    C'est un code unique identifiant la requête. Il est utile pour les réponses d'instructions. En effet si l'arduino a besoin de renvoyer des informations au programme python. il va utiliser ce code dans le packet retour pour permettre au programme python de bien associer avec quel requête ces informations sont reliés.
5. **args et kwargs**:
    Une requête peux avoir une infinité d'arguments supplémentaire du moment que la taille du packet est réglementaire. Il faut savoir que l'arduino tout comme les méthodes en python ne peuvent pas d'eux même reconnaître la nature des arguments et leurs nombres. Ces information devront être renseignées au préalable.


Les requêtes sont toujours à l'initiative de la partie python. L’Arduino ne peut pas déclencher la moindre fonction python contrairement à son homologue.
Quand une requête depuis l'ordinateur est envoyée à l’Arduino, il y a deux cas de figure : 

 * Si notre requête ne requiert aucun retour, dans ce cas le packet va déclencher une fonction dans l’Arduino.
 * Si notre requête requiert un retour l’Arduino, après avoir exécuté la fonction associée à l'OP code reçu va renvoyer sa réponse grâce au code esclave et le Retcode qui a été envoyé dans le packet reçu.




Introduction
-------------------------

Cette partie correspond à la bibliothèque Python destinée à la Raspberry ou à l'ordinateur.

Pour ouvrir les communications avec un Arduino, il faut créer un objet SerialTalks et lancer la connexion avec la méthode de connexion.
Une fois les étapes préliminaires exécutées, il est possible de lancer n’importe quelle requête.    

***********
API
***********


.. class:: SerialTalks

    .. method:: __init__(port)

        :param port:
            Adresse de l'Arduino à connecter, le format de l'adresse dépend de l'OS utilisé.
            Sous Windows elle sera de la forme : ``COM3`` . Alors que sous Linux on aura une adresse de la forme : ``/dev/ttyUSB0`` ou ``/dev/arduino/WheeledBase``

    .. method:: connect(timeout=5)

        Connecte l'Arduino avec l'ordinateur, si cette méthode s’exécute sans erreur, il est ensuite possible d'envoyer des instructions.

        :param int timeout:

            Choisi un timeout pour la connexion entre l'ordinateur et l'arduino (en seconde)

        :exception ConnectionFailedError:

             Dans le cas où l'Arduino n'est pas trouvée ou ne peut pas être configuré.

        :exception AlreadyConnectedError:

            Dans le cas où l'Arduino est déjà connecté.

    .. method:: disconnect()

        Déconnecte l'Arduino.

    .. method:: send(opcode, *args)

        Envoi une requête sans retour d'information de la part de l'Arduino, exemple définir une nouvelle position.

        :param hexa opcode: Code correspondant à la requête demandée. Généralement utilisé sous forme de nombre hexadécimal. Exemple : ``0xF4``

        :param bytes args: Arguments à ajouter en fonction de la requête executée, toujours sous la forme de bytes. Pour la conversion utiliser SerialUtils.

        :return: Code d'identification pour le retour d'informations (retcode). Nombre entier généré aléatoirement entre 0 et 4294967295.

    .. method:: get_queue(retcode)

        :param int retcode: Code d'identification donné lors de l'envoi de la requête. Cela permet de pouvoir retrouver le retour de l'Arduino à propos de cette requête.

        :return: Renvoie l'objet |queue|_ relié avec le retcode.


    .. method:: delete_queue(retcode)

        Supprime une |queue|_ .

        :param int retcode: Code d'indentification de la |queue|_ à supprimer.

    .. method:: reset_queues()

       Supprime toutes les |queue|_ .



    .. method:: poll(retcode, timeout=0)

        Récupère un message en attente dans une queue.

        :param int retcode: Code d'identification de la queue à utiliser.

        :param int timeout: Timeout pour la réception du message.

        :return: Message en bytes.



    .. method:: flush( retcode)

        Méthode pour vider une queue.

        :param int retcode: Code d'identification de la queue à utiliser.

    .. method:: execute( opcode, *args, timeout=5)

        Méthode pour executer une requête avec un retour d'informations. 

        :param int opcode: Code d'identification de la requête à effectuer.
        :param bytes args: Arguments à transmettre à l'Arduino. Attention, les convertir en bytes avant envoi.
        :param int  timeout: Timeout de la réception (en secondes).
        :return: Arguments reçu de l'Arduino sous l'objet Deserialser. 

    .. method:: getuuid(timeout=5)

        Demande à l'Arduino son nom d'identification (ou UUID).

        :param int timeout: Timeout de la réception (en secondes) de l'identification.
        :return: L'identification de l'Arduino.


    .. method:: setuuid( uuid)

        Défini une nouvelle identification pour l'Arduino.

        :param uuid: Nouvelle identification pour l'Arduino.


    .. method:: getlog( retcode, timeout=0)

    .. method:: getout(timeout=0)

    .. method:: geterr(timeout=0):


    .. warning:: Les méthodes suivantes sont réservées à une utilisation interne.

    .. method:: process(message)

        Place un message sous forme de bytes provenant de l'Arduino dans une Queue grâce au retcode contenu dans le message.

        :param bytes message: Message à traiter.

    .. method:: rawsend()





************
Utilisation
************

Il existe deux possibilités pour utiliser cette librairie. Utiliser directement l'objet SeriaTalks, ce qui peut être vite fastidieux pour réaliser des actions autre que la manipulation d'UUID. L'autre option est de créer une classe qui dérive de SerialTalks qui va permettre une utilisation de l'Arduino très haut niveau.

Pour utiliser directement il faut d'abord importer la librairie :

.. code::

    from serialTalks import *

.. warning::

    Pour pouvoir faire l'importation depuis n'importe quel endroit, utiliser le code suivant : 

.. code::

    import os, sys, glob
    home = os.path.expanduser("~")
    for directory in glob.iglob(os.path.join(home, '**/team-2018/raspberrypi'), recursive=True):
    	sys.path.append(directory)


Il suffit ensuite de créer l'objet de le connecter comme ceci : 

.. code::
    
    arduino = SerialTalks('ardresse')
    arduino.connect()

La création de classe fille est un peu plus compliquée. Pour commencer il faut faire hériter notre nouvelle classe de SerialTalks comme ceci:

.. code::

    from serialtalks import *

    class Arduino(SerialTalks): 
        def __init__(self,adresse,..........):
            SerialTalks.__init__(self,adresse)
            .
            .

.. note:: Il est possible de ne pas écrire l'init si votre nouvelle object n'a pas besoin de variable pour son initialisation.

Ensuite il faut ajouter à cette classe des méthodes qui correspondront à des OP code. 
Voici un exemple simple d'envoi d'une variable float à l'Arduino.

.. code::

    def ordre(self, variable):

        self.send(OPCODE,FLOAT(variable))

On peut voir dans cette méthode l'utilisation de l'objet FLOAT, cette object venu tout droit de la librairie SerialUtils permet la conversion en bytes. Les objets de conversions sont expliqués dans le chapitre SerialUtils.

Pour indiquer l'OP code, il est vivement conseillé d'utiliser des constantes à definir en haut de votre fichier python de préférence en hexadécimal. Comme dans l'exemple ci contre.

.. code:: 

    OPCODE = 0xF4

.. warning:: Les opcodes suivants sont réservés par la lib et ne doivent pas être utilisés par vos objects : ``0x00`` , ``0x01`` , ``0x02``





.. |queue| replace:: Queue
.. _queue: https://docs.python.org/3.6/library/queue.html