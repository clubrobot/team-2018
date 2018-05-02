class Heuristics:
    def __init__(self, actions):
        self.actions = actions
        self.action_names = []
        self.action_dict = dict()
        for action in self.actions:
            self.action_names += [action.name] 
            self.action_dict[action.name] = action
        self.heuristics = [self.order]
        

    def order(self):
        heuristic = dict()
        for action in self.action_names:
            available = True
            for pred in self.action_dict[action].predecessors:
                if not pred.done:
                    available = False
            if available:
                heuristic[action] = 1
            else:
                heuristic[action] = 0

        return heuristic
    
    def computeHeuristic(self):
        heuristics_values = dict()
        for action in self.action_names:
            heuristics_values[action] = 1

        for heuristic in self.heuristics:
            current_values = heuristic()
            for action in self.action_names:
                heuristics_values[action] *= current_values[action]
        
        return heuristics_values

    def getBest(self):
        heuristics_values = self.computeHeuristic()
        name_best = ""
        for action in self.action_names:
            if  (name_best == "" \
                or heuristics_values[action] > heuristics_values[name_best])\
                and not self.action_dict[action].done:
                name_best = action
        if name_best == "":
            return None
        return self.action_dict[name_best]
            

    