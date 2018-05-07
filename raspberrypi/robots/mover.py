#!/usr/bin/env python3
# coding: utf-8

from math import cos, sin, pi, copysign, hypot, atan2
from threading import *
import time
from statistics import mean

from common.sync_flag_signal import Flag
from robots.listener.sensor_listener import *
from common.roadmap import RoadMap

DELTA = 100
PUREPURSUIT_LOOKAHEAD_ID = 0xE0
# temps pour reset obstacle
TIMEOUT_OBSTACLE = 7

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

# GOTO
TIMEOUT_GOAL = 5


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
        self.goto_interrupt = Event()
        # Objet qui sont en relation avec les sensors
        self.sensors_front_listener = SensorListener(self.sensors_front.get_mesure)
        self.sensors_back_listener = SensorListener(self.sensors_back.get_mesure)
        # Flags relier a des fonctions interne pour tout bien gérer

        self.front_flag = Flag(self.front_obstacle)
        self.withdraw_flag = Flag(self._withdraw_interrup)
        self.front_safe_flag = Flag(self.front_obstacle_safe)
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
        self.front_safe_flag.clear()
        self.wheeledbase.reset_parameters()
        self.interupted_timeout.clear()
        self.interupted_status.clear()
        self.goto_interrupt.clear()
        self.isarrived = False
        self.path = list()
        self.running.clear()
        self.direction = "forward"
        self.goal = (0, 0, 0)

    def get_enemy_status(self, x, y):
        return True

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
                if abs(current_position[0] - position_goal[0]) < 60:
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
        self.wheeledbase.max_linvel.set(200)

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
        self.wheeledbase.max_linvel.set(200)
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
                    sleep(0.5)
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
        x, y, _ = self.wheeledbase.get_position()
        while hypot(x-self.goal[0],y-self.goal[1])>300:
            while not self.isarrived or self.interupted_status.is_set():
                try:
                    if(self.goto_interrupt.is_set()):
                        break

                    self.isarrived = self.wheeledbase.isarrived()
                    sleep(0.1)
                except RuntimeError:
                    if not self.interupted_lock.acquire(blocking=True, timeout=0.5):
                        while self.interupted_status.is_set():
                            sleep(0.1)
                        continue
                    self.logger("MOVER : ", "Spin! ")
                    x, y, _ = self.wheeledbase.get_position()
                    vel, ang = self.wheeledbase.get_velocities_wanted(True)
                    self.wheeledbase.set_velocities(copysign(150, -vel), copysign(1, ang))
                    time.sleep(1)  # 0.5
                    self.wheeledbase.set_velocities(copysign(150, vel), 0)
                    time.sleep(1.2)
                    self.wheeledbase.purepursuit(self.path)


                    sleep(1)
                    # self.path = self.roadmap.get_shortest_path(self.wheeledbase.get_position()[:2],self.goal)
                    self.wheeledbase.purepursuit(self.path)
                    self.interupted_lock.release()
                except TimeoutError:
                    self.isarrived = False

            x, y, _ = self.wheeledbase.get_position()

        # self.on_path_flag.clear()
        if (self.goto_interrupt.is_set()):
            self.reset()
            raise PositionUnreachable()




    def front_obstacle(self):
        # RoadMap.LEFT
        # RoadMap.RIGHT
        ((a,_),(b,_)) = self.sensors_front.get_normal(0)
        if a>350 and b>350:
            return
        print("LOG ", )
        print("LOG ", self.sensors_front.get_mesure())
        if self.goto_interrupt.is_set():
            return
        self.logger("MOVER : ", "Object in the front detected !")
        if not self.interupted_lock.acquire(blocking=True, timeout=0.5):
            self.logger("MOVER : ", "Abort !")
            return
        self.interupted_status.set()
        x, y, theta = self.wheeledbase.get_position()
        self.logger("MOVER : ", "Objet on the goal", hypot(y - self.goal[1], x - self.goal[0]))
        if hypot(y - self.goal[1], x - self.goal[0]) < 300:
            # Obstacle on the goal !
            self.wheeledbase.set_velocities(0, 0)
            try:
                self.sensors_front.wait(250, timeout=TIMEOUT_GOAL)
            except TimeoutError:
                self.goto_interrupt.set()

            self.interupted_status.clear()
            self.interupted_lock.release()

            return

        lin_wanted, ang_wanted = self.wheeledbase.get_velocities_wanted(True)
        if abs(ang_wanted) > 7:
            self.wheeledbase.set_velocities(copysign(150, -lin_wanted), copysign(1, ang_wanted))
            time.sleep(1)  # 0.5
            self.wheeledbase.set_velocities(copysign(150, lin_wanted), 0)
            time.sleep(1.2)
            self.wheeledbase.purepursuit(self.path)

        self.wheeledbase.stop()



            # Creation de l'obstacle
        x_obs = x
        y_obs = y
        height = 200
        x_obs += cos(theta) * 250
        y_obs += sin(theta) * 250
        obs = self.roadmap.create_temp_obstacle(
            ((-150, height), (-150, -height ), (150, -height ), (150, height)), timeout=TIMEOUT_OBSTACLE)
        obs.set_position(x_obs, y_obs, theta)
        old_path = self.path
        try:
            self.path = self.roadmap.get_shortest_path((x, y), self.goal)
            print(self.path)
            aim_theta= atan2(self.path[1][1]-self.path[0][1], self.path[1][0]-self.path[0][0])
            arrived = False
            while not arrived:
                try:
                    self.wheeledbase.turnonthespot(aim_theta)
                    self.wheeledbase.wait()
                    arrived = True
                except RuntimeError:
                    vel_wanted, _ = self.wheeledbase.get_velocities_wanted(True)
                    self.wheeledbase.stop()
                    self.wheeledbase.goto_delta(copysign(150,-vel_wanted),0)
                    sleep(0.5)
        except (RuntimeError,RuntimeWarning) as e:
            print(e)
            time.sleep(1)
        try:
            self.wheeledbase.purepursuit(self.path)
        except ValueError:
            self.path = old_path
            self.wheeledbase.purepursuit(self.path)
            time.sleep(1)

        self.logger("MOVER : ", "Fin de l'interruption avec isarrived = ", self.wheeledbase.isarrived())
        self.interupted_lock.release()
        self.interupted_status.clear()


    def goto_safe(self, x, y):

        self.goal = (x, y)
        self.path = self.roadmap.get_shortest_path(self.wheeledbase.get_position()[:2], self.goal)
        self.logger("MOVER : ", path=self.path)
        self.wheeledbase.max_linvel.set(300)
        self.wheeledbase.purepursuit(self.path)
        self.front_safe_flag.bind(self.sensors_front_listener.signal)
        self.isarrived = False
        while not self.isarrived or self.interupted_status.is_set():
            try:
                self.isarrived = self.wheeledbase.isarrived()
                sleep(0.1)
            except RuntimeError as e:
                print(e)
                self.logger("MOVER : ", "Spin ! We will wait ")
                if not self.interupted_lock.acquire(blocking=True, timeout=0.5):
                    continue
                self.wheeledbase.stop()
                sleep(5)
                self.wheeledbase.purepursuit(self.path)
                self.interupted_lock.release()
            except TimeoutError:
                self.isarrived = False

        self.reset()

    def front_obstacle_safe(self):
        x, y, _ = self.wheeledbase.get_position()
        if hypot(y-self.goal[1],x-self.goal[0])<70:
            return
        if not self.interupted_lock.acquire(blocking=True, timeout=0.5):
            return
        self.logger("MOVER : ", "Object in the front detected !")
        self.interupted_status.set()
        self.wheeledbase.set_velocities(0,0)
        self.logger("MOVER : ", "Wait....")
        self.sensors_front.wait(220, timeout=100)
        self.wheeledbase.purepursuit(self.path)
        self.interupted_status.clear()
        self.interupted_lock.release()
