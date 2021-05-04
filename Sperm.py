# This is the 'Sperm class file'
import Global_Variables as gv
import Sperm_Algorithms
import pygame as pg
import numpy as np
from scipy import stats
import time


class Sperm:

    # Sperm class constructor
    def __init__(self, sperm_size, sperm_turning_radius, sperm_turning_speed, sperm_turning_direction, sperm_max_speed,
                 sperm_pos, sperm_starting_angle, sperm_colour, sperm_algorithm):
        self.size = sperm_size
        self.turning_circle = sperm_turning_radius
        self.turning_speed = sperm_turning_speed
        # 0 is clockwise, 1 is counter-clockwise
        self.turning_direction = sperm_turning_direction
        self.max_speed = sperm_max_speed
        # pos is actually there centre of rotation
        self.centre = sperm_pos
        self.angle = sperm_starting_angle
        self.pos = [self.centre[0] + ((np.cos(np.deg2rad(self.angle)) * self.turning_circle) * gv.delta_time),
                    self.centre[1] + ((np.sin(np.deg2rad(self.angle)) * self.turning_circle) * gv.delta_time)]
        self.angluar_vel_vec = [self.turning_circle*(np.cos(np.deg2rad(self.angle+(self.turning_speed * gv.delta_time)))
                                                     - np.cos(np.deg2rad(self.angle))),
                                self.turning_circle*(np.sin(np.deg2rad(self.angle+(self.turning_speed * gv.delta_time)))
                                                     - np.sin(np.deg2rad(self.angle)))]
        self.colour = sperm_colour
        # 1 is the real time method, 2 is ear method
        self. algorithm = sperm_algorithm
        # units: pixels per second
        self.velocity = [0, 0]
        self.egg_found = False
        self.alive = True
        # imaging 1 sperm can remember one piece of concentration at a time
        self.memory = 0
        # record start and finsh time so that convergence time can be calculated
        self.start_time = time.time()
        self.fin_time = np.inf

    # updates the position of sperm
    def update(self, display):
        pg.draw.circle(display, self.colour, (int(self.pos[0]), int(self.pos[1])), self.size)

    # moves the sperm in a circle (I think this is wrong)
    def move(self):
        # if random direction then travel in stright line rather than in circles (like bacteria)
        if self.algorithm == 3:
            self.pos = self.centre

            self.centre[0] += self.velocity[0] * gv.delta_time
            self.centre[1] += self.velocity[1] * gv.delta_time

        # else if using any of the other algorithms then travel in circles
        else:
            # pos is the current position, velocity is how fast the centre of rotation is moving, centre is the centre
            # of rotation delta time is to make movement frame rate independent trigonometry produces tangential
            # velocity vector if direction is clockwise then do this
            self.pos = [self.centre[0] + (np.cos(np.deg2rad(self.angle)) * self.turning_circle),
                        self.centre[1] + (np.sin(np.deg2rad(self.angle)) * self.turning_circle)]

            # Reset the angle as doesnt change calculation but saves memory
            if abs(self.angle) >= 360:
                if not self.turning_direction:
                    self.angle -= 360

                else:
                    self.angle += 360

            # increment the centre of rotation by the velocity
            self.centre[0] += self.velocity[0] * gv.delta_time
            self.centre[1] += self.velocity[1] * gv.delta_time

            # increment the angle by the angluar speed
            if not self.turning_direction:
                self.angle += self.turning_speed * gv.delta_time

            else:
                self.angle -= self.turning_speed * gv.delta_time

            # re-calculate angular velocity vector for use in sperm algorithms (method 1)
            self.angluar_vel_vec = [
                self.turning_circle * (np.cos(np.deg2rad(self.angle + (self.turning_speed * gv.delta_time)))
                                       - np.cos(np.deg2rad(self.angle))),
                self.turning_circle * (np.sin(np.deg2rad(self.angle + (self.turning_speed * gv.delta_time)))
                                       - np.sin(np.deg2rad(self.angle)))]

    # if dead then do nothing
    def die(self):
        self.alive = False

    # perform the algorithm selected for sperm to use
    def do_algorithm(self, egg):

        if self.algorithm == 1:
            Sperm_Algorithms.real_time_method(self, egg)

        elif self.algorithm == 2:
            Sperm_Algorithms.ear_method(self, egg)

        elif self.algorithm == 3:
            Sperm_Algorithms.run_and_tumble(self)

        else:
            print("Invalid algorithm code! Dieing")
            self.die()

    # if egg found then change flag to true for statistic collection
    def egg_located(self):
        self.egg_found = True
        self.fin_time = time.time()

    # gets the concentration of chemical released by egg at current postion
    def get_concentration(self, egg):
        # mean is centre of distribution therefore at egg's current position
        concentration = stats.multivariate_normal.pdf(self.pos, egg.pos, gv.egg_dist_cov_matrix, allow_singular=True)
        # exadurate value to make them easier to compute
        return concentration

    def get_prev_pos(self):
        # Actually postion
        postion = [self.pos[0] + 0, self.pos[1] + 0]
        # Get centre of roatation position for clockwise rotation
        centre_rotation = [self.centre[0] + 0, self.centre[1] + 0]

        return postion, centre_rotation
