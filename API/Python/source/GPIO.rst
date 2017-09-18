##################
    GPIO
##################

Cette partie va traiter tous les objets évoluant sur le GPIO de la Raspberry.


Préambule
---------------------



Cette libraire utilise la libraire RPi et la configuration des GPIOs en mode BOARD.

Numero des pins en mode BOARD.


.. image:: tab_GPIO.png



Tous les objets utilisant  du GPIO doivent hériter de l'objet ``Device``. Cet objet permet la bien gérer l'allocation des pins afin d'éviter à deux objets d'utiliser les mêmes pins.


API
---------------------------------------- 

Pour commencer voici la classe Device permettant la gestion des pins.

.. class:: Device

    .. data:: list_pin = [0] * 59

    0 = Libre
    1 = Occupé


Viens ensuite les objets fonctionnant sur le GPIO.
Le premier concerne l'interrupteur, celui-ci dois être branché sur la masse et sur un pin du GPIO à renseigner dans le constructeur.

.. class:: Switch(Device)

    .. method:: __init__(self,pininput,function=None,*args)

        Constructeur de l'objet interrupteur. Elle peut également avec les deux derniers paramètres, paramétrer une méthode à appeler à chaque changement d'état.

        :param pininput: Pin à utiliser pour l'interrupteur. 
        :param function: Fonction à appeler  à chaque changement d'état.
        :param args: Arguments à transmettre à la fonction.
        :exception RuntimeError: Dans le cas de l'utilisation d'un pin déjà utilisé.




    .. method:: SetFunction(function,*args)

        Méthode pour bind une fonction à chaque changement d'état de l'interrupteur. Pour ne plus avoir de méthode d'enregistrée utilisé ``None``.

        :param function: Fonction à associer.
        :param args: Arguments à transmettre à la fonction lors de son appelle.


    .. method:: LaunchFunction(args)

        Méthode interne d'appel de la fonction enregistrée.

        :param args: Arguments annexes.

Le deuxième objet est un bouton poussoir luminescent. Pour les connectiques du bouton, il faut brancher un pin à la masse du GPIO et un pin à une entrée du GPIO.


.. class:: LightButton(Device)

    .. method:: __init__(self,pininput,pinLight,function=None,*args)

        Constructeur de l'interrupteur, qui peut également associer une fonction au bouton.

        :param pininput: Pin à utiliser pour le bouton.
        :param pinLight: Pin à utiliser pour la lumière du bouton.


    .. method:: SetAutoSwitch(value)

        Activation de l'AutoSwitch de la lumière du bouton. C'est à dire qu'à chaque pression sur le bouton, la lumière change d'état.

        :param boolean value: Vrai ou Faux pour l'activation de l'AutoSwitch.

    .. method:: On()

        Allume le bouton.

    .. method:: Off()

        Eteins le bouton.


    .. method:: Switch()

        Change l'état de la lumière du bouton.

    .. method:: SetFunction(function,*args)

        Méthode d'affectation de la fonction pour le bouton. 

        :param function: Fonction à appeler à chaque changement d'état du bouton.
        :param args: Arguments à passer à la fonction lors de l'appel.

    .. method:: Close()

        Coupe le bouton et libére les pins pour une autre utilisation.

        

    .. method:: LaunchFunction(args)

        Méthode interne d'appel de la fonction paramétrée.