import math

class Heuristics:
    POINTS_INFLUENCE = 1
    ORDER_INFLUENCE = 1
    DONE_INFLUENCE = 1
    RELIABILITY_INFLUENCE = 1
    COMBINATIONS_INFLUENCE = 1
    TIME_INFLUENCE = 1
    DISTANCE_INFLUENCE = 1
    OPPONENT_INFLUENCE = 1

    def __init__(self, actions, arduinos, logger, beacon_management):
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

        self.heuristics_soft = [self.points, self.reliability, self.time, self.action_distance, self.opponent_position]
        self.heuristics_hard = [self.order, self.combinations, self.done]
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
        heuristic = self.mul_dict(heuristic, Heuristics.ORDER_INFLUENCE)
        self.logger("HEURISTIC : ", "order", heuristic=heuristic)
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

        heuristic = self.mul_dict(heuristic, Heuristics.POINTS_INFLUENCE)
        self.logger("HEURISTIC : ", "points", heuristic=heuristic)
        return heuristic

    def combinations(self):
        heuristic = dict()
        for action in self.action_names:
            if self.action_dict[action].check_impossible_combinations(self.action_dict) is False:
                heuristic[action] = 0
            else:
                heuristic[action] = 1

        heuristic = self.mul_dict(heuristic, Heuristics.COMBINATIONS_INFLUENCE)
        self.logger("HEURISTIC : ", "combinations", heuristic=heuristic)
        return heuristic

    def done(self):
        heuristic = dict()
        for action in self.action_names:
            if self.action_dict[action].done:
                heuristic[action] = 0
            else:
                heuristic[action] = 1
        heuristic = self.mul_dict(heuristic, Heuristics.DONE_INFLUENCE)
        self.logger("HEURISTIC : ", "done", heuristic=heuristic)
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

        heuristic = self.mul_dict(heuristic, Heuristics.DISTANCE_INFLUENCE)
        self.logger("HEURISTIC : ", "distance to action", heuristic=heuristic)
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
        heuristic = self.mul_dict(heuristic, Heuristics.TIME_INFLUENCE)
        self.logger("HEURISTIC : ", "time", heuristic=heuristic)
        return heuristic

    def opponent_position(self):
        heuristic = dict()
        for action in self.action_names:
            if self.action_dict[action].area is not None:
                heuristic[action] = 1 - self.beacon_management.get_area_value(self.action_dict[action].area)
            else:
                heuristic[action] = 1

        heuristic = self.mul_dict(heuristic, Heuristics.OPPONENT_INFLUENCE)
        self.logger("HEURISTIC : ", "opponent_position", heuristic=heuristic)
        return heuristic

    def mul_dict(self, dict, mul):
        for action in self.action_names:
            dict[action] *= mul
        return dict

    def reliability(self):
        heuristic = dict()
        for action in self.action_names:
            heuristic[action] = self.action_dict[action].reliability
        print(" * RELIABILITY")
        heuristic = self.mul_dict(heuristic, Heuristics.RELIABILITY_INFLUENCE)
        print(heuristic)
        return heuristic

    def compute_heuristics(self):
        heuristics_values = dict()
        for action in self.action_names:
            heuristics_values[action] = 1

        for heuristic in self.heuristics_soft:
            current_values = heuristic()
            for action in self.action_names:
                heuristics_values[action] += current_values[action]

        for action in self.action_names:
            heuristics_values[action] /= len(self.heuristics_soft)

        for heuristic in self.heuristics_hard:
            current_values = heuristic()
            for action in self.action_names:
                tmp = current_values[action]
                heuristics_values[action] *= tmp

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
            return None
        return self.action_dict[name_best]
            

    