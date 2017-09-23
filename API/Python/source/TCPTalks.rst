############
TCP Talks
############

TCPTalks est une librairie qui permet la communication entre deux terminales pythons.

*************
Preambule
*************

TCPTalks est une librairie utilisée pour faire la liaison entre deux ordinateurs (généralement utilisée entre un ordinateur et une Raspberry). Il peut également être utilisé en local pour une utilisation interne à la Raspberry.
Cette librairie utilise les librairies ``socket`` et ``pickle`` , l'une pour la communication et l'autre pour la sérialisation.
Cette librairie est capable de transférer toutes les données possibles, et même des objets si le destinataire en possède l'architecture.

TCPTalks pour fonctionner à besoin d'une partie client et d'une partie serveur. Cette différenciation est peu importante pour l'utilisation car les deux rôles possèdent les mêmes fonctionnalités.

Les packets de données sont comme celle de SerialTalks c'est à dire standardisés pour une meilleur utilisation. 
Il existe des packets maitre et esclave. Les packets maitres sont destinés à lancer une méthode chez le destinataire, alors que les messages esclaves sont destinés à se retrouver dans les listes de données reçu et ne peux donc rien déclencher.

Voici un schéma récapitulant la structure des packets transités par cette librairie :


Message **maitre** : 

.. image:: tab_tcptalks_1.png


Message **esclave** :


.. image:: tab_tcptalks_2.png



1. **Master Code**:
    Le Master code permet de faire la différence entre un packet esclave et maitre. Il vaut soit ``b'R'`` (maitre)  soit ``b'A'`` (esclave).
2. **OP Code**
    L'Op code est très important puisqu'il permet d'expliciter la requête. On associe pour chaque requête à executer un Op code. L'Op code n'est pas nessaire pour le message esclave car seul le retcode est utilisé pour identifier à quelle requête ce message répond.
3. **RET Code**
    Le RET code est utile pour les retours d'instructions. En effet si le destinataire a besoin de renvoyer des informations au programme python. il va utiliser ce code dans le packet retour pour permettre au programme python de bien associer avec quelle requête ces informations sont reliées.
4. **args et kwargs**:
    Une requête peux avoir une infinité d'arguments suplémentaire du moment que la taille n'est pas trop excessif.



.. note:: Il n'y a pas de TCPUtils car c'est la librairie ``pickle`` qui permet la sérialisation et la désérialisation.


**************
API
**************

La librairie contient deux objets, TCPTalks et TCPListener. TCPTalks est utile pour lancer les requêtes tandis que TCPListener s'occupe de recevoir et traiter les messages. Il est donc important de ne pas toucher à ce dernier.


.. class:: TCPTalks

    .. method:: __init__(ip=None, port=25565, password=None)

        :param ip: Permet de choisir de se connecter à un ip ou de se lancé en tant que serveur si égal à  **None**.

        :param int port: Indiquez le port à utilisé pour les communications avec ce TCPtalks. Il est possible de lancer plusieurs TCPTalks du moment que chaqu'un à un port different.

        :param password: Indiquez le mot de passe à utiliser.

        .. note:: Pour se connecter à un serveur sur le même ordinateur utilisez l'IP ``127.0.0.1``


    .. method:: __enter__()

        Méthode pour l'utilisation de ``with``

        :return TCPTalks: Retourne l'objet de communication connecté.


    .. method:: __exit__(exc_type, exc_value, traceback)

        Méthode pour l'utilisation de ``with``


        :param exc_type: Type de l'erreur.
        :param exc_value: Argument d'erreur.
        :param traceback: Trace de l'erreur.



    .. method:: connect(timeout=5)

        Connecte le socket avec les renseignements donnés au constructeur ``__init__``.

        :param timeout: Timeout pour la conexion du socket.


        :exception AlreadyConnectedError: Dans le cas ou le socket est déjà connecté.
        :exception ForeverAloneError: Dans le cas ou la connexion ne peux s'établir faute de réponse de la part du binome.
        :exception AuthentificationError: Dans le cas d'un mot de passe faux.


    .. method:: disconnect()

        Coupe les communications, le socket et le thread TCPListener.


    .. method:: bind(opcode, instruction):
        
        Bind permet d'associer un Opcode et une fonction ou méthode. La cible (instruction) sera executée à chaque fois que l'Op code est reçu. La méthode selectionnée peux renvoyer n'importe quels arguments, il sera automatiquement transmit à l'éméteur de la requête.
        
        :param opcode: Opcode à utiliser pour la requête.
        :param instruction: Adresse de la fonction a utiliser pour le bind.

        :exception KeyError: Dans le cas ou l'OpCode est déjà utilisé.

        .. note:: Pour donner l'adresse d'une méthode, il suffit d'indiquer son nom. Exemple ``print``.



    .. method:: send(opcode, *args, **kwargs)
    
        Permet l'envoi d'une requête sans récupérer directement la réponse du binome. Il est recommandé d'utiliser cette méthode pour les requêtes sans retours, mais permet dans le cas contraire de récupérer la reponse plus tard grâce au retcode retourné.

        :param opcode: Code pour identifier la requête
        :param args: Arguments suplémentaire à transmettre.
        :param kwargs: Arguments suplémentaire à transmettre nommés.

        :return: Le retcode a utiliser pour la réception de retour éventuel.

        :exception NotConnectedError: Levée si le socket n'est pas connecté.


    .. method:: execute(opcode, *args, timeout=5, **kwargs)

        Envoie une requête et retourne directement le résultat de celle-ci. Il est recommandé de l'utiliser si votre requête attend un retour de la part du binome.

        :param opcode: OPCode pour la requête.
        :param args: Arguments à mettre dans de la requête.
        :param timeout: Timeout pour la reception du resultat de la requête.
        :param kwargs: Arguments nommés à mettre dans de la requête.


    .. method:: get_queue(retcode)

        Récupère la |queue|_ qui est associée au retcode indiqué.

        :param retcode: Code de la |queue|_ .
        :return: |queue|_  qui est associée au retcode indiqué.


    .. method:: delete_queue(retcode)

        Supprime la |queue|_  associé au retcode indiqué. Dans la conception cette methode consiste à supprimer les données de la |queue|_ uniquement.

        :param retcode: Code de la |queue|_ à supprimer.
        

    .. methode reset_queues()

        Supprime de toutes les données reçus.


    .. method poll(retcode, timeout=0)

        Recupère un retour associé à un retcode.

        :param retcode: Retcode  pour retrouver le retour demandé.
        :param timeout: Timeout à utiliser pour récupérer l'information.


    .. method flush(retcode)

        Récupère toutes les informations reçu du retcode associé. Elle ne se termine que quand il n'y a plus d'informations à supprimer.

        :param retcode: Retcode à utiliser.



    .. warning::  Ces méthodes sont destinées à une utilisation interne, il est peu recommandé de les utiliser.


    .. method:: sendback(retcode, *args)

        Envoie le message esclave avec les arguments et le retcode associé à la reponse. Il est possible de définir soit même son retcode mais très peu pratique pour le retrouver chez le binome sans configuration au préalable.

        :param args: Arguments à transmettre.
        


    .. method:: process(message)

        Traite le message reçu. C'est à dire identifie quel type de message a été reçu (esclave ou maitre).

        :param message: Message en |tuples|_ reçu.


    .. method:: execinstruction(opcode, retcode, *args, **kwargs)

        Lance l'exécution de la fonction associée à l'OPCode et renvoie ce que la fonction retourne après son exécution. 

        :param opcode: Opcode de la requête.
        :param retcode: RetCode de la requête.
        :param args: Arguments à transmettre à la méthode lancée.
        :param kwargs: Arguments nommés à transmettre à la méthode lancée.

    .. method:: rawsend(rawbytes)

        Méthode permettant l'envoi direct de bytes au binome.

        :param rawbytes: Données à transmettre.

        :exception NotConnectedError: Levée si le socket n'est pas connecté.

    .. method:: _serversocket(port, timeout)

        Méthode privée pour la connexion du socket en tant que serveur.

        :param port: Port à utiliser pour le lancement du serveur.
        :param timeout: Timeout pour la connexion.
        :return: Retourne un objet socket utilisable pour la connexion.

    .. method:: _clientsocket(ip, port, timeout)

        Méthode privée pour la connexion à un serveur avec l'ip et le port.

        :param ip: Ip du serveur à connecter.
        :param port: Port à utiliser.
        :param timeout: Timeout utilisé pour la connexion au serveur.


    .. method:: _loads(rawbytes)

        Méthode qui permet d'isoler le premier message du rawbytes, ou renvoie une erreure si le rawbytes n'est constitué que d'un message incomplet.

        :exception pickle.UnpicklingError: Levée si le rawbytes n'est constitué que d'un message incomplet.
        :exception AttributeError: Levée si le rawbytes n'est constitué que d'un message incomplet.
        :exception EOFError: Levée si le rawbytes n'est constitué que d'un message incomplet.






..class:: TCPListener(Thread)
    
    .. method:: __init__(parent)

        Constructeur du TCPListener.

        :param parent: Objet TCPTalks auquel le TCPListener sera rataché.


    .. method:: run()

        Méthode principal du Thread, elle permet la reception des messages et l'envoie pour traitement à TCPTalks.




************
Utilisation
************


Il faut bien comprendre que dans cette librairie la connexion n'est pas exactement symétrique. Puis qu'il faut choisir qui sera le serveur et qui sera le client. 
Il est donc important de bien choisir les rôles pour une bonne utilisation.


Dans ce petit guide, je vous montrerai une utilisation basique de la librairie avec quelques astuces.


Pour établir une connexion il suffit d'écrire les lignes suivantes.

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

La prochaine étape est d'affecter des méthodes ou fonctions à un opcode pour pouvoir répondre à des requêtes.



.. code:: 

    tcplink.bind(0xFF,``fonction``)

Pour la réalisation de fonction utilisable par la librairie, il n'y a pas beaucoup de contrainte, puisque le TCPtalks va remplir tous les champs de la fonction avec les données reçu.
S'il manque des arguments dans la requête la librairie lèvera une erreur chez l'émetteur de cette requête.

Pour retourner des arguments il suffit de les mettre dans le return de la méthode. Il est possible d'avoir plusieurs return différents avec un nombre d'arguments différents.

Exemple : 

.. code::

    def fonction(texte):
        print(texte)

        return ("Bien reçu",10)


Dans cet exemple, la fonction va quand elle sera appelée par TCPTalks afficher le paramètre reçu dans la requête avec l'OPCode qui était associé à cette fonction. Elle va ensuite renvoyer deux variables, un texte et un entier.
Cet exemple reste très basique, mais illustre bien le peu de contrainte qu'impose TCPTalks.


Il ne reste plus qu'à lancer l'instruction que nous venons de créer. Pour finir ce petit tutoriel, je vais montrer les deux méthodes pour une parfaite exécution de la commande.
La première méthode qui est la plus simple quand il faut appeler une requête qui attend un retour comme avec la fonction que nous avons créé  juste au-dessus.

.. code:: 

    tcplink.execute(0xFF,"tu me reçois ?")
    #Cette ligne va naturelement renvoyer le tuple ("Bien reçu",10)

La deuxième méthode moins recommandée (pour des raisons de gestion d'erreur à distance) consiste à utiliser les deux méthodes send et poll.

.. code::

    #envoi de la requête
    retcode = tcplink.send(0xFF,("tu me reçois?")

    #reception du rendu de la requête
    tcplink.poll(retcode)
    #Cette ligne affiche naturellement le tuple  ("Bien reçu",10).


    




.. |tuples| replace:: Tuples
.. _tuples: https://docs.python.org/3/library/stdtypes.html?highlight=tuples



.. |queue| replace:: Queue
.. _queue: https://docs.python.org/3.6/library/queue.html