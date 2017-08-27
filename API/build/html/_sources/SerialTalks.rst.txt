############
SerialTalks
############

La librairie SerialTalks assure la comunication entre une ordinateur et un arduino.
On trouve dans cette librairie deux versions asymétriques pour chaque terminal.

**************
Python Object
**************
Pour ouvrir les comunications avec un arduino, il faut creer un object SerialTalks et lancé la connexion avec les méthodes disponibles de celle-ci.

Object SerialTalks
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

        :return: Renvoie l'object `Queue <https://docs.python.org/3.6/library/queue.html>`_ relié avec le retcode.


    .. method:: delete_queue(retcode)

        Permet la suppression d'une `Queue <https://docs.python.org/3.6/library/queue.html>`_

        :param int retcode: Code d'indentification de la queue à supprimer.

    .. method:: reset_queues()

        Permet la suppression de toutes les `Queues <https://docs.python.org/3.6/library/queue.html>`_ .



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
        :param bytes args: Argument à transmettre à l'arduino, attention les convertir en bytes avant ( voir :ref:`my-reference-label`)
        :param int  timeout: Timeout de la reception (en seconde).
        :return: Arguments recu de l'arduino sous l'object Deserialser voir :ref:`my-reference-label`

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



.. _my-reference-label:


Object de SerialUtils
--------------------------


.. class:: Deserialser


**************
Arduino Object
**************