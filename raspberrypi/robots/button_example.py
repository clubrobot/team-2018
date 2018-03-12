from components import *
from buttons    import *

def button(bytes):
    print("Bouton " + str(bytes.read(BYTE)+1))

def emergency(a):
    print ("Emergency")

def tirette(a) :
    print("Tirette")

def mode(bytes):
    print("Mode{}".format(bytes.read(BYTE) ))


t = Manager()
t.connect()

b = ButtonCard(t)

b.bind(1,button)
b.bind(2,emergency)
b.bind(3,tirette)
b.bind(4,mode)

b.setLedOn(5)