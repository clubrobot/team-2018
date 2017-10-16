####################
PeriodicProcess
####################


PeriodicProcess est une librairie pour mieux gérer les resources et les taches parallèles. En effet les fichiers .ino ne peuvent pas faire de threading. Il est parfois necessaire de faire des taches parallèle sous les Arduinos.
L'astuce est de faire les taches l'une après l'autre en paramètrant un temps entre chaque appel. Il est donc possible de privilégié une tache plutot qu'une autre en réduisant le temps d'actualisation.
Le temps d'actualisation correspont au temps minimum entre chaque appel. J'ai dit que le but de PeriodicProcess est d'appeler les process un par un mais si un des process à un temps d'actualisation trop long, il se peut qu'il saute son tour.

PeriodicProcess prend la forme d'une classe à implémenter. Cette classe va possédé quelques méthodes à implémenter. 
Les méthodes sont : 

1. **onProcessEnabling()** :
    Cette méthode est appelée à l'activation du PeriodicProcess. Elle vous permet de faire des instructions lors de l'activation.

2. **process()** :
    Cette méthode est celle qui sera appelée en boucle pour simuler le threading. Cette méthode doit donc être implémentée avec précaution pour ne pas réduire les performances des autres PeriodicProcess.

3. **onProcessDisabling()** :
    Cette méthode est appelée à la désactivation du PeriodicProcess. Elle vous permet de faire des instructions lors de la désactivation.


---------------------------------------
`API <http://www.u-bordeaux1.fr/>`_
---------------------------------------

----------------------
Utilisation
----------------------