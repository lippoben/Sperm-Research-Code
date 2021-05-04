# This file contains the algorithm the sperm uses the find the egg.
import numpy as np
import Global_Variables as gv
import time
import random


# constantly compares current concentration to one tick previously
# if the concentration is greater than previous increase Offset in current direction
# if the concentration is less than than previous increase Offset in opposite direction
def real_time_method(sperm, egg):

    # if noting in memory ie equal to 0 then record concentration
    if not sperm.memory:
        sperm.memory = sperm.get_concentration(egg)

    # if there is a concentraiton in memory then sperm has moved therefore calculate difference in concentration and
    # change velocity accordiingly
    elif sperm.memory != 0:
        # calculate difference between current position and old position
        concentration_gradient = sperm.get_concentration(egg) - sperm.memory

        # if sperm have 1 sensitivity then make the concentration gradient 1 so that it's term doesn't effect sperms
        # motion
        if not gv.sperm_sensitivity:
            concentration_gradient = 1

        # else apply sensitivty constant
        else:
            concentration_gradient *= gv.sperm_sensitivity

        # if the motion of sperm is anti clockwise then reverse vector else sperm will diverge from egg rather than
        # converge
        if sperm.turning_direction:
            sperm.angluar_vel_vec = [sperm.angluar_vel_vec[0] * -1, sperm.angluar_vel_vec[1] * -1]

        # if greater than increase velocity in current direction
        if concentration_gradient > 0:
            # if the new velocity's magnitude is less than the max speed of sperm then procceed with calculation else
            # hold current trejectory

            # check max speed is not exceeded in either i or j direction if not then increment velcity.
            # weighting the increments size based on read gradient
            if (abs(sperm.velocity[0] + (sperm.angluar_vel_vec[0] * concentration_gradient * gv.delta_time)) <
                    sperm.max_speed):

                sperm.velocity[0] += (sperm.angluar_vel_vec[0] * concentration_gradient * gv.delta_time)

            if (abs(sperm.velocity[1] + (sperm.angluar_vel_vec[1] * concentration_gradient * gv.delta_time)) <
                    sperm.max_speed):

                sperm.velocity[1] += (sperm.angluar_vel_vec[1] * concentration_gradient * gv.delta_time)

        # if negative gradient then increase velocity in opposite direction
        elif concentration_gradient < 0:
            # if the new velocity's magnitude is less than the max speed of sperm then procceed with calculation else
            # hold current trejectory

            # inverse gradient value else when applying the weighting the sign of angular velocity vector will change
            # causing the sperm to diverge
            concentration_gradient *= -1

            # check max speed is not exceeded in either i or j direction if not then increment velcity.
            # weighting the increments size based on read gradient
            if (abs(sperm.velocity[0] - (sperm.angluar_vel_vec[0] * concentration_gradient * gv.delta_time)) <
                    sperm.max_speed):

                sperm.velocity[0] -= sperm.angluar_vel_vec[0] * concentration_gradient * gv.delta_time

            if (abs(sperm.velocity[1] - (sperm.angluar_vel_vec[1] * concentration_gradient * gv.delta_time)) <
                    sperm.max_speed):

                sperm.velocity[1] -= (sperm.angluar_vel_vec[1] * concentration_gradient * gv.delta_time)

        # clear memory
        sperm.memory = 0


# take the concentration of two points, each on opposite sides of circular path, calculate the difference then move in
# direction of positive difference or move in opposite direciton of negative difference
def ear_method(sperm, egg):

    # if noting in memory ie equal to 0 then record concentration and current angle
    if not sperm.memory:
        sperm.memory = [sperm.get_concentration(egg), sperm.angle + 0]

    # if there is a concentraiton in memory therefore sperm has moved and difference between recorded angle and current
    # angle degrees is greater than 180 therefore sperm now on opposite side of circular path so calculate diffrence and
    # move centre of rotation in direction of postive trend
    elif sperm.memory[0] != 0 and abs(sperm.angle - sperm.memory[1]) >= 180:
        # calculate concentration gradient between current postion and previously recorded position
        concentration_gradient = sperm.get_concentration(egg) - sperm.memory[0]
        # calculate unit vector from centre to current postion
        velocity_vector = [np.cos(np.deg2rad(sperm.angle)), np.sin(np.deg2rad(sperm.angle))]

        # give lots of information about tracked sperm just uncomment for info. Best observed with one tracked sperm
        # if sperm.colour == gv.GREEN:
        #    print("\nmy current centre of rotation is: ", sperm.centre)
        #    print("my current angle is: ", sperm.angle)
        #    print("my current concentration gradient and recorded angle are: ", sperm.memory)
        #    print("my current velocity vector is: ", velocity_vector)
        #    print("current angle step: ", gv.delta_time * sperm.turning_speed)
        #    print("my turning direction: ", sperm.turning_direction)
        #    print("My velocity is: ", sperm.velocity)

        # if sperm have 0 sensitivity then make the concentration gradient 1 so that it's term doesn't effect sperms
        # motion
        if not gv.sperm_sensitivity:
            concentration_gradient = 1

        # else apply sensitivty constant
        else:
            concentration_gradient *= gv.sperm_sensitivity

        # if gradient is positive then apply a velocity vector in direction of gradient
        if concentration_gradient > 0:
            if abs(sperm.velocity[0] + (velocity_vector[0] * concentration_gradient * gv.delta_time)) < sperm.max_speed:
                sperm.velocity[0] += velocity_vector[0] * concentration_gradient * gv.delta_time

            if abs(sperm.velocity[1] + (velocity_vector[1] * concentration_gradient * gv.delta_time)) < sperm.max_speed:
                sperm.velocity[1] += velocity_vector[1] * concentration_gradient * gv.delta_time

        # if gradient is negative then apply a velocity vector in opposite direction to gradient
        elif concentration_gradient < 0:
            # stops the concentration gradient changing the sign of vector direction
            concentration_gradient *= -1

            # if gradient is positive then apply a velocity vector in opposite direction of gradient
            if abs(sperm.velocity[0] - (velocity_vector[0] * concentration_gradient * gv.delta_time)) < sperm.max_speed:
                sperm.velocity[0] -= velocity_vector[0] * concentration_gradient * gv.delta_time

            if abs(sperm.velocity[1] - (velocity_vector[1] * concentration_gradient * gv.delta_time)) < sperm.max_speed:
                sperm.velocity[1] -= velocity_vector[1] * concentration_gradient * gv.delta_time

        # clear memory
        sperm.memory = 0


# sperm picks a random direction and acclerates in that direction for x seconds then stops anc picks a new
# random direction.
def run_and_tumble(sperm):
    # if sperm has nothing in memory then record current time and pick direction
    if not sperm.memory:
        random_angle = random.uniform(0, 360)
        random_stop_time = random.randint(0, 5)
        sperm.memory = [time.time(),
                        [np.cos(np.deg2rad(random_angle)), np.sin(np.deg2rad(random_angle))],
                        random_stop_time]

    # travel in a direction for a random number of seconds
    if time.time() - sperm.memory[0] < sperm.memory[2]:
        sperm.velocity[0] = sperm.memory[1][0] * sperm.max_speed
        sperm.velocity[1] = sperm.memory[1][1] * sperm.max_speed

    # else time is up so clear memory
    else:
        sperm.memory = 0
