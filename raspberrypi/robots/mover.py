#!/usr/bin/env python3
# coding: utf-8

from math import cos, sin, pi, copysign, hypot
from threading import *
import time
from statistics import mean

from common.sync_flag_signal import Flag
from robots.listener.sensor_listener import *
from common.roadmap import RoadMap

DELTA = 100
PUREPURSUIT_LOOKAHEAD_ID = 0xE0
# temps pour reset obstacle
TIMEOUT_OBSTACLE = 5

# TODO
# Faire des cas particulier pour les sensors qui sont activé que sur les coté et si la velocity angulaire souhaité est trop haut

# <> CONSTANTE <>

# - Turnonthespot
WALL_RANGE = 200
ENEMY_RANGE = 400
SENSORS_RANGE = 200
BACKWARD_VELOCITY = 150

# -  GOWALL
WALL_RANGE_TO_MOVE = 100
SENSORS_RANGE = 200

# -  BEACONS CONSTANT
ENEMY_THRESHOLD = 200


# <> ERROR <>
class PositionUnreachable(RuntimeError):
    pass


class Mover:
    AIM = 1
    SOFT = 2
    QUICK = 3
    SAFE = 4
    FAST = 5
    SIMPLE = 6
    HARD = 7
    SENSORS = 8
    POSITION = 9

    def __init__(self, side, roadmap, arduinos, logger, becons_receiver):

        # RoadMap et ses obstacles virtuel
        self.roadmap = roadmap
        self.logger = logger
        self.becons_receiver = becons_receiver

        # Arduino et autre
        self.wheeledbase = arduinos["wheeledbase"]
        self.sensors_front = arduinos["sensors_front"]
        self.sensors_lat = arduinos["sensors_lat"]
        self.sensors_back = arduinos["sensors_back"]
        self.side = side

        # Objet qui sont en relation avec les sensors
        self.sensors_front_listener = SensorListener(self.sensors_front.get_mesure)
        self.sensors_back_listener = SensorListener(self.sensors_back.get_mesure)
        # Flags relier a des fonctions interne pour tout bien gérer

        self.front_flag = Flag(self.front_obstacle)
        self.withdraw_flag = Flag(self._withdraw_interrup)

        self.path = list()
        self.isarrived = False
        self.interupted_lock = RLock()
        self.interupted_status = Event()
        self.interupted_timeout = Event()
        self.running = Event()
        self.direction = "forward"
        self.goal = (0, 0, 0)
        self.timeout = 1

    def reset(self):
        self.front_flag.clear()
        self.withdraw_flag.clear()
        self.wheeledbase.reset_parameters()
        self.interupted_timeout.clear()
        self.interupted_status.clear()
        self.isarrived = False
        self.path = list()
        self.running.clear()
        self.direction = "forward"
        self.goal = (0, 0, 0)

    def get_enemy_status(self, x, y):
        robot_0 = self.becons_receiver.get_position(0)
        robot_1 = self.becons_receiver.get_position(1)
        if hypot(robot_0[0] - x, robot_0[1] - y) < ENEMY_THRESHOLD or robot_0 == (-1000, -1000):
            return True
        if hypot(robot_1[0] - x, robot_1[1] - y) < ENEMY_THRESHOLD or robot_1 == (-1000, -1000):
            return True
        return False

    @staticmethod
    def get_wall_status(x, y):
        return x < WALL_RANGE or (2000 - x) < WALL_RANGE or y < WALL_RANGE or (3000 - y) < WALL_RANGE

    def gowall(self, try_limit=3, strategy=SENSORS, direction="forward", position=None):
        #  /\ Determination de la proximité avec un enemies et initialisation des variables /\
        # closed_to_enemy = self.get_enemy_status()
        self.goal = self.wheeledbase.get_position()
        if strategy == Mover.SENSORS:
            self._gowall_sensors(try_limit, direction)
        elif strategy == Mover.POSITION:
            if position is None:
                raise ValueError
            self._gowall_position(try_limit, direction, position)
        self.reset()

    # Button activation
    def _gowall_sensors(self, try_limit, direction):
        wall_reached = False
        nb_try = try_limit
        direction = {"forward": 1, "backward": -1}[direction]
        while not wall_reached:
            try:
                self.wheeledbase.set_velocities(250 * direction, 0)
                while not self.wheeledbase.isarrived():
                    time.sleep(0.1)
            except RuntimeError:
                if not nb_try > 0:
                    break
                nb_try -= 1
                if (direction == 1 and mean(self.sensors_front.get_mesure()) < 45) or (
                        direction == -1 and mean(self.sensors_back.get_mesure()) < 55):
                    wall_reached = True

                else:
                    # TODO maybe increase the threshold 40
                    print(mean(self.sensors_back.get_mesure()))
                    print(mean(self.sensors_front.get_mesure()))
                    _, ang = self.wheeledbase.get_velocities_wanted(True)
                    print(ang)
                    print(nb_try)
                    if abs(ang) > 4.5:
                        # Try to reach the initial angle
                        while True:
                            try:
                                # TODO DANGER
                                self.wheeledbase.left_wheel_maxPWM.set(0.5)
                                self.wheeledbase.right_wheel_maxPWM.set(0.5)
                                self.wheeledbase.turnonthespot(self.goal[-1])
                                self.wheeledbase.wait()
                                self.wheeledbase.left_wheel_maxPWM.set(1)
                                self.wheeledbase.right_wheel_maxPWM.set(1)
                                break
                            except RuntimeError:
                                self.wheeledbase.left_wheel_maxPWM.set(1)
                                self.wheeledbase.right_wheel_maxPWM.set(1)
                                self.wheeledbase.set_velocities(-100 * direction, 0)
                                sleep(0.2)
                                self.wheeledbase.stop()
                        # Go backward
                        if ang < 0:
                            self.wheeledbase.goto_delta(-50 * direction, 0)
                        else:
                            self.wheeledbase.goto_delta(-40 * direction, 0)
                        try:
                            self.wheeledbase.wait()
                        except RuntimeError:
                            pass

                        # TURN HARD
                        self.wheeledbase.set_velocities(0, copysign(6, -ang))
                        sleep(0.8)
                        try:
                            self.wheeledbase.turnonthespot(self.goal[-1])
                            self.wheeledbase.wait()
                        except RuntimeError:
                            pass
                    else:
                        self.wheeledbase.goto_delta(-10 * direction, 0)
                        try:
                            self.wheeledbase.wait()
                        except RuntimeError:
                            pass
                        self.wheeledbase.set_velocities(0, -6)
                        sleep(0.8)
                        self.wheeledbase.stop()
                        while True:
                            try:
                                self.wheeledbase.turnonthespot(self.goal[-1])
                                self.wheeledbase.wait()
                                break
                            except RuntimeError:
                                pass

    def _gowall_position(self, try_limit, direction, position_goal):
        wall_reached = False
        nb_try = try_limit
        direction = {"forward": 1, "backward": -1}[direction]
        while not wall_reached:
            try:
                self.wheeledbase.set_velocities(250 * direction, 0)
                while not self.wheeledbase.isarrived():
                    time.sleep(0.1)
            except RuntimeError:
                if not nb_try > 0:
                    break
                nb_try -= 1

                current_position = self.wheeledbase.get_position()
                # TODO Change for more generic com      paraison
                self.logger("MOVER : ", position_goal=position_goal, current_position=current_position)
                if abs(current_position[0] - position_goal[0]) < 30:
                    wall_reached = True

                else:
                    _, ang = self.wheeledbase.get_velocities_wanted(True)
                    self.logger("MOVER : ", "Obstacle detected")
                    if abs(ang) > 4.5:
                        self.logger("MOVER : ", "Try to avoid a lateral obstacle")
                        # Try to reach the initial angle
                        while True:
                            try:
                                # TODO DANGER
                                self.wheeledbase.left_wheel_maxPWM.set(0.5)
                                self.wheeledbase.right_wheel_maxPWM.set(0.5)
                                self.wheeledbase.turnonthespot(self.goal[-1])
                                self.wheeledbase.wait()
                                self.wheeledbase.left_wheel_maxPWM.set(1)
                                self.wheeledbase.right_wheel_maxPWM.set(1)
                                break
                            except RuntimeError:
                                self.wheeledbase.left_wheel_maxPWM.set(1)
                                self.wheeledbase.right_wheel_maxPWM.set(1)
                                self.wheeledbase.set_velocities(-100 * direction, 0)
                                sleep(0.2)
                                self.wheeledbase.stop()
                        # Go backward
                        if ang < 0:
                            self.wheeledbase.goto_delta(-50 * direction, 0)
                        else:
                            self.wheeledbase.goto_delta(-40 * direction, 0)
                        try:
                            self.wheeledbase.wait()
                        except RuntimeError:
                            pass

                        # TURN HARD
                        print("ANG", ang)
                        self.wheeledbase.set_velocities(0, copysign(6, -ang))
                        sleep(0.8)
                        try:
                            self.wheeledbase.turnonthespot(self.goal[-1])
                            self.wheeledbase.wait()
                        except RuntimeError:
                            pass
                    else:
                        self.logger("MOVER : ", "Try to avoid a front obstacle")
                        self.wheeledbase.goto_delta(-10 * direction, 0)
                        try:
                            self.wheeledbase.wait()
                        except RuntimeError:
                            pass
                        self.wheeledbase.set_velocities(0, -6)
                        sleep(0.8)
                        self.wheeledbase.stop()
                        while True:
                            try:
                                self.wheeledbase.turnonthespot(self.goal[-1])
                                self.wheeledbase.wait()
                                break
                            except RuntimeError:
                                pass

    def withdraw(self, x, y, direction="forward", timeout=5, strategy=SIMPLE, last_point_aim=None):
        self.goal = (x, y)
        self.timeout = timeout
        if strategy == Mover.SIMPLE:
            self._withdraw_simple(direction)
        if strategy == Mover.HARD:
            self._withdraw_hard(direction, last_point_aim)
        self.reset()

    def _withdraw_simple(self, direction):
        self.wheeledbase.max_linvel.set(100)

        self.direction = direction
        if direction == "forward":
            self.withdraw_flag.bind(self.sensors_front_listener.signal)
            self.sensors_front_listener.threadhold = 80
        else:
            self.withdraw_flag.bind(self.sensors_back_listener.signal)
            self.sensors_back_listener.threadhold = 80
        while not self.isarrived or self.interupted_status.is_set():

            try:
                if self.interupted_status.is_set():
                    sleep(0.2)
                else:
                    self.wheeledbase.goto(*self.goal, direction=direction)
                    self.isarrived = True

            except RuntimeError:
                if self.interupted_timeout.is_set():
                    sleep(0.7)
                    self.wheeledbase.set_velocities(100 if direction == "forward" else -100, 0)
                    sleep(0.3)
                    self.wheeledbase.stop()
                else:
                    pass
        self.reset()

    def _withdraw_hard(self, direction, last_point_aim):
        self.wheeledbase.max_linvel.set(100)
        self.logger("MOVER : ", "Start withdraw hard")
        self.direction = direction
        if direction == "forward":
            self.withdraw_flag.bind(self.sensors_front_listener.signal)
            self.sensors_front_listener.threadhold = 80
        else:
            self.withdraw_flag.bind(self.sensors_back_listener.signal)
            self.sensors_back_listener.threadhold = 80
        while not self.isarrived or self.interupted_status.is_set():

            try:
                if self.interupted_status.is_set():
                    sleep(0.2)
                else:
                    self.logger("MOVER : ", "Launch a goto")
                    self.wheeledbase.goto(*self.goal, direction=direction)
                    self.isarrived = True

            except RuntimeError:
                self.logger("MOVER : ", "Spin detected !")
                if self.interupted_status.is_set():
                    continue
                self.logger("MOVER : ", 'Go back a little !')
                self.wheeledbase.stop()
                if last_point_aim is None:
                    self.wheeledbase.set_velocities(-100 if self.direction == "forward" else 100, 0)
                else:
                    try:
                        self.wheeledbase.goto(*last_point_aim)
                    except RuntimeError:
                        pass
                time.sleep(0.5)
                self.wheeledbase.stop()

    def _withdraw_interrup(self):
        self.logger("MOVER : ", "Interruption !")
        if self.interupted_timeout.is_set():
            return
        if not self.interupted_lock.acquire(blocking=False):
            return
        self.interupted_status.set()
        self.logger("MOVER : ", "Stop the wheeledbase")
        self.wheeledbase.stop()
        sensors = self.sensors_front if self.direction == "forward" else self.sensors_back
        try:
            self.logger("MOVER : ", "Wait sensors")
            sensors.wait(80, timeout=self.timeout)
        except TimeoutError:
            self.logger("MOVER : ", "Time out ", self.timeout)
            self.interupted_timeout.set()
            self.withdraw_flag.clear()
            self.wheeledbase.max_linvel.set(100)
        self.interupted_status.clear()
        self.interupted_lock.release()

    def turnonthespot(self, angle, try_limit=3, stategy=AIM):
        self.running.set()
        self.isarrived = False
        self.goal = (*self.wheeledbase.get_position()[:-1], angle)
        try:
            if stategy == Mover.AIM:
                self._turnonthespot_aim(try_limit)
            if stategy == Mover.SOFT:
                self._turnonthespot_soft(try_limit)
        except PositionUnreachable:
            self.reset()
            raise PositionUnreachable()
        else:
            self.reset()

    def _turnonthespot_soft(self, try_limit):
        try_number = 0
        way = 'forward'
        closed_to_wall = self.get_wall_status(*self.goal[:-1])  # Boolean qui représente la proximité à un cube
        closed_to_enemy = True  # self.get_enemy_status() # Boolean qui représente la proximité à un enemie
        position_reach = False
        while not position_reach and ((try_limit + 1) >= try_number or try_limit < 0):
            try:
                self.wheeledbase.turnonthespot(self.goal[2], direction=way)
                self.wheeledbase.wait()
                position_reach = True
            except RuntimeError:
                _, ang_vel = self.wheeledbase.get_velocities_wanted(True)
                # /\ récupéré les données des balises de devant /\
                if ang_vel >= 0:
                    std_f, _ = self.sensors_front.get_normal(0)[1]
                if ang_vel < 0:
                    std_f, _ = self.sensors_front.get_normal(0)[0]
                # /\ récupéré les données des balises de derriere /\
                if ang_vel >= 0:
                    std_b, _ = self.sensors_back.get_normal(0)[0]
                if ang_vel < 0:
                    std_b, _ = self.sensors_back.get_normal(0)[1]
                # /\ récupéré les données des balises des côtés /\
                std_l, _ = self.sensors_lat.get_normal(0)[1]
                std_r, _ = self.sensors_back.get_normal(0)[0]
                # <> Premiere essaie <>
                if try_number == 0:
                    if closed_to_enemy and (std_f < SENSORS_RANGE or std_b < SENSORS_RANGE):
                        self.wheeledbase.max_angvel.set(1.5)
                        if std_f < SENSORS_RANGE:
                            try:
                                self.sensors_front.wait(SENSORS_RANGE, 22)
                            except TimeoutError:
                                pass
                        else:
                            try:
                                self.sensors_back.wait(SENSORS_RANGE, 22)
                            except TimeoutError:
                                pass
                        try_number += 1
                        continue

                    self.wheeledbase.max_angvel.set(2)
                    try_number += 1
                    continue
                if try_number == 1:
                    # On ne regarde pas les enemies on change juste de sens
                    way = {'forward': 'backward', 'backward': 'forward'}[way]
                    try_number += 1
                    continue
                if try_number == 2:
                    # On regarde les enemies et si c'est bien ce probleme on attend un peu sinon on change de sens
                    if closed_to_enemy and (std_f < SENSORS_RANGE or std_b < SENSORS_RANGE):
                        self.wheeledbase.max_angvel.set(1.5)
                        if std_f < SENSORS_RANGE:
                            self.sensors_front.wait(SENSORS_RANGE, 2)
                        else:
                            self.sensors_back.wait(SENSORS_RANGE, 2)
                        try_number += 1
                        continue

                    way = {'forward': 'backward', 'backward': 'forward'}[way]
                    try_number += 1
                    continue
                if try_number == 3:
                    try_number = 0
                    try_limit -= 3
                    continue

        if not position_reach:
            raise PositionUnreachable()

    def _turnonthespot_aim(self, try_limit):

        try_number = 0
        way = 'forward'
        closed_to_wall = self.get_wall_status(*self.goal[:-1])  # Boolean qui représente la proximité à un cube
        closed_to_enemy = self.get_enemy_status(*self.goal[:-1])  # Boolean qui représente la proximité à un enemie
        self.wheeledbase.left_wheel_maxPWM.set(0.4)
        self.wheeledbase.right_wheel_maxPWM.set(0.4)
        constant_pwm = 0.4
        while not self.isarrived and ((try_limit - try_number) > 0 or try_limit < 0):
            try:
                self.wheeledbase.turnonthespot(self.goal[2], direction=way)
                self.wheeledbase.wait()
                self.isarrived = True
            except RuntimeError:
                self.wheeledbase.stop()
                lin_vel, ang_vel = self.wheeledbase.get_velocities_wanted(True)
                if abs(lin_vel) > 300:
                    self.wheeledbase.set_velocities(copysign(BACKWARD_VELOCITY, -lin_vel), 0)
                    time.sleep(0.35)
                    self.wheeledbase.stop()
                else:
                    constant_pwm = min(constant_pwm + 0.2, 1)
                    way = {'forward': 'backward', 'backward': 'forward'}[way]
                    self.wheeledbase.left_wheel_maxPWM.set(constant_pwm)
                    self.wheeledbase.right_wheel_maxPWM.set(constant_pwm)
                try_number += 1

        if not self.isarrived:
            raise PositionUnreachable()

    def goto(self, x, y):
        self.goal = (x, y)

        # self.on_path_flag.bind(self.big_listener.signal)
        # self.on_path_flag.bind(self.little_listener.signal)
        self.front_flag.bind(self.sensors_front_listener.signal)

        # self.obstacle_big.set_position(*self.balise.get_position(BIG_ROBOT))
        # self.obstacle_little.set_position(*self.balise.get_position(LITTLE_ROBOT))

        self.path = self.roadmap.get_shortest_path(self.wheeledbase.get_position()[:2], self.goal)
        self.logger("MOVER : ", path=self.path)
        self.wheeledbase.purepursuit(self.path)
        self.isarrived = False
        while not self.isarrived or self.interupted_status.is_set():
            try:
                self.isarrived = self.wheeledbase.isarrived()
                sleep(0.1)
            except RuntimeError:
                if not self.interupted_lock.acquire(blocking=True, timeout=0.5):
                    continue
                x, y, _ = self.wheeledbase.get_position()
                # Si tu n'est pas a coté d'un enemie
                # TODO
                if not self.get_enemy_status(x, y):
                    vel, ang = self.wheeledbase.get_velocities_wanted()
                    self.wheeledbase.set_velocities(copysign(150, -vel), copysign(1, ang))
                    time.sleep(1)  # 0.5
                    self.wheeledbase.set_velocities(copysign(150, vel), 0)
                    time.sleep(1.2)
                    self.wheeledbase.purepursuit(self.path)
                # Si tu est 
                else:
                    pass

                sleep(1)
                # self.path = self.roadmap.get_shortest_path(self.wheeledbase.get_position()[:2],self.goal)
                self.wheeledbase.purepursuit(self.path)
                self.interupted_lock.release()
            except TimeoutError:
                self.isarrived = False

        # self.on_path_flag.clear()

        self.reset()

    def front_obstacle(self):
        # RoadMap.LEFT
        # RoadMap.RIGHT

        self.logger("MOVER : ", "Object in the front detected !")
        if not self.interupted_lock.acquire(blocking=True, timeout=1):
            return
        self.interupted_status.set()
        x, y, theta = self.wheeledbase.get_position()
        if hypot(y - self.goal[1], x - self.goal[0]) < 300:
            self.interupted_status.clear()
            self.interupted_lock.release()
            # TODO QUOI FAIRE ?
            return

        if not self.get_enemy_status(x, y):
            self.interupted_status.clear()
            self.interupted_lock.release()
            return

        lin_wanted, ang_wanted = self.wheeledbase.get_velocities_wanted()
        if abs(ang_wanted) > 7:
            self.wheeledbase.set_velocities(copysign(150, -lin_wanted), copysign(1, ang_wanted))
            time.sleep(1)  # 0.5
            self.wheeledbase.set_velocities(copysign(150, lin_wanted), 0)
            time.sleep(1.2)
            self.wheeledbase.purepursuit(self.path)

        self.wheeledbase.stop()

        side = self.roadmap.best_side(x, y, theta)
        time.sleep(0.4)
        (left, _), (right, _) = self.sensors_front.get_normal(0)
        if left > 800:
            side = RoadMap.LEFT
        if right > 800:
            side = RoadMap.RIGHT
        self.logger("MOVER : ", "I'm decided to turn {} at {},{}".format("left" if side == 1 else "right", x, y))
        while True:
            try:
                self.wheeledbase.turnonthespot(theta - pi / 2)

                self.wheeledbase.wait()
                break
            except RuntimeError:
                self.wheeledbase.stop()
                # PROBLEME
                self.wheeledbase.set_velocities(-200, 0)
                time.sleep(0.4)
                self.wheeledbase.stop()
                continue

        time.sleep(1)
        # Wait varience  pour attendre des variables stable
        init_time = time.time()
        while self.sensors_lat.get_normal(0)[0][1] > 1000 and time.time() - init_time < 2:
            time.sleep(0.2)
        self.wheeledbase.set_velocities(-100 * side, 0)
        # print(self.sensors_lat.get_normal(0))
        while self.sensors_lat.get_normal(0)[0][0] < 200:
            try:
                self.wheeledbase.isarrived()
                if self.sensors_lat.get_normal(0)[0][0] < 35:
                    self.wheeledbase.set_velocities(-100 * side, 0.2 * side)
                else:
                    self.wheeledbase.set_velocities(-100 * side, 0)
                time.sleep(0.2)
            except RuntimeError:
                side *= -1
                self.wheeledbase.set_velocities(-100 * side, 0)
        time.sleep(0.1)
        self.wheeledbase.stop()
        x_p, y_p, theta_p = self.wheeledbase.get_position()
        self.wheeledbase.turnonthespot(theta)
        try:
            self.wheeledbase.wait()
        except RuntimeError:
            pass
            # Creation de l'obstacle
        x_obs = (x + x_p) / 2
        y_obs = (y + y_p) / 2
        height = hypot(x - x_p, y - y_p)
        x_obs += cos(theta) * 200
        y_obs += sin(theta) * 200
        obs = self.roadmap.create_temp_obstacle(
            ((-100, height / 2), (-100, -height / 2), (100, -height / 2), (100, height / 2)), timeout=TIMEOUT_OBSTACLE)
        obs.set_position(x_obs, y_obs, theta)
        self.path = self.roadmap.get_shortest_path((x_p, y_p), self.goal)
        # try:
        self.wheeledbase.purepursuit(self.path)
        # except ValueError:
        #    pass  # TODO
        self.interupted_status.clear()
        self.interupted_lock.release()
