##################
    GPIO
##################

Cette partie va traiter tous les objects evoluant sur le GPIO de la raspberry


Préambule
---------------------



Cette libraire utilise la libraire RPi et la configuration des GPIOs en mode BOARD

Numero des pins en mode BOARD.


.. image:: tab_GPIO.png



Tous les objets utilisants du GPIO doivent hériter de l'object ``Device`` Qui permet la gestion des pins pour éviter à deux objects d'utiliser les mêmes pins.


API
---------------------------------------- 

Pour commencer voici la classe Device permettant la gestion des pins

.. class:: Device

    .. data:: list_pin = [0] * 59

    0 = Libre
    1 = Occupé


Viens ensuite les objects fonctionnant sur le GPIO.
Le premier conserne l'interrupteur, celui-ci dois être brancher sur la masse et sur un pin du GPIO à renseigner.

.. class:: Switch(Device)

    .. method:: __init__(self,pininput,function=None,*args)

        Constructeur de l'object interrupteur. Elle peut également avec les deux derniers paramètre parametrer une methode à apeller à chaque changement d'etat.

        :param pininput: Pin à utiliser pour l'interrupteur. 
        :param function: Fonction à apeller à chaque changement d'etat.
        :param args: Arguments à transmettre à la fonction.
        :exception RuntimeError: Dans le cas de l'utilisation d'un pin déjà utilisé.




    .. method:: SetFunction(function,*args)

        Methode pour bind une fonction à chaque changement d'état de l'interrupteur. Pour ne plus avoir de methode d'enregistrée utilisé ``None``.

        :param function: Fonction à associer.
        :param args: Arguments à transmettre à la fonction lors de son apelle.


    .. method:: LaunchFunction(args)

        Methode interne d'apelle de la fonction enregistrée.

        :param args: Arguments annexes.

Le deuxieme object est un bouton poussoir luminessante. Pour les connectiques du bouton, il faut brancher une pin à la masse du GPIO et un pin à une entrée du GPIO.


.. class:: LightButton(Device)

    .. method:: __init__(self,pininput,pinLight,function=None,*args)

        Constructeur de l'interrupteur, qui peut également associer une fonction au bouton.

        :param pininput: Pin à utiliser pour le bouton.
        :param pinLight: Pin à utiliser pour la lumière du bouton.


    .. method:: SetAutoSwitch(value)

        Activation de l'autoswitch de la lumière du bouton. C'est a dire qu'à chaque changement d'état du bouton, la lumière change également d'état.
        :param boolean value: Vrai ou Faux pour l'activation de l'AutoSwitch.

    .. method:: On()

        Allumer le bouton.

    .. method:: Off()

        Etteindre le bouton.


    .. method:: Switch()

        Changer l'état de la lumière du bouton.

    .. method:: SetFunction(function,*args)

        Methode d'affectation de la fonction pour le bouton. 

        :param function: Fonction à apeller à chaque changement d'état du bouton.
        :param args: Arguments à passer à la fonction lors de l'apelle.

    .. method:: Close()

        Couper le bouton et libéré les pins pour une autre utilisation.

        

    .. method:: LaunchFunction(args)

        Methode interne d'apelle de la fonction parametrée.