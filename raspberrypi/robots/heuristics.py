import math

class Heuristics:
    MANUAL = 1
    AUTO = 0
    def __init__(self, actions, arduinos, logger, beacon_management, mode=AUTO):
        self.actions = actions
        self.action_names = []
        self.action_dict = dict()
        self.logger = logger
        for action in self.actions:
            self.action_names += [action.name] 
            self.action_dict[action.name] = action

        for action in self.action_names:
            self.init_time_recursive(self.action_dict[action], self.action_dict[action].time)
            self.init_reliability_recursive(self.action_dict[action], self.action_dict[action].reliability)
            self.init_points_recursive(self.action_dict[action], self.action_dict[action].points)

        if mode is not Heuristics.MANUAL:
            self.heuristics_soft = [self.points, self.reliability, self.time, self.action_distance]
            if beacon_management is not None:
                self.heuristics_soft += [self.opponent_position]

            self.influences = {"points":3, "reliability":1, "time":2, "action_distance":1, "opponent_position": 4}
            self.heuristics_hard = [self.order, self.combinations, self.done]

        else:
            self.heuristics_soft = [self.manual]
            self.influences = {"manual":10000}
            self.heuristics_hard = [self.done]

        self.wheeledbase = arduinos["wheeledbase"]
        self.beacon_management = beacon_management

    def init_points_recursive(self, action, points):
        for pred in action.predecessors:
            pred.points += points
            self.init_points_recursive(pred, points)

    def init_time_recursive(self, action, time):
        for pred in action.predecessors:
            pred.points += time
            self.init_points_recursive(pred, time)

    def init_reliability_recursive(self, action, reliability):
        for pred in action.predecessors:
            pred.reliability *= reliability
            self.init_points_recursive(pred, reliability)

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

    def manual(self):
        MAX_MANUAL_ORDER = 20
        heuristic = dict()
        for action in self.action_names:
            if self.action_dict[action].manual_order == 0:
                heuristic[action] = 0
            else:
                heuristic[action] = MAX_MANUAL_ORDER - self.action_dict[action].manual_order/MAX_MANUAL_ORDER
        return heuristic

    def points(self):
        heuristic = dict()
        max_points = 0
        for action in self.action_names:
            if not self.action_dict[action].done:
                max_points = max(self.action_dict[action].points, max_points)

        for action in self.action_names:
            if max_points != 0:
                heuristic[action] = self.action_dict[action].points/max_points
            else:
                heuristic[action] = 0
        return heuristic

    def combinations(self):
        heuristic = dict()
        for action in self.action_names:
            if self.action_dict[action].check_impossible_combinations() is False:
                heuristic[action] = 0
            else:
                heuristic[action] = 1
        return heuristic

    def done(self):
        heuristic = dict()
        for action in self.action_names:
            if self.action_dict[action].done:
                heuristic[action] = 0
            else:
                heuristic[action] = 1
        return heuristic

    def action_distance(self):
        heuristic = dict()
        max_distance = 0
        robot_pos = self.wheeledbase.get_position()[:-1]
        for action in self.action_names:
            if not self.action_dict[action].done:
                point = self.action_dict[action].actionPoint
                max_distance = max(math.hypot(robot_pos[0] - point[0], robot_pos[1] - point[1]), max_distance)

        for action in self.action_names:
            point = self.action_dict[action].actionPoint
            if max_distance != 0:
                heuristic[action] = 1 - math.hypot(robot_pos[0] - point[0], robot_pos[1] - point[1]) / max_distance
            else:
                heuristic[action] = 0
        return heuristic

    def time(self):
        heuristic = dict()
        max_time = 0
        for action in self.action_names:
            if not self.action_dict[action].done:
                max_time = max(self.action_dict[action].points, max_time)

        for action in self.action_names:
            if max_time != 0:
                heuristic[action] = 1-self.action_dict[action].points / max_time
            else:
                heuristic[action] = 0
        return heuristic

    def opponent_position(self):
        heuristic = dict()
        for action in self.action_names:
            if self.action_dict[action].area is not None:
                heuristic[action] = 1 - self.beacon_management.get_area_value(self.action_dict[action].area)
            else:
                heuristic[action] = 1
        return heuristic


    def reliability(self):
        heuristic = dict()
        for action in self.action_names:
            heuristic[action] = self.action_dict[action].reliability
        return heuristic

    def compute_heuristics(self):
        heuristics_values = dict()
        for action in self.action_names:
            heuristics_values[action] = 0

        total_influences = 0
        for heuristic in self.heuristics_soft:
            current_values = heuristic()
            for action in self.action_names:
                heuristics_values[action] += current_values[action] * self.influences[heuristic.__name__]
            total_influences += self.influences[heuristic.__name__]
            self.logger("HEURISTIC : ", heuristic.__name__, heuristic=current_values)

        for action in self.action_names:
            heuristics_values[action] /= total_influences

        for heuristic in self.heuristics_hard:
            current_values = heuristic()
            for action in self.action_names:
                heuristics_values[action] *= current_values[action]
            self.logger("HEURISTIC : ", heuristic.__name__, heuristic=current_values)

        self.logger("HEURISTIC : ", "TOTAL", heuristic=heuristics_values)
        return heuristics_values

    def get_best(self):
        heuristics_values = self.compute_heuristics()
        name_best = ""
        for action in self.action_names:
            if heuristics_values[action] == 0:
                continue
            if name_best == "" or heuristics_values[action] > heuristics_values[name_best]:
                name_best = action
        if name_best == "":
            print("NO ACTION")
            return None
        return self.action_dict[name_best]
