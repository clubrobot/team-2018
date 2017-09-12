############
Outils
############

Cette rubrique regroupe tous les outils annexes qui peuvent avoir une utilisation dans l'élaboration d'une IA, ou d'automate.



***********
GeoGebra
***********

Preambule
--------------

La librairie GeoGebra permet de pouvoir extraire des points, angles, et lignes brisés. Cette librairie extrait les données des fichiers GGB qui ne sont que des fichiers XML compressés.
Voici un exemple de XML de geogebra avec comme exemple un point apellé ``bornibus``.

.. code:: 

    <element type="point" label="bornibus">
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255" alpha="0.0"/>
    <layer val="0"/>
	<labelMode val="0"/>
	<animation step="1" speed="1" type="1" playing="false"/>
	<isShape val="false"/>
	<coords x="-0.72" y="4.14" z="1.0"/>
	<pointSize val="4"/>
	<pointStyle val="0"/>
 
Cette petites fonctiobs utilisent les librairies ``zipfile`` et ``xml.etree.ElementTree``.

API
-------------


.. function:: loadggb(filename)

    Fonction pour convertir le fichier .ggb en object ELEMENT de la librairie ``xml.etree.ElementTree``.

    :param filename: Chemin du fichier ou nom du fichier.

.. function:: getpos(root, label)

    Retourn la position du point de nom label (en tuple).

    :param Element root: object XML obtenu avec le loadggb.
    :param label: Nom du point à retourner.


.. function:: getangle(root, label)

    Retourne la valeur de l'angle avec le nom Label.

    :param Element root: object XML obtenu avec le loadggb.
    :param label: Nom de l'angle à retourner.


.. function:: getpath(root,label)

    Retourne une liste des points de la ligne brisé se nommant label.

    :param Element root: object XML obtenu avec le loadggb.
    :param label: Nom de la ligne brisé à retourner.



Utilisation
------------

La librairie étant très simple ce chapitre ce limitera à un exemple d'utilisation avec une ligne brisé généralement utilisé pour les paths.


Voici un exmple de géogebra contenant une ligne brisé. Celle-ci prend le nom de ``main``.

.. image:: example1_geogebra.png



Une fois le fichier sauvegardé (``example.ggb``), vous pouvez lancer votre python pour exploiter le fichier. Il faut d'abord ouvrir le fichier pour l'exploiter.

.. code:: 

    file = loadggb('example.ggb')

A partir d'içi il est tres facile extraire les données comme ci-dessous : 

.. code::

    print(getpath(file,'main'))
    #[(-2.0, 3.0), (1.56, 5.161818181818181), (3.4509090909090903, 2.9254545454545458), (0.8145454545454542, -0.9836363636363615), (-2.0, -1.0)]


Il faut noté que pour les indices il faut l'ecrire dans les methodes comme cela : ``nom_{indice}``





***********************
RoadMap 
***********************


Cette librairie permet une utilisation simplifié d'Igraph qui est une librairie de python permetant de creer des graphs. Grace aux outils de cette librairie vous pourez faire du path finding dans un graph creer avec geogebra.


Préambule
------------

Cette librairie utilise les methodes de ``geogebra``, voir au dessus. Cette resource est composée d'une fonction d'intersectinon est  d'un object roadmap. 



API
------------------

.. function:: intersect(A, B)

    Retourne un boolean si les deux segments donnés en argument se coupent.  

    :param tuple A: Coordonnées du premier segment avec la forme suivante : (xA1, yA1), (xA2, yA2)
    :param tuple B: Coordonnées du deuxième segment avec la forme suivante : (xB1, yB1), (xB2, yB2)
    :return: Un boolean si il y a croisement ou pas.

.. class:: RoadMap



    .. method:: __init__(vertices=list(), edges=set())

        Constructeur de l'object RoadMap, elle a pour but de charger le graph.

        :param list vertices: Liste des sommets du graph.
        :param set edges: Set des segments du graph.


    .. method:: reset_edges()

        Calcule le poid des segments, c'est à dire leur longueur.

    .. method:: cut_edges(cutline)

        Retire les segments du graph qui coupe la cutline.

        :param cutline: Ligne permetant là découpe des segments du graph. Elle dois être de cette forme : ``(xCutLine, yCutLine), (xCutLine2, yCutLine2)``

    .. method:: get_vertex_distance(vid, vertex)

        Calcule la distance entre deux sommets du graph.

        :param vid: Numéro du sommet , c'est à dire le rang de celle-ci dans la liste donné au constructeur.
        :param vertex: Coordonnées du deuxième sommet. Dois être de cette forme ``x1, y1``
        :return: la distance entre les deux sommets.


    .. method:: get_closest_vertex(vertex)

        Trouve le sommet le plus près du point vertex.

        :param vertex: point à partir du quel, on cherche le plus près sommet.
        :return: L'index du sommet du graph trouvé comme le plus proche de vertex.

    .. method:: add_vertex(vertex)

        Ajoute un sommet au graph.

        :param vertex: Point à ajouter comme sommet au graph.
        :return: L'index du sommet créé.


    .. method:: get_shortest_path(source, target)

        Effectue un path finding à l'aide du graph.

        :param source: Point d'origine du path finding.
        :param target: Point d'arrivé du path finding.
        :return: Le tableau avec chaque point du pathfinding.


    @staticmethod

    .. function:: load(geogebra, pattern='roadmap_{\s*\d+\s*,\s*\d+\s*}')

        Cree un object Roadmap à partir d'un fichier geogebra.

        :param geogebra: Nom du fichier ou object GeoGebra.
        :param pattern: structure du nom du graph sous GeoGebra.
        :return: L'object Roadmap généré.








