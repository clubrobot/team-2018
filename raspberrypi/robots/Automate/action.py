class Action():
    def __init__(self,actionPoint,actionFunction,typ, name):
        self.actionPoint=actionPoint
        self.actionFunction=actionFunction
        self.typ=typ
        self.predecessors = []
        self.done = False
        self.name = name
        
    def __call__(self):
        self.actionFunction()

    def realize(self):
        self()

    def set_predecessors(self, predecessors):
        self.predecessors = predecessors

class Actionnable():
    def getAction(self,robot,builerCollector,waterDispenser):
        raise NotImplementedError("Need implementation")
