############
Serial Utils
############

Serial Utils est une librairie de sérialisation pour la communication entre l'ordinateur sous python et l'Arduino sous CPP.


*************
Préambule
*************

Cette librairie existe en deux versions (python , cpp). Ces deux versions diffèrent un peu dans le fonctionnement mais l'idée reste la même. Le but est de sérialiser et de desérialiser. Ces opérations consistent à passer d'un objet utilisable par un langage (exemple int float double string) à une chaine d'octet ou l'inverse.
Pour une utilisation plus simple cette librairie est composée d'objet avec des taches bien spécifiques. 


Pour le côté python, il existe des objets qui sont capables de faire la sérialisation et la desérialisation en même temps mais pour un seul type de donnée. Malgré le fais que ces objets existent, on préfèrera utiliser un objet de déserialisation pur qui peux gérer des données avec plusieurs variables encodées en octets à l'intérieur (ce qui n'est pas possible avec les objets de sérialisation).
Pour commencer l'API nous allons traiter les objets de sérialisation hybride puis l'objet de desérialisation.

Toutes les classes de sérialisation hybride héritent de AbstractType qui permet de les utiliser beaucoup plus facilement.

*************
API
*************

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

    Sérialiser pour les chaines de caractères.

    .. method:: __init__(encoding)

        Constructeur de l'objet.

        :param encoding: Encodage à utiliser pour transcrire les chaines de caractères en octets.

        .. note:: Pour une utilisation avec un Arduino, il faut utiliser l'utf-8.


    .. method:: to_bytes(string)

        Converti des chaines de caractères en octets.

        :param string: Chaine de caractères à convertir.
        :return: Les octets générés.



    .. method:: from_bytes(rawbytes)

        Converti les octets en une chaine de caractères.

        :param rawbytes: Octets à convertir.
        :return: La chaine de caractères transcrit.



.. class:: Deserializer

    Objet de désérialisation d'octets pour générer plusieurs variables.

    .. method:: __init__(rawbytes)

        Constructeur de l'objet de désérialisation.

        :param rawbytes: Octets à convertir.

    
    .. method:: read(*types)

        Extrait les variables des octets fourni dans le constructeur.


        :param types: Objets AbstractType pour décoder les variables dans les types souhaités. 
        :return: La liste des variables extraites en tuple.

        .. warning:: Il faut obligatoirement utiliser des objets d'AbstractType, pour bien convertir dans les bons formats.

*************
Utilisation
*************
Voici quelques exemples d'utilisation de la librairie.

Pour la conversion en octet:

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


Voici un tableau récapitulant les objets de désérialisation utiles pour l'Arduino :

.. csv-table:: Tableau des sérialisations pour utiliser Serialtalks
   :header: Variable, Object , Paramètres
   :widths: 50,50,50,50,50

    BYTE, IntegerType,1, 'little', False
    INT, IntegerType ,2, 'little', True
    LONG , IntegerType ,4, 'little', True
    FLOAT,FloatType,'f'
    STRING ,StringType,'utf-8'




