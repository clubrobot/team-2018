#!/usr/bin/env python3
# coding: utf-8

from math import cos, sin, pi, hypot, copysign
from threading import *
import time
from statistics import mean

from common.sync_flag_signal import Flag
from robots.listener.position_listener import *
from robots.listener.sensor_listener import *
from beacons.balise_receiver import *
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
SENSORS_RANGE = 100
BACKWARD_VELOCITY = 150

# -  GOWALL
WALL_RANGE_TO_MOVE = 100
SENSORS_RANGE = 100


# <> ERROR <>
class PositionUnreachable(RuntimeError): pass


class Mover:
    AIM = 1
    SOFT = 2
    QUICK = 3
    SAFE = 4
    FAST = 5
    SIMPLE  = 6
    HARD   = 7

    def __init__(self, side, roadmap, arduinos, logger):  # , balise_receiver):

        # RoadMap et ses obstacles virtuel
        self.roadmap = roadmap
        self.logger = logger
        # self.obstacle_big = self.roadmap.create_obstacle(( (-200,-200),(200,-200),(200,120),(-200,200)   ))
        # self.obstacle_little = self.roadmap.create_obstacle(( (-90,-90),(90,-90),(90,90),(-90,90)   ))
        # self.obstacles_front = self.roadmap.create_temp_obstacle(((-100,150),(-100,-150),(100,-150),(100,150)),timeout = TIMEOUT_OBSTACLE)
        # self.obstacles_right= list()
        # Shape des obstacles
        # self.obstacles_left.append(self.roadmap.create_temp_obstacle(((-100,150),(-100,-150),(100,-150),(100,150)),timeout = TIMEOUT_OBSTACLE))
        # self.obstacles_right.append(self.roadmap.create_temp_obstacle(((-100,150),(-100,-150),(100,-150),(100,150)),timeout = TIMEOUT_OBSTACLE))
        # self.obstacles_left.append(self.roadmap.create_temp_obstacle(((-100,150),(-100,-150),(100,-150),(100,150)),timeout = TIMEOUT_OBSTACLE))
        # self.obstacles_right.append(self.roadmap.create_temp_obstacle(((-100,150),(-100,-150),(100,-150),(100,150)),timeout = TIMEOUT_OBSTACLE))
        # self.obstacles_left.append(self.roadmap.create_temp_obstacle(((-100,150),(-100,-150),(100,-150),(100,150)),timeout = TIMEOUT_OBSTACLE))
        # self.obstacles_right.append(self.roadmap.create_temp_obstacle(((-100,150),(-100,-150),(100,-150),(100,150)),timeout = TIMEOUT_OBSTACLE))

        # Arduino et autre
        self.wheeledbase = arduinos["wheeledbase"]
        self.sensors_front = arduinos["sensors_front"]
        self.sensors_lat = arduinos["sensors_lat"]
        self.sensors_back = arduinos["sensors_back"]
        self.side = side
        # self.balise  = BaliseReceiver("192.168.12.3")
        # try :
        #    self.balise.connect()
        #    self.balise.set_color(self.side)
        # except:
        #    pass

        # Object qui tcheck la position des robots adverse
        # self.big_listener  = PositionListener(lambda : self.balise.get_position(BIG_ROBOT),0.5)
        # self.little_listener  = PositionListener(lambda : self.balise.get_position(LITTLE_ROBOT),0.5)

        # Objet qui sont en relation avec les sensors
        self.sensors_front_listener = SensorListener(self.sensors_front.get_mesure)
        self.sensors_back_listener = SensorListener(self.sensors_back.get_mesure)
        # Flags relier a des fonctions interne pour tout bien gérer

        self.front_flag = Flag(self.front_obstacle)
        self.on_path_flag = Flag(self.on_path_obstacle)
        self.withdraw_flag = Flag(self._withdraw_interrup)


        # On connect les flags au signaux
        # self.on_path_flag.bind(self.big_listener.signal)
        # self.on_path_flag.bind(self.little_listener.signal)
        # self.front_flag.bind(self.sensors_listener.signal)

        self.path = list()
        self.isarrived = False
        self.interupted_lock = RLock()
        self.interupted_status = Event()
        self.interupted_timeout = Event()
        self.running = Event()
        self.direction = "forward"
        self.goal = (0, 0, 0)

    def get_enemy_status(self):
        return False

    # if( hypot(self.big_listener.position[0]-self.goal[0],self.big_listener.position[1]-self.goal[1])<ENEMY_RANGE):
    #    return True
    # return ( hypot(self.little_listener.position[0]-self.goal[0],self.little_listener.position[1]-self.goal[1])<ENEMY_RANGE)

    def get_wall_status(self, x, y):
        return (x < WALL_RANGE or (2000 - x) < WALL_RANGE or y < WALL_RANGE or (3000 - y) < WALL_RANGE)

    def gowall(self, try_limit=3, strategy=SAFE):
        #  /\ Determination de la proximité avec un enemies et initialisation des variables /\
        closed_to_enemy = self.get_enemy_status()
        self.goal = self.wheeledbase.get_position()
        if strategy == Mover.FAST: self._gowall_fast(try_limit)

    # Button activation
    def _gowall_fast(self, try_limit):
        wall_reached = False
        nb_try = try_limit
        while not wall_reached:
            try:
                self.wheeledbase.set_velocities(150, 0)
                while not self.wheeledbase.isarrived():
                    time.sleep(0.1)
            except RuntimeError:
                if not nb_try > 0: break
                nb_try -= 1
                if mean(self.sensors_front.get_mesure()) < 40:
                    wall_reached = True
                    print(self.sensors_front.get_mesure())
                else:
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
                                self.wheeledbase.set_velocities(-100, 0)
                                sleep(0.2)
                                self.wheeledbase.stop()
                        # Go backward
                        self.wheeledbase.set_velocities(-100, 0)
                        if ang < 0:
                            sleep(0.5)
                        else:
                            sleep(0.4)
                        self.wheeledbase.stop()
                        # TURN HARD
                        self.wheeledbase.set_velocities(0, copysign(6, -ang))
                        sleep(0.8)
                        self.wheeledbase.turnonthespot(self.goal[-1])
                        self.wheeledbase.wait()
                    else:
                        self.wheeledbase.set_velocities(200, -0)
                        sleep(0.2)
                        self.wheeledbase.stop()
                        self.wheeledbase.set_velocities(0, -6)
                        sleep(0.8)
                        self.wheeledbase.stop()
                        self.wheeledbase.turnonthespot(self.goal[-1])
                        self.wheeledbase.wait()


    def withdraw(self,x, y,direction="forward", strategy=SIMPLE):
        self.goal = (x,y)
        self.interupted_status.clear()
        self.interupted_timeout.clear()
        if strategy == Mover.SIMPLE: self._withdraw_simple(direction)
        if strategy == Mover.HARD: self._withdraw_hard(direction)

    def _withdraw_simple(self, direction):
        is_arrived = False
        self.wheeledbase.max_linvel.set(100)

        self.direction = direction
        if direction =="forward":
            print("lol")
            self.withdraw_flag.bind(self.sensors_front_listener.signal)
            self.sensors_front_listener.threadhold = 80
        else:
            print("lul")
            self.withdraw_flag.bind(self.sensors_back_listener.signal)
            self.sensors_back_listener.threadhold = 80
        while not is_arrived or self.interupted_status.is_set():

            try:
                if  self.interupted_status.is_set() :
                    sleep(0.2)
                else:
                    self.wheeledbase.goto(*self.goal, direction=direction)
                    is_arrived = True

            except RuntimeError:
                pass
        self.wheeledbase.max_linvel.set(800)
        self.withdraw_flag.clear()


    def _withdraw_hard(self, direction):
        is_arrived = False
        self.wheeledbase.max_linvel.set(100)

        self.direction = direction
        if direction =="forward":
            print("lol")
            self.withdraw_flag.bind(self.sensors_front_listener.signal)
            self.sensors_front_listener.threadhold = 80
        else:
            self.withdraw_flag.bind(self.sensors_back_listener.signal)
            self.sensors_back_listener.threadhold = 80
        while not is_arrived or self.interupted_status.is_set():

            try:
                if  self.interupted_status.is_set() :
                    sleep(0.2)
                else:
                    self.wheeledbase.goto(*self.goal, direction=direction)
                    is_arrived = True

            except RuntimeError:
                self.wheeledbase.stop()
                self.wheeledbase.set_velocities( -100 if self.direction =="forward" else 100,0)
                time.sleep(0.5)
                self.wheeledbase.stop()

        self.wheeledbase.max_linvel.set(800)
        self.withdraw_flag.clear()



    def _withdraw_interrup(self):

        if self.interupted_timeout.is_set() : return
        if not self.interupted_lock.acquire(blocking=False): return
        self.interupted_status.set()
        print("INTERRUPT")
        self.wheeledbase.stop()
        initial_time = time.time()
        sensors = self.sensors_front if self.direction == "forward" else self.sensors_back
        mesure  = sensors.get_mesure()
        print( min(*mesure)<80)
        while min(*mesure)<80 and  (time.time()- initial_time)<5 :
            time.sleep(0.4)
            print((time.time()- initial_time))
            mesure = sensors.get_mesure()
        if min(*mesure)<80:
            self.interupted_timeout.set()
            self.withdraw_flag.clear()
            self.wheeledbase.max_linvel.set(100)

        self.interupted_status.clear()
        self.interupted_lock.release()





    def turnonthespot(self, angle, try_limit=3, stategy=AIM):
        self.running.set()
        self.goal = (*self.wheeledbase.get_position()[:-1], angle)
        if stategy == Mover.AIM: self._turnonthespot_aim(try_limit)
        if stategy == Mover.SOFT: self._turnonthespot_soft(try_limit)

    def _turnonthespot_soft(self, try_limit):
        try_number = 0
        way = 'forward'
        closed_to_wall = self.get_wall_status(*self.goal[:-1])  # Boolean qui représente la proximité à un cube
        closed_to_enemy = True  # self.get_enemy_status() # Boolean qui représente la proximité à un enemie
        position_reach = False
        x, y = self.goal[:-1]
        while not position_reach and (try_limit + 1) >= try_number:
            print(try_number)
            try:
                self.wheeledbase.turnonthespot(self.goal[2], direction=way)
                self.wheeledbase.wait()
                position_reach = True
            except RuntimeError:
                _, ang_vel = self.wheeledbase.get_velocities_wanted()
                std = 0.0
                var = 0.0
                # /\ récupéré les données des balises de devant /\
                if ang_vel > 0: std_f, _ = self.sensors_front.get_normal(0)[1]
                if ang_vel < 0: std_f, _ = self.sensors_front.get_normal(0)[0]
                # /\ récupéré les données des balises de derriere /\
                if ang_vel > 0: std_b, _ = self.sensors_back.get_normal(0)[1]
                if ang_vel < 0: std_b, _ = self.sensors_back.get_normal(0)[1]
                # /\ récupéré les données des balises des côtés /\
                std_l, _ = self.sensors_lat.get_normal(2)[1]
                std_r, _ = self.sensors_back.get_normal(2)[0]
                print(std_f)
                # <> Premiere essaie <>
                if (try_number == 0):
                    if (closed_to_enemy and (std_f < SENSORS_RANGE or std_b < SENSORS_RANGE)):
                        self.wheeledbase.max_angvel.set(1.5)
                        if (std_f < SENSORS_RANGE):
                            self.sensors_front.wait(SENSORS_RANGE, 2)
                        else:
                            self.sensors_back.wait(SENSORS_RANGE, 2)
                        try_number += 1
                        continue

                    self.wheeledbase.max_angvel.set(2)
                    try_number += 1
                    continue
                if (try_number == 1):
                    # On ne regarde pas les enemies on change juste de sens
                    way = {'forward': 'backward', 'backward': 'forward'}[way]
                    try_number += 1
                    continue
                if (try_number == 2):
                    # On regarde les enemies et si c'est bien ce probleme on attend un peu sinon on change de sens
                    if (closed_to_enemy and (std_f < SENSORS_RANGE or std_b < SENSORS_RANGE)):
                        self.wheeledbase.max_angvel.set(1.5)
                        if (std_f < SENSORS_RANGE):
                            self.sensors_front.wait(SENSORS_RANGE, 1.5)
                        else:
                            self.sensors_back.wait(SENSORS_RANGE, 1.5)
                        try_number += 1
                        continue

                    way = {'forward': 'backward', 'backward': 'forward'}[way]
                    try_number += 1
                    continue
                if (try_number == 3):
                    break

        self.wheeledbase.max_angvel.set(6)
        if (not position_reach):
            raise PositionUnreachable()

    def _turnonthespot_aim(self, try_limit):

        initial_try_number = try_limit
        way = 'forward'
        closed_to_wall = self.get_wall_status(*self.goal[:-1])  # Boolean qui représente la proximité à un cube
        closed_to_enemy = self.get_enemy_status()  # Boolean qui représente la proximité à un enemie
        position_reach = False
        x, y = self.goal[:-1]
        while not position_reach and try_limit > 0:
            try:
                self.wheeledbase.turnonthespot(self.goal[2], direction=way)
                self.wheeledbase.wait()
                position_reach = True
            except RuntimeError:
                self.wheeledbase.stop()

                _, ang_vel = self.wheeledbase.get_velocities_wanted()
                # /\ récupéré les données des balises de devant /\
                if ang_vel > 0: std_f, _ = self.sensors_front.get_normal(2)[0]
                if ang_vel < 0: std_f, _ = self.sensors_front.get_normal(2)[1]
                # /\ récupéré les données des balises de derriere /\
                if ang_vel > 0: std_b, _ = self.sensors_back.get_normal(2)[1]
                if ang_vel < 0: std_b, _ = self.sensors_back.get_normal(2)[1]
                # /\ récupéré les données des balises des côtés /\
                std_l, _ = self.sensors_lat.get_normal(2)[1]
                std_r, _ = self.sensors_back.get_normal(2)[0]

                # /\ Première étude de la situation /\
                if (initial_try_number == try_limit):
                    self.wheeledbase.max_angvel.set(3)
                    # <> Si on a des enemi à côté, on vérifie leur présence et on ralenti
                    if (closed_to_enemy or std_f < SENSORS_RANGE or std_b < SENSORS_RANGE):
                        self.wheeledbase.max_angvel.set(0.4)
                        if (std_b < SENSORS_RANGE):
                            self.wheeledbase.stop()
                            self.wheeledbase.set_velocities(ang_vel / abs(ang_vel) * 150, 0)
                            time.sleep(0.4)
                            self.wheeledbase.stop()
                            try_limit -= 1
                            continue

                        if (std_f < SENSORS_RANGE or True):
                            self.wheeledbase.stop()
                            self.wheeledbase.set_velocities(-ang_vel / abs(ang_vel) * BACKWARD_VELOCITY, 0)
                            time.sleep(0.4)
                            self.wheeledbase.stop()
                            try_limit -= 1
                            continue
                    # <> Eloignement du mur si nécessaire <>
                    if (closed_to_wall):
                        self.wheeledbase.set_velocities(-ang_vel / abs(ang_vel) * BACKWARD_VELOCITY, 0)
                        time.sleep(0.4)
                        self.wheeledbase.stop()
                        try_limit -= 1
                        continue

                # Les autres cas
                if (std_f < SENSORS_RANGE):
                    self.wheeledbase.set_velocities(-ang_vel / abs(ang_vel) * BACKWARD_VELOCITY, 0)
                    time.sleep(0.4)
                    self.wheeledbase.stop()
                    try_limit -= 1
                    continue
                if (std_b < SENSORS_RANGE):
                    self.wheeledbase.set_velocities(ang_vel / abs(ang_vel) * BACKWARD_VELOCITY, 0)
                    time.sleep(0.4)
                    self.wheeledbase.stop()
                    try_limit -= 1
                    continue
                else:
                    way = {'forward': 'backward', 'backward': 'forward'}[way]
                    try_limit -= 1
                    continue

        self.wheeledbase.max_angvel.set(6)
        if (not position_reach):
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
                if not self.interupted_lock.acquire(blocking=True, timeout=1):
                    continue
                # Si tu n'est pas a coté d'un enemie
                # TODO
                if not self.get_enemy_status():
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
                pass

        # self.on_path_flag.clear()
        self.front_flag.clear()

    def front_obstacle(self):
        # RoadMap.LEFT
        # RoadMap.RIGHT

        self.logger("MOVER : ", "Object in the front detected !")
        if not self.interupted_lock.acquire(blocking=True, timeout=1):
            return
        x, y, theta = self.wheeledbase.get_position()
        if (hypot(y - self.goal[1], x - self.goal[0]) < 300):
            self.interupted_status.clear()
            self.interupted_lock.release()
            return
        self.interupted_status.set()
        lin_wanted, ang_wanted = self.wheeledbase.get_velocities_wanted()
        if (abs(ang_wanted) > 7):
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
        while (True):
            try:
                self.wheeledbase.turnonthespot(theta - pi / 2)

                self.wheeledbase.wait()
                break
            except:
                self.wheeledbase.stop()
                # PROBLEME
                self.wheeledbase.set_velocities(-200, 0)
                time.sleep(0.4)
                self.wheeledbase.stop()
                continue

        blocking = True
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
                time.sleep(0.3)
            except:
                side *= -1
                self.wheeledbase.set_velocities(-100 * side, 0)
        time.sleep(0.5)
        self.wheeledbase.stop()
        x_p, y_p, theta_p = self.wheeledbase.get_position()
        self.wheeledbase.turnonthespot(theta)
        try:
            self.wheeledbase.wait()
        except:
            return
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
        try:
            self.wheeledbase.purepursuit(self.path)
        except ValueError:
            pass  # TODO
        self.interupted_status.clear()
        self.interupted_lock.release()

    def on_path_obstacle(self):
        self.obstacle_big.set_position(*self.balise.get_position(BIG_ROBOT))
        self.obstacle_little.set_position(*self.balise.get_position(LITTLE_ROBOT))
        if not self.interupted_lock.acquire():
            return
        new_path = self.roadmap.get_shortest_path(self.path[0], self.goal)
        if (new_path != self.path):
            self.path = new_path
            self.wheeledbase.purepursuit(self.path)
        self.interupted_lock.release()
