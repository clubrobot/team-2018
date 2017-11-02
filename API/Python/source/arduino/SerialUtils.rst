################
SerialUtils
################


Serial Utils est une librairie de sérialisation pour la communication entre l'ordinateur sous python et l'Arduino sous CPP.


*************
Préambule
*************

Cette librairie existe en deux versions (python , cpp). Ces deux versions diffèrent un peu dans le fonctionnement mais l'idée reste la même. Le but est de sérialiser et de desérialiser. Ces opérations consistent à passer d'un objet utilisable par un langage (exemple int float double string) à une chaine d'octet ou l'inverse.
Pour une utilisation plus simple cette librairie est composée d'objet avec des taches bien spécifiques. 

Pour la partie C++ dédiée au Arduinos, la librairie est composée de deux ``struct``. Les deux struct correspondent aux opérations de sérialisation (``Serializer``) et de désérialisation (``Deserializer``). Bien que leurs missions différents leur fonctionnement reste le même.
Chaque ``struct`` disposent d'un buffer interne, ce buffer n'est rien de plus qu'un simple tableau de d'octets (dont la taille max correspond à une constante de SerialTalks). Dans le cas du sérialiseur, le buffer est à l'origine vide et à partir de méthode, l'utilisateur va pourvoir le remplir.
Dans le sens inverse, le desérialiseur a à l'origine, un buffer déjà rempli qu'il va décoder avec les types de variables demandés par l'utilisateur. Pour utiliser cette librairie, il est important de toujour spécifier les types utilisés, pour permettre une bonne sérialisation.
Ce renseignement sera toujours passé au struct par des templates (chevrons devant le nom de la fonction).

**************
API
**************

***************
Utilisation
***************
Pour mieux illustrer l'utilité des sérialiseurs, nous allons pour cette exemple se placer dans un contexte d'instruction pour du SerialTalks.

Pour commencer voici un instruction vierge avec la signature classique pour pouvoir être associée à une requête SerialTalks.

.. code:: 

    void exemple(Serialtalks& inst,Deserializer&  input, Serializer& output){

    }

Dans n'importe quelle instruction, vous aurrez besoin de faire passer ou de récupérer des informations depuis le serial. Pour ce faire SerialTalks va vous donner les serialiseurs à remplir et les desérialiseur à vider.
Les serialiseurs seront ensuite transmit à la RaspBerry tandis que les desérialiseurs ont déjà dans leur buffer les informations données par la Raspberry.

Pour commencer, il faut récupérer les informations du Deserializer. Pour ce faire on utilisera la méthode read avec dans les chevrons le type souhaité. Voici un exemple :

.. code::

    bool activation;
    activation = input.read<bool>();

    float distance;
    distance = input.read<float>();

.. note:: Tous les octets lu ne sont ensuite plus accessible.

Pour finir voici comment il est possible de remplir le buffer du serialiseur.

.. code::

    int longueur(4);
    output.write<int>(longueur);
    