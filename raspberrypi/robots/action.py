class Action():
    def __init__(self,actionPoint,actionFunction,typ):
        self.actionPoint=actionPoint
        self.actionFunction=actionFunction
        self.typ=typ

    def __call__(self):
        self.actionFunction()

    def realize(self):
        self()

class Actionnable():
    def getAction(self,robot,builerCollector,waterDispenser):
        raise NotImplementedError("Need implementation")
