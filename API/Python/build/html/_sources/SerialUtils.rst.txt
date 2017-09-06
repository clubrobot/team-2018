############
Serial Utils
############

Serial Utils est une librairie de serialisation pour la communication entre l'ordinateur sous python et l'arduino sous CPP et ino.


*************
Préambule
*************

Cette librairie existe en deux versions (python , cpp). Ces deux versions different un peu dans le fonctionnement mais l'idée reste la même. Le but est de serialiser et de deserialiser. Ces opérations consistent à passer d'un object utilisable par un language (exemple int float double string) à une chaine d'octet ou l'inverse.
Pour une utilisation plus simple cette librairie est composé d'object avec une tache bien spécifique. 


**************
Python 
**************

Voici la version en python de cette librairie


Préambule
----------------


Pour le côté python, il existe des objects qui sont capables de faire la serialisation et la déserialisation en même temps mais pour un seul type de donnée. Malgrès le fais que ces objects existent, on prefèrera utiliser un object de déserialisation pur qui peux gérer des données avec plusieurs variables encodé en octet à l'interieur (ce qui n'est pas possible avec les objects de serialisation).
Pour commencer l'API nous allons traiter les objects de serialisation hybride puis l'object de déserialisation.

Toutes les classes de serialisation hybride hérite de AbstractType qui permet de les utiliser beaucoup plus facilement.


API
-----------------

.. class:: AbstractType

    .. method:: __call__(value)

        Cette methode permet à l'object d'être utilisé comme une methode et de retourner l'arguement (octets) en variable exploitable.

        :param octet value: Les octets à convertir en variable exploitables
        :return: Retourne la variable transcrit de l'octet à partir de value.


.. class:: IntegerType(AbstractType)

    Methode pour les variables sans virgules et les caractères simple (int , char , long).

    .. method:: __init__(length, byteorder, signed)

        Constructeur de l'object

        :param length: nombre d'octet du type à convertir, exemple 2 pour int.
        :param byteorder: Cette argument defini l'octet principal. Seul deux options possible ``big`` pour l'octet principal au debut et ``little`` pour l'octet principal à la fin.
        :param signed: Boolean pour savoir si la variable peut être négatif ou non.
        

    .. method:: to_bytes(integer)

        Methode pour convertir l'argument en octet.

        :param integer: argument à convertir en octet.
        :return: Retourne l'argument en octet.


    .. method:: from_bytes(rawbytes)

        Methode pour transformer des octets en variable exploitable dans le type prealablement paramétré.

        :param rawbytes: octets à convertir en variable utilisable.
        :return: Retourne la variable convertie de l'octet renseigné.





        .. note:: Pour l'arduino il faut prendre comme byteorder ``little``

.. class:: FloatType(AbstractType)

    Object de serialisation pour les variables float et double

    .. method:: __init__(standard)

        Constucteur du serialiser

        :param standard: Egal à ``f`` pour float et ``d`` pour double.


    .. method:: to_bytes(real)

        Methode pour convertir l'argument en octet.

        :param integer: argument à convertir en octet.
        :return: Retourne l'argument en octet.


    .. method:: from_bytes(rawbytes)


        Methode pour transformer des octets en variable exploitable dans le type prealablement paramétré.

        :param rawbytes: octets à convertir en variable utilisable.
        :return: Retourne la variable convertie de l'octet renseigné.


.. class:: StringType(AbstractType)

    Serialiser pour les chaines de caractère

    .. method:: __init__(encoding)

        Constructeur de l'oject.

        :param encoding: Encodage à utiliser pour transcrire les chaines de caractères en octets.

        .. note:: Pour une utilisation avec un arduino, il faut utiliser l'utf-8.


    .. method:: to_bytes(string)

        Methode de conversion des strings en octets.

        :param string: Chaine de caractères à convertir en octets.
        :return: Les octets defini à partir de la chaine de caractères en argument.



    .. method:: from_bytes(rawbytes)

        Methode de conversion d'octets en une chaine de caractères.

        :param rawbytes: Octets à convertir.
        :return: La chaine de caractères transcrit des octets en argument.



.. class:: Deserializer

    Object de déserialisation d'octets avec plusieurs variables dedans.

    .. method:: __init__(rawbytes)

        Constructeur de l'object de deserialisation.

        :param rawbytes: Octets à convertir en variables.

    
    .. method:: read(*types)

        Methode pour extraire les variables des octets fourni dans le constructeur.


        :param types: Arguments pour deserialiser les octets. 
        :return: La liste des variables extraite en tuple.

        .. warning:: Il faut obligatoirement utiliser des objets d'AbstractType, pour bien convertir.


Utilisation
------------
Voici quelques exemples d'utilisation de la libraire.

Pour la conversion en octet :

.. code::

    char_t   = IntegerType(1, 'little', True)
	byte_t   = IntegerType(1, 'little', False)
	int_t    = IntegerType(2, 'little', True)
	uint_t   = IntegerType(4, 'little', False)
	string_t = StringType('utf-8')
	float_t  = FloatType('f')

    rawbyte = byte_t  (10) + char_t  (ord('X')) + uint_t  (123456) + int_t   (-789) +  string_t('hello') + float_t (987.654)

Rawbyte est donc une liste d'octets contenants toutes ces variables.
Pour la reconversion : 

.. code:: 

    out = Deserializer(rawbyte)
    variables = out.read(byte_t,char_t,uint_t,int_t,string_t,float_t)


Voici un tableau récapitulant les objects de déserialisation utile pour l'arduino :

.. csv-table:: Tableau des serialisation pour utiliser Serialtalks
   :header: Variable, Object , Paramètres
   :widths: 50,50,50,50,50

    BYTE, IntegerType,1, 'little', False
    INT, IntegerType ,2, 'little', True
    LONG , IntegerType ,4, 'little', True
    FLOAT,FloatType,'f'
    STRING ,StringType,'utf-8'





**************
C++ API
**************



.. class:: Serializer

    `API <file:///W:/Francois/Mes%20documents/projet-robot/team-2018/API/CPP/html/struct_serializer.html#details>`_