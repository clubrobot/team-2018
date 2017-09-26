############
SerialTalks
############

a librairie SerialTalks assure la communication entre ordinateur et arduino.
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
    Le RET code est utile pour les réponses d'instructions. En effet si l'arduino a besoin de renvoyer des informations au programme python. il va utiliser ce code dans le packet retour pour permettre au programme python de bien associer avec quel requête ces informations sont reliés.
5. **args et kwargs**:
    Une requête peux avoir une infinité d'arguments supplémentaire du moment que la taille du packet est réglementaire. Il faut savoir que l'arduino tout comme les méthodes en python ne peuvent pas d'eux même reconnaître la nature des arguments et leurs nombres. Ces information devront être renseignées au préalable.


Les requêtes sont toujours à l'initiative de la parti python. L’Arduino ne peut pas déclencher la moindre fonction python contrairement à son homologue.
Quand une requêtes depuis l'ordinateur est envoyé à l’Arduino, il y a deux cas de figure : 

 * Si notre requête ne requière aucun retour, dans ce cas le packet va déclenché une fonction dans l’Arduino.
 * Si notre requête requière un retour, l’Arduino après avoir exécuté la fonction associé à l'OP code reçu va renvoyer ça réponse grâce au code esclave et le Retcode qui a été envoyé dans le packet reçu.




Introduction
-------------------------


Cette partie correspond à la bibliothèque Cpp destinée aux Arduinos.

Avant de commencer la documentation, quelques explications sont nécessaires pour mieux comprendre l'architecture de la librairie. Dans un premier temps, la librairie a besoin de sérialiser et de désérialiser, ces objets sont explicités dans la page SerialUtils.
Les autres points importants de cette librairie sont les types de variables, il en existe un certain nombres et il vaut mieux être claire sur les rôles de chacun.

Dans la librairie nous allons trouver des ``byte``. Ce sont de simple ``unsigned char`` qui représente parfaitement le byte puisque les ``unsigned char`` prennent leur valeur entre 0 et 255.
Nous avons ensuite des ``buffer``, ce sont de simple liste de ``byte``. Ils sont utiliser pour l'envoi et la recèption de données.

Un autre type utilisé est le ``Stream``. Ce type est importé de ``<Arduino.h>``. Il représente un flux de communication, dans notre cas il permet l'utilisation du Serial, vous trouverez plus de renseignements `ici <https://www.arduino.cc/en/Reference/Stream>`_. 

Le type ``*Instruction`` correspond à un pointeur de fonction dont la signature est la suivante ```(SerialTalks& inst, Deserializer& input, Serializer& output)```. On peux voir que ces fonctions vont correspondre à des requêtes ( reliée à un OPcode).

Le dernier type utilisé est le ostream. C'est une classe de SeriaTalks qui a pour but de créer un autre canal virtuel de communication avec le serial. Ces canaux sont utilisés pour les erreurs et les sorties de l'Arduino. On dit que le canal est virtuel, car il utilise en réalité le même canal que les autres informations, mais avec un retcode bien spécifique.


*******************
API
*******************

Nous commencerons cette API par la classe d'Ostream avant de passer à SeriaTalks.

`API OSTREAM <file:///W:/Francois/Mes%20documents/projet-robot/team-2018/API/CPP/html/classostream.html>`_

Voici l'API de SerialTalks :

API SERIALTALKS

*******************************
Note et utilisation
*******************************
