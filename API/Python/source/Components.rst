############
Components
############

Components est une libraire qui permet une utilisation de SerialTalks à travers TCPTalks. Cette librairie est très pratique pour la réalisation intelligence puisqu'elle permet de pouvoir exécuter l’intelligence depuis l'ordinateur sans à avoir à rentrer dans la Raspberry.

**************
Préambule
**************

Cette librairie est purement python, puisqu'elle est exécuté par la Raspberry et un ordinateur. Son principal rôle comme indiqué précédemment est d'externaliser l'utilisation de SerialTalks et des objets dérivés de celui-ci (ce reporté au chapitre utilisation de SerialTalks).

Pour cette librairie il existe plusieurs type d’éléments, tout d'abord les classes principales qui permettent la communication (ordi-rasp) c'est à dire Manager (client) et Serveur.
Chacune de ces entités à besoins d'objets pour matérialiser un Arduino ou d'autre objets accessibles à distance.

Du côté de la Raspberry et de l'objet Serveur, ils existent des objets appelés "component". Chaque component représente un élément  utilisable à distance (exemple : Arduino GPIO devices etc). Ces éléments se créent sur demande du client.
De l'autre côté le client utilise des objets Proxy qui vont utiliser l'objet Managers pour créer leurs homologues (component) et communiquer avec eux.

**************
Server
**************
Dans ce chapitre nous mettrons à disposition l'API.


API
----------------

Dans cette API, vous trouverez en premier le serveur puis tous les components disponibles à ce jour.


Le serveur utilise un dictionnaire pour stocker les components. Dans ce dictionnaire vous trouverez le nom ou (compid) associé à un objet component (comp).

.. class:: Server(TCPTalks)

        Server est la classe principal pour la communication de la Raspberry vers un client.

    .. method:: __init__(port=COMPONENTS_SERVER_DEFAULT_PORT, password=None)

        Constructeur du serveur.

        :param port: Port à utiliser pour le TCPTalks.
        :param password: Mot de passe à utiliser pour le TCPTalks.


    .. method:: disconnect

        Déconnecte le client du serveur et tous les components.

    .. method:: cleanup

        Déconnecte tous les components connecté à la Raspberry.

    .. method:: addcomponent(comp, compid)

        Ajoute un component avec un identifiant associée.

        :param component comp: L'objet component à ajouter au serveur.
        :param compid: Nom associé au component à ajouter.

    .. warning:: Les méthodes suivantes sont normalement réservées à TCPTalks et donc au client.

    .. method:: MAKE_COMPONENT_EXECUTE(compid, methodname, args, kwargs)

        Permet au client d'executer une méthode d'un objet component associé au serveur avec le code d'identification compid.

        :param compid: Identifiant du component à utiliser.
        :param methodname: Nom de la méthode à appelée .
        :param args: Arguments à transmettre à la méthode appelée.
        :param kwargs: Arguments nommés à transmettre à la méthode appelée.
        
    
    .. method:: GET_COMPONENT_ATTRIBUTE(compid, attrname)

        Permet au client d'optenir une variable d'un component.

        :param compid: Identifiant du component à utiliser.
        :param attrname: Nom de l'attribut demandé.


    .. method:: SET_COMPONENT_ATTRIBUTE(compid, attrname, attrvalue)

        Permet au client de modifier une variable d'un component.

        :param compid: Identifiant du component à utiliser.
        :param string attrname: Nom de la variable à modifier.
        :param attrvalue: Nouvelle valeur de la variable à modifier.



    .. method:: CREATE_SERIALTALKS_COMPONENT(uuid)

        Permet au client de connecter des components de type SerialTalks.

        :param uuid: Code d'identification de l'arduino à connecter.


    .. method:: CREATE_SWITCH_COMPONENT(switchpin)

        Permet au client de paramétrer un interrupteur sous le GPIO de la Raspberry et de creer le component associé.

        :param switchpin: Pin du GPIO de la Raspberry à utiliser.


    .. method:: CREATE_LIGHTBUTTON_COMPONENT(switchpin, ledpin)

        Permet de paramétrer un bouton-led sous le GPIO de la Raspberry et de creer le component associé.

        :param switchpin:  Pin du GPIO de la Raspberry à utiliser.
        :param ledpin: Pin du GPIO à utiliser pour la lumière du bouton.


    .. method:: CREATE_PICAMERA_COMPONENT(resolution, framerate)

        Permet de parametrer la caméra branchée en direct sur la raspberry et de creer le component associé.

    
Dans la suite de cette API nous traiterons des components implémentés.


.. class:: Component

    .. method:: _setup()

        Cette méthode est appelée  à la création du component, elle peut être modifiée en fonction des besoins de chaque components.

    .. method:: _clean()

        Cette méthode est appelée à la déconnexion du component, elle peut être modifiée en fonction des besoins de chaque components.


Voici le component utilisé pour les Arduinos, il utilise la librairie SerialTalks.


.. class:: SerialTalksComponent(SerialTalks, Component)

    .. method:: __init__(uuid)

        Constructeur du component.

        :param uuid: Identifiant de l'Arduino à utiliser pour la connexion.


    .. method:: _setup()

        Connecte l'Arduino.

    .. method:: _cleanup()

        Déconnecte l'Arduino.

.. note:: Il existe aussi toutes les méthodes du serialTalks.

Les deux components suivants sont destiné à l'utilisation du GPIO.


.. class:: SwitchComponent(Switch, Component)

    .. method:: __init__(switchpin)
    
        Constructeur du component. Il paramètre le pin du  GPIO également pour une utilisation immédiate sans setup.
        :param switchpin: Pin à utiliser.


    .. method:: _cleanup()

        Libère le pin utiliser pour une futur utilisation.


.. class:: LightButtonComponent(LightButton, Component)

    .. method:: __init__(switchpin, ledpin)

        Constructeur du component. Il paramètre les pins du GPIO également pour une utilisation immédiate sans setup.

        :param switchpin: Pin à utiliser.
        :param ledpin: Pin à utiliser pour la lumière du bouton.

        

    .. method:: _cleanup()

        Libère les pins monopolisés pour une autre utilisation.




Le dernier component permet l'utilisation de la caméra.


.. class:: PiCameraComponent(PiCamera, Component)

    .. method:: __init__(server, resolution, framerate)

        Constructeur du component.

        :param server:
        :param resolution: Résolution à paramétrer.
        :param framerate: Rafraichissement à utiliser.



    .. method:: generate_streams_and_send_their_values(self, server, compid)



    .. method:: start_capture()


    .. method:: stop_capture()


    .. method:: _cleanup()
    
        Déconnecte la caméra.



**************
Manager
**************

Cette partie sur Manager n'est composée que de l'API.



API
----------------------------------------------


Pour commencer voici l'objet Manager.


.. class:: Manager

    .. method:: __init__(ip='localhost', port=COMPONENTS_SERVER_DEFAULT_PORT, password=None)

        Constructeur de Manager, il va paramétrer le TCPTalks pour établir la connexion avec le serveur.

        :param ip: Adresse du serveur (l'ip de la Raspberry).
        :param port: Port à utiliser pour le TCPTalks, attention il dois être le même que celui du serveur.
        :param password: Mot de passe utilisé par le serveur.


    .. note:: Les méthodes suivantes sont destinées à une utilisation par le serveur via TCPTalks.

    .. method:: UPDATE_MANAGER_PICAMERA(compid, streamvalue)

        Permet au serveur d'envoyer le flux de la vidéo.

        :param compid: ID de la caméra à l'origine du flux.
        :param streamvalue: Flux.

    .. method:: MAKE_MANAGER_EXECUTE(compid)

        Permet au serveur d'executer une commande associée au component. Cette association est réalisée dans les proxys.

        :param compid: Identification du component.


Nous allons finir par les Proxys. Ces objets ont pour objectif de parfaitement simuler une utilisation en local de l'objet .C'est à dire que si on prend l'exemple de SeriaTalks, le proxy va imiter toutes les commandes en les modifiants un peu pour que l'utilisateur puisse les utiliser comme avec un objet SeriaTalks classique.

Nous allons détailler le fonctionnement de l'objet proxy pour une meilleur compréhension.

.. class:: Proxy

    .. method:: __init__(manager, compid, attrlist, methlist)

        Constructeur du Proxy, très important car il va creer des méthodes à partir des arguments données. Le constructeur va donc creer pour chaque élement de methlist une méthode parfaitement utilisable qui va consister à envoyer vias le TCPTalks l'OPCode MAKE_COMPONENT_EXECUTE avec tous les arguments données.
        
        :param Manager manager: Cet objet correspond au TCPTalks à utiliser pour communiquer avec les components.
        :param compid: Compid représente le component qui dois être créer avec cette objet.
        :param attrlist: Liste des attributs du component associé.
        :param methlist: Liste des fonctions du component associé.

    .. method:: __getattr__(attrname, tcptimeout=10)

        La méthode d'accès aux variables. Cette méthode regarde si la variable appelé est dans la liste des arguments du component associé. Si c'est bien le cas, il envoie une requête TCPTalks pour obtenir cette valeur et la renvoie.

        :param attrname: Nom de l'atribut demandé.
        :param tcptimeout: Timeout pour la requête TCPTalks.
        :return: Retourne la valeur de l'attribu demandé.


    .. method:: __setattr__(attrname, attrvalue, tcptimeout=10)

        La méthode de modification de variable. Cette méthode regarde si la variable apellé est dans la liste des arguments du component associé. Si c'est bien le cas, il envoye une requête de modification de cette variable vias TCPTalks.

        :param attrname: Nom de l'attribut à modifier.
        :param attrvalue: Nouvelle valeur de l'attribue.
        :param tcptimeout: Timeout à utliser pour la requête TCPTalks.

Dans les objets qui héritent de proxy, on va pouvoir dans le constructeur modifier la liste des attributs et des méthodes en fonction du component auquel on fait référence. Le constructeur de proxy se chargera de  créer les méthodes avec le bon Opcode pour obtenir un nouveau proxy parfaitement utilisable.

Le proxy de SerialTalks

.. class:: SerialTalksProxy(Proxy)

    .. method:: __init__(manager, uuid)

        Constructeur de SerialTalksProxy avec un uuid d'Arduino.

        .. data:: attrname = ['port', 'is_connected']
            methlist = ['connect', 'disconnect', 'send', 'poll', 'flush', 'execute', 'getuuid', 'setuuid', 'getout', 'geterr']

        :param uuid: Code d'identification de l'Arduino à utiliser.


.. class:: SwitchProxy(Proxy)

    .. method:: __init__(manager, switchpin)

        Constructeur du proxy.

        .. data:: attrname = ['state', 'PinInput']
            methlist = ['Close']

        :param Manager manager: Object pour la comunication en TCPTalks.
        :param switchpin: Pin GPIO à utiliser.

	.. method:: SetFunction(function, *args):

        méthode d'association de la méthode à un compid pour la requête MAKE_MANAGER_EXECUTE.

        :param function: Adresse de la fonction à utiliser.
        :param args: Arguments à utiliser pour la fonction.




.. class:: LightButtonProxy(Proxy)

    .. method:: __init__(manager, switchpin, ledpin)

        Constructeur du proxy.

        .. data:: attrname = ['state', 'PinInput', 'PinLight']
            methlist = ['SetAutoSwitch', 'On', 'Off', 'Switch', 'Close']

        :param Manager manager: Object pour la comunication en TCPTalks.
        :param switchpin: Pin GPIO à utiliser pour le bouton.
        :param ledpin: Pin GPIO pour la lumière du bouton.

    


	.. method:: SetFunction(function, *args):

        Méthode d'association de la méthode à un compid pour la requête MAKE_MANAGER_EXECUTE.

        :param Manager manager: Objet pour la comunication en TCPTalks.
        :param function: Adresse de la fonction à utiliser.
        :param args: Arguments à utiliser pour la fonction.




.. class:: PiCameraProxy(Proxy)

    .. method:: __init__(manager, resolution, framerate)

        Constructeur du proxy de la picamera.

        .. data:: attrlist = ['resolution', 'framerate']
            methlist = ['start_capture', 'stop_capture']

        :param Manager manager: Object pour la comunication en TCPTalks.
        :param resolution: Résolution à paramétrer.
        :param framerate: Taux de Rafraichissement à utiliser.



