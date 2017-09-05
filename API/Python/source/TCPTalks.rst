############
TCP Talks
############

TCPTalks est une librairie qui permet la communication entre deux terminales pythons.

*************
Preambule
*************

TCP Talks est une librairie utilisé pour faire la liaison entre les arduinos et un ordinateur. Il peux également être utilisé en local pour une utilisation interne à la raspberry.
Cette librairie utilise les librairie ``socket`` et ``pickle`` , l'un pour la communication et l'autre pour la serialisation.
Cette librairie est capable de transférer n'importe quelles données, et même des objects si le destinataire en possède l'architecture.

TCPTalks pour fonctionner à besoin d'une partie client et d'une partie serveur. Cette differenciation est peu importante pour l'utilisation car les deux roles possèdents les même fonctionalités.

Les packets de données sont comme celle de SerialTalks c'est a dire standardisés pour une meilleur utilisation. 
Il existe des packets maitre et esclave. Les packets maitres sont destiné à lancer une methode chez le destinataire, alors que les messages esclaves sont destinés à se retrouver dans les listes de données reçu et ne peux donc rien déclancher.

Voici un shema récapitulant la structure des packets transités par cette librairie :

Message **maitre** : 

.. image:: tab_tcptalks_1.png


Message **esclave** :


.. image:: tab_tcptalks_2.png



1. **Master Code**:
    Le Master code permet de faire la difference entre un packet esclave et maitre. Il vaut soit ``b'R'`` (maitre)  soit ``b'A'`` (esclave).
2. **OP Code**
    L'Op code est très important puisqu'il permet d'explicité la requette. On associe pour chaque requette à executer un Op code. L'Op code n'est pas nessaire pour le message esclave car seul le retcode est utilisé pour identifié à quel requette ce message repond.
3. **RET Code**
    Le RET code est utile pour les retours d'instructions. En effet si le destinataire a besoin de renvoyé des informations au programme python. il va utilisé ce code dans le packet retour pour permettre au programme python de bien associé avec quel requette ces informations sont reliés.
4. **args et kwargs**:
    Une requette peux avoir une infinité d'arguments suplémentaire du moment que la taille n'est pas trop excessif.



.. note:: Il n'y a pas de TCPUtils car c'est la librairie ``pickle`` qui permet la serialisation et la deserialisation.


**************
API
**************

La librairie contient deux objects, TCPTalks et TCPListener. TCPTalks est utile pour lancer les requettes tandis que TCPListener s'occupe de recevoir et traités les messages. Il est donc important de ne pas touché a ce dernier.


.. class:: TCPTalks

    .. method:: __init__(ip=None, port=25565, password=None)

        :param ip: Permet de choisir de se connecter à un ip ou de se lancé en tant que serveur si égal à  **None**.

        :param int port: Indiquez le port à utilisé pour les communications avec ce TCPtalks. Il est possible de lancer plusieurs TCPTalks du moment que chaqu'un à un port different.

        :param password: Indiquez le mot de passe a utiliser.

        .. note:: Pour se connecter à un server sur le même ordinateur utilisez l'IP ``127.0.0.1``


    .. method:: __enter__()

        Methode pour l'utilisation de ``with``

        :return TCPTalks: Retourne l'object de communication connecté.


    .. method:: __exit__(exc_type, exc_value, traceback)

        Methode pour l'utilisation de ``with``


        :param exc_type: type de l'erreur
        :param exc_value: argument d'erreur
        :param traceback: trace de l'erreur



    .. method:: connect(timeout=5)

        Lance la connexion du socket avec les renseignements données au constructeur ``__init__``.

        :param timeout: Timeout à utiliser pour la conexion du socket.


        :exception AlreadyConnectedError: Dans le cas ou le socket est déjà connecté.
        :exception ForeverAloneError: Dans le cas ou la connexion ne peux s'établir faute de réponse de la part du binome.
        :exception AuthentificationError: Dans le cas d'un mot de passe faux


    .. method:: disconnect()

        Coupe les communications, le socket et le thread TCPListener.


    .. method:: bind(opcode, instruction):
        
        Bind permet d'associé un Opcode et une fonction ou methode. La cible (instruction) sera executé a chaque fois que l'Op code est recu. La methode selectionner peux renvoyer n'importe quels arguments, il sera automatiquement transmit à l'éméteur de la requette.
        
        :param opcode: Opcode à utiliser pour la requette
        :param instruction: Adresse de la fonction a utiliser pour le bind.

        :exception KeyError: Dans le cas ou l'OpCode est déjà utilisé.

        .. note:: Pour donner l'adresse d'une méthode, il suffit d'Indiquer son nom. Exemple ``print``.



    .. method:: send(opcode, *args, **kwargs)
    
        Permet l'envoie d'une requette sans récupérer directement la réponse du binome. Il est recommandé d'utiliser cette methode pour les requettes sans retours, mais permet dans le cas contraire de récupérer la reponse plus tard grace au retcode retourné.

        :param opcode: Code a utilisé pour identifier la requette
        :param args: Arguments suplémentaire à transmettre.
        :param kwargs: Arguments suplémentaire à transmettre només.

        :return: Le retcode à utilisé pour la reception de retour éventuel.

        :exception NotConnectedError: Levé si le socket n'est pas connecté.


    .. method:: execute(opcode, *args, timeout=5, **kwargs)

        Execute permet l'envoie d'une requette et retourne directement le resultat de celle-ci. Il est recommandé de l'utilisé si votre requette attend un retour de la part du binome

        :param opcode: OPCode a utlisé pour la requette.
        :param args: Arguments à envoyer pour la bonne execution de la requette.
        :param timeout: Timeout à utiliser pour la reception du resultat de la requette.
        :param kwargs: Arguments nommés à envoyer pour la bonne execution de la requette.


    .. method:: get_queue(retcode)

        get_queue permet de récuperer la |queue|_ qui est associé au retcode indiqué. Peut importe si elle est vide ou non.

        :param retcode: Code de la |queue|_ à retourner.
        :return: Retourne la |queue|_  qui est associé au retcode indiqué.


    .. method:: delete_queue(retcode)

        Methode pour la suppression de la |queue|_  associé au retcode indiqué. Dans la conception cette methode consiste à supprimer les données de la |queue|_ uniquement.

        :param retcode: Code de la |queue|_ à supprimer.
        

    .. methode reset_queues()

        Permet la suppression de toutes les données reçus.


    .. method poll(retcode, timeout=0)

        Poll permet de récuperer un retour associé à un retcode.

        :param retcode: Retcode à utiliser pour retrouver le retour demandé.
        :param timeout: Timeout à utiliser pour récupérer l'information.


    .. method flush(retcode)

        Flush récupère toutes les informations reçu du retcode assicié. Elle ne se termine que quand il n'y a plus d'informations à supprimer.

        :param retcode: Retcode à utiliser.



    .. warning::  Ces methodes sont destiées à une utilisation interne, il est peu recommandé de les utiliser.


    .. method:: sendback(retcode, *args)

        Methode destinée à une utilisation interne. Permet l'envoie du message esclave avec les arguments et le retcode associé à la reponse. Il est possible de définir soit même son retcode mais très peu pratique pour le retrouver chez le binome sans configuration au préalable.

        :param args: Arguments a transmettre dans le message esclave.
        


    .. method:: process(message)

        Permet de traités le message reçu. C'est à dire identifier quel type de message (esclave ou maitre) .

        :param message: Message en |tuples|_ recu.


    .. method:: execinstruction(opcode, retcode, *args, **kwargs)

        Cette methode lance l'execution de la fonction associé à l'OPCode et renvoie ce que la fonction retourne après son execution. 

        :param opcode: Opcode de la requette a traiter.
        :param retcode: RetCode de la requette en cours de traitement.
        :param args: Arguments à transmettre à la methode lancée.
        :param kwargs: Arguments nommés à transmettre à la methode lancée.

    .. method:: rawsend(rawbytes)

        Methode permettant l'envoie direct de bytes au binome.

        :param rawbytes: Données à transmettre.

        :exception NotConnectedError: Levé si le socket n'est pas connecté.

    .. method:: _serversocket(port, timeout)

        Methode privée pour la connexion du socket en tant que serveur.

        :param port: Port à utiliser pour le lancement du serveur.
        :param timeout: Timeout à utiliser pour la connexion.
        :return: Retourne un object socket utilisable pour la connexion.

    .. method:: _clientsocket(ip, port, timeout)

        Methode privée pour la connexion à un serveur avec l'ip et le port.

        :param ip: Ip du serveur à connecter.
        :param port: Port à utiliser pour la connexion.
        :param timeout: Timeout utilisé pour la connexion au serveur.


    .. method:: _loads(rawbytes)

        Methode qui permet d'isolé le premier message du rawbytes, ou renvoie une erreure si le rawbytes n'est constitué que d'un message incomplet.

        :exception pickle.UnpicklingError: Levée si le rawbytes n'est constitué que d'un message incomplet.
        :exception AttributeError: Levée si le rawbytes n'est constitué que d'un message incomplet.
        :exception EOFError: Levée si le rawbytes n'est constitué que d'un message incomplet.






..class:: TCPListener(Thread)
    
    .. method:: __init__(parent)

        Constructeur du TCPListener.

        :param parent: Object TCPTalks auquel le TCPListener sera rataché


    .. method:: run()

        Methode principal du Thread, elle permet la reception des messages et l'envoie pour traitement à TCPTalks.




************
Utilisation
************


Il faut bien comprendre que dans cette librairie la connexion n'est pas exactement symetrique. Puisque qu'il faut choisir qui sera le serveur et qui sera le client. 
Il est donc important de bien choisir les rôles pour une bonne utilisation.


Dans ce petit guide je vous montrerai une utilisation basique de la librairie avec quelques astuces.


Pour etablir une connexion il suffit d'écrire les lignes suivantes.

.. note:: Il est possible d'utiliser cette librairie en interne avec l'IP ``127.0.0.1``.

Côté client : 

.. code::

    from TCPTalks import *

    #creation du TCPTalks
    tcplink = TCPTalks("127.0.0.1",1000)

    #Connexion au client
    tcplink.connect()
    
Côté serveur:

.. code::

    from TCPTalks import *

    #creation du TCPTalks
    tcplink = TCPTalks(port=1000)

    #Connexion au serveur
    tcplink.connect()

Une fois la connexion faite, il n'y a plus de difference dans le fonctionnement de la lib entre serveur et client.

La prochaine étape est d'affecter des methodes ou fonctions à un opcode pour pouvoir repondre à des requettes.



.. code:: 

    tcplink.bind(0xFF,``fonction``)

Pour la realisation de fonction utilisable par la librairie, il n'y a pas beaucoup de contraite, puisque le TCPtalks va remplir tous les champs de la fonction avec les données reçu.
Si il manque des arguments dans la requettes la librairie lèvera une erreur chez l'emetteur de cette requette.

Pour retourner des arguments il suffit de les mettres dans le return de la methode. Il est possible d'avoir plusieurs return différents avec un nombre d'arguments differents.

Exemple : 

.. code::

    def fonction(texte):
        print(texte)

        return ("Bien reçu",10)






.. |tuples| replace:: Tuples
.. _tuples: https://docs.python.org/3/library/stdtypes.html?highlight=tuples



.. |queue| replace:: Queue
.. _queue: https://docs.python.org/3.6/library/queue.html