from heuristics           import Heuristics
from action               import Action
import time

shortshot = Action(None, None, None, "shortshot", 40)
longshot = Action(None, None, None, "longshot", 20)
dispMono = Action(None, None, None, "dispMono", 10)
dispMulti = Action(None, None, None, "dispMulti", 10)
abeille = Action(None, None, None, "abeille", 50)
panneau = Action(None, None, None, "Panneau", 25)
treatment = Action(None, None, None, "traitement", 40)

treatment.set_predecessors([longshot])
longshot.set_predecessors([dispMulti])
shortshot.set_predecessors([dispMono])

dispMulti.set_impossible_combination(lambda: dispMono and not shortshot)
dispMono.set_impossible_combination(lambda: dispMulti and (not longshot or not treatment))

actions = [shortshot, longshot, dispMono, abeille, dispMulti, treatment, panneau]

h = Heuristics(actions)

act = h.get_best()
while act is not None:
    print(" ====> "+ act.name)
    print("-------------------------------------------")
    act.done = True
    act = h.get_best()
    #time.sleep(0.5)
