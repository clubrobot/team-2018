############
Components
############

Components est une libraire qui permet une utilisation de SerialTalks à travers TCPTalks. Cette librairie est très pratique pour la réalisation d'intéligence puisqu'elle permet de pouvoir executer l'inteligence depuis l'ordinateur sans à avoir à rentrer dans la raspberry.


**************
Préambule
**************

Cette librairie est purement python, puisqu'elle est executer par la raspberry et un ordinateur. Son principal rôle comme indiqué précedement est d'externalisé l'utilisation de SerialTalks et des objects dérivés de celui-ci (ce reporté au chapitre utilisation de SerialTalks).

Pour cette librairie il existe plusieurs type d'elements, tout d'abord les classes principals qui permettent la communication c'est à dire Manager (client) et Serveur.
Chacune de ces entités à besoins d'objects pour matérialisé un arduino ou d'autre object accessible à distance.

Du côté de la raspberry et de l'object Serveur,ils existents des objects apellés "component". Chaque component représente un element  utilisable a distance (arduino , gpio devices). Ces elements se creent sur demande du client.
De l'autre côté le client utilise des objects Proxy qui vont utiliser l'object Managers pour creer leurs homologues (component) et communiquer avec eux.



**************
Server
**************
Dans ce chapitre nous metterons a disposition l'API .


API
----------------

Dans cette API, vous trouverez en premier le serveur puis tous les components disponibles à ce jour.


Le serveur utilise un dictionnaire pour stocker les components. Dans ce dictionnaire vous trouverer le nom ou (compid) associé à l'object component (comp).

.. class:: Server(TCPTalks)

        Server est la classe principal pour la communication de la raspberry vers un client.

    .. method:: __init__(port=COMPONENTS_SERVER_DEFAULT_PORT, password=None)

        Constructeur du serveur.

        :param port: Port à utiliser pour le TCPTalks
        :param password: Mot de passe à utiliser pour le TCPTalks


    .. method:: disconnect

        Disconnect permet de deconnecter le client du serveur et de déconnecter tous les components.

    .. method:: cleanup

        Cette methode permet de déconnecter tous les components connecté à la raspberry.

    .. method:: addcomponent(comp, compid)

        Permet l'ajout d'un component avec un identifiant associé.

        :param component comp: L'object component à ajouter au serveur.
        :param compid: Nom associé au component à ajouter.

    .. warning:: Les mothodes suivantes sont normalement réservé à TCPTalks et donc au client.

    .. method:: MAKE_COMPONENT_EXECUTE(compid, methodname, args, kwargs)

        Methode qui permet au client d'executer une methode de d'un object component associé au serveur grâce au code d'identification compid.

        :param compid: identifiant du component à utiliser.
        :param methodname: Nom de la méthode à apeller.
        :param args: Arguments à transmettre à la methode apellé.
        :param kwargs: Arguments nommé à transmettre à la methode apellé.
        
    
    .. method:: GET_COMPONENT_ATTRIBUTE(compid, attrname)

        Methode qui permet au client d'optenir une variable d'un component.

        :param compid: Identifiant du component à utiliser.
        :param attrname: Nom de l'attribut demandé.


    .. method:: SET_COMPONENT_ATTRIBUTE(compid, attrname, attrvalue)

        Methode qui permet au client de modifier une variable d'un component.

        :param compid: Identifiant du component à utiliser.
        :param string attrname: Nom de la variable à modifier.
        :param attrvalue: Nouvelle valeur de la variable à modifier.



    .. method:: CREATE_SERIALTALKS_COMPONENT(uuid)

        Cette methode permet au client de connecté des components de type SerialTalks.

        :param uuid: Code d'identification de l'arduino à connecter.


    .. method:: CREATE_SWITCH_COMPONENT(switchpin)

        Cette methode permet au client de paramétrer un interrupteur sous le GPIO de la raspberry et de creer le component associé.

        :param switchpin: Pin du GPIO de la raspberry à utiliser.


    .. method:: CREATE_LIGHTBUTTON_COMPONENT(switchpin, ledpin)

        Cette methode permet de paramétrer un bouton-led sous le GPIO de la raspberry et de creer le component assicié.

        :param switchpin:  Pin du GPIO de la raspberry à utiliser pour le bouton.
        :param ledpin: Pin du GPIO à utiliser pour la lumière du bouton.


    .. method:: CREATE_PICAMERA_COMPONENT(resolution, framerate)

        Cette methode permet de parametrer la caméra branché en direct sur la raspberry et de creer le component associé.

    
Dans la suite de cette API nous traiterons des components implémenté dans cette librairie.


.. class:: Component

    .. method:: _setup()

        Cette methode est apeller à la creation du component, elle peut être modifier en fonction des besoins de chaque components.


    .. method:: _clean()

        Cette methode est apeller à la déconnection du component, elle peut être modifier en fonction des besoins de chaque components.



Voici le component utilisé pour les arduinos qui utilise la librairie SerialTalks.


.. class:: SerialTalksComponent(SerialTalks, Component)

    .. method:: __init__(uuid)

        Constructeur du component.

        :param uuid: identifiant de l'arduino à utiliser pour la connexion.


    .. method:: _setup()

        Connecte l'arduino.

    .. method:: _cleanup()

        Déconnecte l'arduino.

.. note:: Il existe aussi toutes les methodes du serialTalks.

Les deux components suivants sont destiné à l'utilisation du GPIO.


.. class:: SwitchComponent(Switch, Component)

    .. method:: __init__(switchpin)
    
        Constructeur du component. Il parametre le pin du  GPIO également pour une utilisation immédiate sans setup.
        :param switchpin: Pin à utiliser pour l'interrupteur.


    .. method:: _cleanup()

        Cette methode libère le pin utiliser pour une futur utilisation.


.. class:: LightButtonComponent(LightButton, Component)

    .. method:: __init__(switchpin, ledpin)

        Constructeur du component. Il parametre les pins du GPIO également pour une utilisation immédiate sans setup.

        :param switchpin: Pin à utiliser pour le bouton.
        :param ledpin: Pin à utiliser pour la lumière du bouton.

        

    .. method:: _cleanup()

        Cette methode libère les pins monopolisés pour une autre utilisation.




Le dernier component permet l'utilisation de la caméra.


.. class:: PiCameraComponent(PiCamera, Component)

    .. method:: __init__(server, resolution, framerate)

        Constructeur du component.

        :param server:
        :param resolution: Resolution à parametrer pour la caméra.
        :param framerate: Rafraichissement à utiliser pour la caméra.



    .. method:: generate_streams_and_send_their_values(self, server, compid)



    .. method:: start_capture()


    .. method:: stop_capture()


    .. method:: _cleanup()
    
        Déconnecter la caméra 



**************
Manager
**************

Dans cette partie nous metterons à disposition l'API.



API
----------------------------------------------


Pour commencé voici l'object Manager.


.. class:: Manager

    .. method:: __init__(ip='localhost', port=COMPONENTS_SERVER_DEFAULT_PORT, password=None)

        Cette methode est le constructeur de Manager, elle va parametrer le TCPTalks pour établir la connexion avec le serveur.

        :param ip: C'est IP du serveur auquel vous voulez vous connecter (l'ip de la raspberry)
        :param port: Port à utiliser pour le TCPTalks, attention il dois être le même que celui du serveur.
        :param password: Mot de passe utilisé par le serveur.


    .. note:: Les methodes suivantes sont destiné à une utilisation par le serveur via TCPTalks.

    .. method:: UPDATE_MANAGER_PICAMERA(compid, streamvalue)

        Methode qui permet au serveur d'envoyer le flux de la vidéo.

        :param compid: ID de la caméra à l'origine du flux
        :param streamvalue: flux

    .. method:: MAKE_MANAGER_EXECUTE(compid)

        Methode qui permet au serveur d'executer une commande associé au component. Cette association est réalisé dans les proxys.

        :param compid: Identification du component.


Nous allons finir par les Proxys. Ces objects ont pour objectif de parfaitement simuler une utilisation en interne de l'object .C'est à dire que si on prend l'exemple de SeriaTalks, le proxy de celui ci va imiter toutes les commandes en les modifiants un peu pour que l'utilisateur puisse l'utiliser comme un seriatalks classique.

Nous allons détailler le fonctionnement de l'object proxy pour une meilleur compréhension.

.. class:: Proxy

    .. method:: __init__(manager, compid, attrlist, methlist)

        Le constructeur du Proxy est très important puisqu'il va ensuite creer des methodes à partir des arguments données. Le constructeur va donc creer pour chaque element de methlist une methode parfaitement utilisable qui va consister à envoyer vias le TCPTalks l'OPCode MAKE_COMPONENT_EXECUTE avec tous les arguments données.
        
        :param Manager manager: Cette object correspond au TCPTalks à utiliser pour communiquer avec les components.
        :param compid: Compid représente le component qui dois être creer avec cette object.
        :param attrlist: Liste des attributs du component associé.
        :param methlist: Liste des fonctions du component associé.

    .. method:: __getattr__(attrname, tcptimeout=10)

        La methode d'accès au variable. Cette methode regarde si la variable apellé est dans la liste des arguments du component associé. Si c'est bien le cas, il envoye une requette TCPTalks pour obtenir cette valeur et la renvoie.

        :param attrname: Nom de l'atribut demandé.
        :param tcptimeout: Timeout pour la requette TCPTalks.
        :return: Retourne la valeur de l'attribu demandé.


    .. method:: __setattr__(attrname, attrvalue, tcptimeout=10)

        La methode de modification de variable. Cette methode regarde si la variable apellé est dans la liste des arguments du component associé. Si c'est bien le cas, il envoye une requette de modification de cette variable vias TCPTalks.

        :param attrname: Nom de l'attribut à modifier.
        :param attrvalue: Nouvelle valeur de l'attribue.
        :param tcptimeout: Timeout à utliser pour la requette TCPTalks.

Dans les objets qui hérite de proxy, on va pouvoir dans le contructeur modifier la liste des attributs et des methodes du component association, puis apeller le constructeur de proxy pour creer les methodes.

Le proxy de SerialTalks

.. class:: SerialTalksProxy(Proxy)

    .. method:: __init__(manager, uuid)

        Constructeur de SerialTalksProxy avec un uuid d'arduino.

        .. data:: attrname = ['port', 'is_connected']
            methlist = ['connect', 'disconnect', 'send', 'poll', 'flush', 'execute', 'getuuid', 'setuuid', 'getout', 'geterr']

        :param uuid: Code d'identification de l'arduino à utiliser pour ce proxy.


.. class:: SwitchProxy(Proxy)

    .. method:: __init__(manager, switchpin)

        Constructeur du proxy.

        .. data:: attrname = ['state', 'PinInput']
            methlist = ['Close']

        :param Manager manager: Object pour la comunication en TCPTalks.
        :param switchpin: Pin GPIO à utiliser pour l'interrupteur.

	.. method:: SetFunction(function, *args):

        Methode d'association de la methode à un compid pour la requette MAKE_MANAGER_EXECUTE.

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

        Methode d'association de la methode à un compid pour la requette MAKE_MANAGER_EXECUTE.

        :param Manager manager: Object pour la comunication en TCPTalks.
        :param function: Adresse de la fonction à utiliser.
        :param args: Arguments à utiliser pour la fonction.




.. class:: PiCameraProxy(Proxy)

    .. method:: __init__(manager, resolution, framerate)

        Constructeur du proxy de la picamera.

        .. data:: attrlist = ['resolution', 'framerate']
            methlist = ['start_capture', 'stop_capture']

        :param Manager manager: Object pour la comunication en TCPTalks.
        :param resolution: Resolution à parametrer à la caméra.
        :param framerate: Taux de Rafraichissement à utiliser pour la caméra.



