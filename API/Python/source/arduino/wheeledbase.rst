#########################
WheeledBase
######################### 

WheeledBase est l'arduino avec les programmes les plus lourds à ce jour. Car à lui seul l'arduino doit gérer l'Odométrie, l'asservissement et les trajectoires.
Pour permettre de mieux gérer toutes ces taches le code est divisée en de nombreuses classes pour permettre de futur customisations.


*************************
Préambule
*************************
Cette page sera séparer en plusieur sous parties correspondants à des groupes de classe ayant des fonctions similaires. Nous allons dans un premier temps retrouver l'Odométrie.
Cette partie est réalisé deux types d'objets, les roues codeuses et la classe mère pour effectuer les calcules. La partie suivante consiste à controler les moteurs en y appliquant de l'asservissement. Cette partie est réalisé par plusieurs classe.
Les premières classes sont celles des moteurs DC. Puis on a une classe VelocityController qui permet d'appliquer un asservissement au moteur à partir de commande. Cette commande veux venir soit de l'algorythme de trajectoire soit de l'utilisateur directement.
Viens ensuite le PositionController qui sert de support pour les classes de trajectoires. Les classes de trajectoire ont comme objectif de donner des ordres de vitesses en temps réel au moteur pour suivre une trajectoire donné par l'utilisateur.
Suivant la demande de l'utilisateur certain étage d'asservissement peuvent être désactivé. Par exemple si l'utilisateur demande une vitesse l'étage d'asservissement en position sera désactivé. L'utilisateur peux également tous désactivé et demandé l'envoie directement d'une tension au moteur.




*************************
Odométrie
*************************
L'odométrie est une phase importante de calcul de la WheeledBase. Puisque les données récoltés sont indispenssable pour l'asservissement et la gestion de trajectoire. Pour mener à bien cette tache, l'odometrie dispose de deux grandes classe.
Il y a la classe mère qui permet de réalisé les calculs et les classes de 



*************************
Vitesse
*************************


*************************
Position
*************************




*************************
API Python
*************************