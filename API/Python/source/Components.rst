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
Dans ce chapitre nous metterons a disposition l'API ainsi que quelques conseil et explication pour la creation de nouveaux components.


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




**************
Manager
**************



*************
Utilisation
*************