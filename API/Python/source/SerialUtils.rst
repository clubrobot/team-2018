############
Serial Utils
############

Serial Utils est une librairie de sérialisation pour la communication entre l'ordinateur sous python et l'Arduino sous CPP.


*************
Préambule
*************

Cette librairie existe en deux versions (python , cpp). Ces deux versions diffèrent un peu dans le fonctionnement mais l'idée reste la même. Le but est de sérialiser et de desérialiser. Ces opérations consistent à passer d'un objet utilisable par un langage (exemple int float double string) à une chaine d'octet ou l'inverse.
Pour une utilisation plus simple cette librairie est composée d'objet avec une tache bien spécifique. 


**************
Python 
**************

Voici la version en python de cette librairie.


Préambule
----------------


Pour le côté python, il existe des objets qui sont capables de faire la sérialisation et la desérialisation en même temps mais pour un seul type de donnée. Malgré le fais que ces objets existent, on préfèrera utiliser un objet de déserialisation pur qui peux gérer des données avec plusieurs variables encodées en octets à l'intérieur (ce qui n'est pas possible avec les objets de sérialisation).
Pour commencer l'API nous allons traiter les objets de sérialisation hybride puis l'objet de desérialisation.

Toutes les classes de sérialisation hybride héritent de AbstractType qui permet de les utiliser beaucoup plus facilement.


API
-----------------

.. class:: AbstractType

    .. method:: __call__(value)

        Cette méthode permet à l'objet d'être utilisé comme une méthode et de retourner l'argument (octets) en variable exploitable.

        :param octet value: Octets à convertir en variable.
        :return: Variable transcrit de l'octet à partir de value.


.. class:: IntegerType(AbstractType)

    Classe pour les variables sans virgules et les caractères simple (int , char , long).

    .. method:: __init__(length, byteorder, signed)

        Constructeur de l'objet.

        :param length: Nombre d'octet du type à convertir, exemple 2 pour int.
        :param byteorder: Défini l'octet principal. Seul deux options possible ``big`` pour l'octet principal au début et ``little`` pour l'octet principal à la fin.
        :param signed: Boolean pour savoir si la variable peut être négatif ou non.
        

    .. method:: to_bytes(integer)

        Converti l'argument en octet.

        :param integer: Argument à convertir en octet.
        :return: Argument en octet.


    .. method:: from_bytes(rawbytes)

        Transforme des octets en  une variable exploitable dans le type prealablement paramétré.

        :param rawbytes: Octets à convertir.
        :return: Variable convertie.



        .. note:: Pour l'Arduino il faut prendre comme byteorder ``little``.

.. class:: FloatType(AbstractType)

    Objet de sérialisation pour les variables float et double.

    .. method:: __init__(standard)

        Constucteur du sérialiser.

        :param standard: Egal à ``f`` pour float et ``d`` pour double.


    .. method:: to_bytes(real)

        Convertis l'argument en octet.

        :param integer: Argument à convertir.
        :return: Argument en octet.


    .. method:: from_bytes(rawbytes)


        Transforme des octets en variable exploitable dans le type prealablement paramétré.

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