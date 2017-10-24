#########################
WheeledBase
######################### 

WheeledBase est l'arduino avec les programmes les plus lourds à ce jour. Car à lui seul l'Arduino doit gérer l'Odométrie, l'asservissement et les trajectoires.
Pour permettre de mieux gérer toutes ces taches le code est divisée en de nombreuses classes pour permettre de futur customisations.


*************************
Préambule
*************************
Cette page sera séparée en plusieurs sous parties correspondants à des groupes de classes ayant des fonctions similaires. Nous allons dans un premier temps retrouver l'Odométrie.
Cette partie est réalisée deux types d'objets, les roues codeuses et la classe mère pour effectuer les calcules. La partie suivante consiste à controler les moteurs en y appliquant de l'asservissement. Cette partie est réalisé par plusieurs classe.
Les premières classes sont celles des moteurs DC. Puis on a une classe VelocityController qui permet d'appliquer un asservissement au moteur à partir de commande. Cette commande veux venir soit de l'algorythme de trajectoire soit de l'utilisateur directement.
Viens ensuite le PositionController qui sert de support pour les classes de trajectoires. Les classes de trajectoire ont comme objectif de donner des ordres de vitesses en temps réel au moteur pour suivre une trajectoire donné par l'utilisateur.
Suivant la demande de l'utilisateur certain étage d'asservissement peuvent être désactivé. Par exemple si l'utilisateur demande une vitesse l'étage d'asservissement en position sera désactivé. L'utilisateur peux également tous désactivé et demandé l'envoie directement d'une tension au moteur.




*************************
Odométrie
*************************
L'odométrie est une phase importante de calcul de la WheeledBase. Puisque les données récoltées sont indispenssable pour l'asservissement et la gestion de trajectoire. Pour mener à bien cette tache, l'odometrie dispose de deux grandes classe.
Il y a la classe mère qui permet de réalisé les calculs et les classes des roues codeuses. Ces dernières permets à partir du nombres de tics des roues codeuses de pouvoir en déduire une distance parcouru qu'il transmettra à la classe mère.
Une fois que la classe mère Odometry a les distances parcouru elle peut à partir de l'entraxe, calculer la distance linéaire et angulaire parcourut pour en déduire la nouvelle position.
Avec cette nouvelle position, l'odometrie peut en déduire une vitesse casi instantané. Une fois la position et la vitesse calculés, elle le transmet respectivement à PositionController et VelocityController.


*************************
Vitesse
*************************
La parti vitesse est une phase importante pour correctement ce déplacer sur le terrain. Elle va avoir plusieur tache; la première est de garantir des accélérations limites puis de suivre correctement les consignes grâce à un asservissement. Ces étapes de calcules sont séparé en plusieurs parties.
La première est de récupéré la vitesse actuel de robot donnée par l'odométrie. Ensuite, l'objet VelocityController détermine à partir de la consigne, de la vitesse demandé et de la consigne donnée à l'asservissement pour déterminé une nouvelle vitesse à suivre.
Cette consigne répondra le plus rapidement à la consigne en respectant la limite de d'accélération. Une fois la consigne d'asservissement généré, on passe à l'asservissement à proprement parlé (avec un objet ``PID``). Cette étape va utilisé la vitesse actuel et la vitesse demandé pour en déduire une erreur.
Cette erreur est nécessaire pour générer une nouvelle consigne au moteur (objet ``DCMotor``).

*************************
Position
*************************

TODO


*************************
API Python
*************************

.. class:: WheeledBase

    .. method:: __init__(parent, uuid='wheeledbase')

        Constructeur de WheeledBase.
        :param Manager parent: Objet Manager connecté au serveur du robot.
        :param uuid: Identifiant de l'Arduino à utiliser comme WheeledBase.
    
    .. method:: set_openloop_velocities(left, right)

        Impose une vitesse non asservie directement au moteur.

        :param left: Vitesse pour la roue gauche.
        :param right: Vitesse pour la roue droite.

    .. method:: get_codewheels_counter(**kwargs)

        Affiche le nombre de tics des roues codeuses depuis le dernier démarage de l'Arduino (sous forme d'un tuple).

    .. method:: set_velocities(linear_velocity, angular_velocity)

        Paramètre une vitesse asservie au moteur.

        :param linear_velocity: Vitesse linéaire en mm/s.
        :param angular_velocity: Vitesse angulaire en rad/s.


    .. method:: purepursuit(waypoints, direction='forward', finalangle=None, lookahead=None, lookaheadbis=None, linvelmax=None, angvelmax=None)

        Méthode de trajectoire courbe. Elle permets d'ajouter des points de passage, une direction pour le robot et des paramètres de fin de suivit de trajectoire.

        :param tuple waypoints: Liste des points de passage sous forme de tableau ou tuple.
        :param direction: 'forward' ou 'backward' , désigne dans quel sens doit se déplacer le robot.
        :param finalangle: Angle à visé à la fin de la trajectoire.
        :param lookahead: Distance en mm pour générer le point objectif.
        :param lookaheadbis: Distance en mm pour générer le point objectif en fin de trajectoire.
        :param linvelmax: Vitesse maximal pendant le déplacement.
        :param angvelmax: Vitesse angulaire maximal pendant le déplacement. 
        :raise RuntimeError: Sécurité patinage ``spin urgency``.
        :raise ValueError: Il n'y a pas assez de points.

    .. method:: turnonthespot(theta)

        Méthode de rotation asservie en position.
        :param theta: angle à atteindre.

    .. method:: isarrived(**kwargs)

        Verifie si la position désiré avec turnonthespot ou purepursuit est atteinte.

        :return: Vrai si la position est atteinte faux sinon.

    .. method:: wait(timestep=0.1, **kwargs)

        Bloque le programme tant que le robot n'a pas atteint sa position cible.
        :param timestep: Temps d'actualisation de la requette isarrived().


    .. method:: goto( x, y, theta=None, direction=None, **kwargs)

        Donne une nouvelle position à atteindre. Goto va simplement exécuté un purepursuit entre la position du robot et la position demandé.
        :param theta: Angle à atteindre à la position demandée.
        :param direction: 'forward' ou 'backward' indique le sens que dois prendre le robot pour ce déplacer.


    .. method:: stop()

        Arrête le robot.

    .. method:: set_position(x, y, theta)

        Modifie la position actuel de l'odométrie.

    .. method:: reset()

        Initialise l'odométrie du robot.

    .. method:: get_position(**kwargs)

        Retourne la position du robot sous un tuple (x,y,theta).

        :return: Position en mm et rad.

    .. method:: get_velocities(**kwargs)

        Retourne la vitesse.
        :return: Vitesses linéaire et angulaire en mm/s et rad.

    .. method:: set_parameter_value(id, value, valuetype)

        Charge un nouveau paramètre à la wheeledbase (retrouver la liste en bas de page).

        :param id: Numéro d'indentification du paramètre à mettre à jour.
        :param value: Nouvelle valeur du paramètre.
        :param valuetype: Type de cette nouvelle variable.

    .. method:: get_parameter_value(id, valuetype)

        Donne la valeur du paramètre demandé.
        
        :param id:  Numéro d'indentification du paramètre à obtenir.
        :param valuetype: Type de la valeur à obtenir.
        :return: La valeur du paramètre demandé.


==================================  ======  =========  ===========================================================
Nom Parametre                        ID      Type                 Desciption
==================================  ======  =========  ===========================================================
LEFTWHEEL_RADIUS_ID                 0x10     FLOAT     Rayon de la roue motrice gauche.
LEFTWHEEL_CONSTANT_ID               0x11     FLOAT     Constante d'asservissement du moteur gauche.
LEFTWHEEL_MAXPWM_ID                 0x12     FLOAT     PWM maximal pour le moteur gauche.
RIGHTWHEEL_RADIUS_ID                0x20     FLOAT     Rayon de la roue motrice droite.
RIGHTWHEEL_CONSTANT_ID              0x21     FLOAT     Constante d'asservissement du moteur droit.
RIGHTWHEEL_MAXPWM_ID                0x22     FLOAT     PWM maximal pour le moteur droit.
LEFTCODEWHEEL_RADIUS_ID	            0x40     FLOAT     Rayon de la roue codeuse gauche.
LEFTCODEWHEEL_COUNTSPERREV_ID       0x41     **LONG**  Nombre de tics par révolution de la roue gauche.
RIGHTCODEWHEEL_RADIUS_ID            0x50     FLOAT     Rayon de la roue codeuse droit.
RIGHTCODEWHEEL_COUNTSPERREV_ID      0x51     **LONG**  Nombre de tics par révolution de la roue droit.
ODOMETRY_AXLETRACK_ID               0x60     FLOAT     Entraxe entre les roues codeuses.
ODOMETRY_SLIPPAGE_ID                0x61     FLOAT     Coefficient linéaire de décalage latéral.
VELOCITYCONTROL_AXLETRACK_ID        0x80     FLOAT     Entraxe entre les roues motrices.
VELOCITYCONTROL_MAXLINACC_ID        0x81     FLOAT     Accélération linéaire max.
VELOCITYCONTROL_MAXLINDEC_ID        0x82     FLOAT     Déceleration linéaire max.
VELOCITYCONTROL_MAXANGACC_ID        0x83     FLOAT     Accélération angulaire max.
VELOCITYCONTROL_MAXANGDEC_ID        0x84     FLOAT     Déceleration angulaire max.
VELOCITYCONTROL_SPINSHUTDOWN_ID     0x85     **BYTE**  Activation de la sécurité anti-patinage.
LINVELPID_KP_ID                     0xA0     FLOAT     Coefficient proportionnel d'asservissement lin.
LINVELPID_KI_ID                     0xA1     FLOAT     Coefficient intégrateur d'asservissement lin.
LINVELPID_KD_ID                     0xA2     FLOAT     Coefficient dérivateur d'asservissement lin.
LINVELPID_MINOUTPUT_ID              0xA3     FLOAT     Vitesse maximal linéaire min en sorti d'aserv.
LINVELPID_MAXOUTPUT_ID              0xA4     FLOAT     Vitesse maximal linéaire max en sorti d'aserv.
ANGVELPID_KP_ID                     0xB0     FLOAT     Coefficient proportionnel d'asservissement angulaire.
ANGVELPID_KI_ID                     0xB1     FLOAT     Coefficient intégrateur d'asservissement angulaire.
ANGVELPID_KD_ID                     0xB2     FLOAT     Coefficient dérivateur d'asservissement angulaire.
ANGVELPID_MINOUTPUT_ID	            0xB3     FLOAT     Vitesse maximal angulaire min en sorti d'aserv.
ANGVELPID_MAXOUTPUT_ID	            0xB4     FLOAT     Vitesse maximal angulaire max en sorti d'aserv.
POSITIONCONTROL_LINVELKP_ID         0xD0     FLOAT     Coefficient proportionnel lin de gestion de trajectoire.
POSITIONCONTROL_ANGVELKP_ID         0xD1     FLOAT     Coefficient proportionnel ang de gestion de trajectoire.
POSITIONCONTROL_LINVELMAX_ID        0xD2     FLOAT     Vitesse maximal linéaire pour la gestion de trajectoire.
POSITIONCONTROL_ANGVELMAX_ID        0xD3     FLOAT     Vitesse maximal angulaire pour la gestion de traj.
POSITIONCONTROL_LINPOSTHRESHOLD_ID  0xD4     FLOAT     Erreur cart. acceptée pour la gestion de trajectoire.
POSITIONCONTROL_ANGPOSTHRESHOLD_ID  0xD5     FLOAT     Erreur ang. acceptée pour la gestion de trajectoire.
PUREPURSUIT_LOOKAHEAD_ID            0xE0     FLOAT     Distance du point objectif pour purpursuit.
PUREPURSUIT_LOOKAHEADBIS_ID         0xE2     FLOAT     Distance du point objectif de l'arrivée pour purpursuit.
==================================  ======  =========  ===========================================================
 

