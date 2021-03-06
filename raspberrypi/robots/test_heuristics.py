from robots.heuristics           import Heuristics
from robots.action               import Action
import time

shortshot = Action(None, None, None, "shortshot", 40, 20)
longshot = Action(None, None, None, "longshot", 20, 30)
dispMono = Action(None, None, None, "dispMono", 10, 10)
dispMulti = Action(None, None, None, "dispMulti", 10, 10)
abeille = Action(None, None, None, "abeille", 50, 10)
panneau = Action(None, None, None, "Panneau", 25, 5)
treatment = Action(None, None, None, "traitement", 40, 10)

dispMono.set_reliability(0.6)
dispMulti.set_reliability(0.6)
shortshot.set_reliability(0.8)
longshot.set_reliability(0.8)

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
