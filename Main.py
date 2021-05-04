# This is the main run file

import multiprocessing
import Global_Variables as gv
import Sim_Init
import pygame as pg


# define Main as a function for multiprocessing
def main(egg_obj, sperm_population_objs):
    import time
    import numpy as np
    import Statistics
    # inislise the pygame function
    pg.init()
    timer_font = pg.font.SysFont('Comic Sans MS', 30)
    display = pg.display.set_mode((gv.display_width, gv.display_height))
    pg.display.set_caption('Sperm Simulation')
    clock = pg.time.Clock()

    # interate thought sperm and check for any sperm that have spawned on the egg_obj if so remove them from simulation
    for current_sperm in sperm_population_objs:
        # check for collisions with egg_obj if any exist then remove sperm from simulation
        if (np.sqrt(np.square(current_sperm.pos[1] - egg_obj.pos[1]) + np.square(current_sperm.pos[0] - egg_obj.pos[0]))
                <= (current_sperm.size + egg_obj.size)):

            sperm_population_objs.remove(current_sperm)
            print("collision detected removing sperm")

    print("New sperm test population: ", len(sperm_population_objs), "\n")

    # halt the program and wait for user to press space to start simulation
    while not gv.sim_start and not gv.simulationRunning:
        tick_start = time.time()
        # check for key board and mouse inputs from user
        for event in pg.event.get():
            # if red X is pressed then end program
            if event.type == pg.QUIT:
                gv.sim_start = True
                gv.simulationRunning = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    gv.sim_start = True
                    gv.simulationRunning = True
                    # Record the start time for 2 min timer to function
                    start_time = time.time()
                    five_sec_timer = time.time()

        # draw everything to screen
        display.fill(gv.BLACK)
        egg_obj.update(display)
        for positions in gv.sperm_prev_pos_array:
            pg.draw.circle(display, gv.YELLOW, (int(positions[0]), int(positions[1])), 1)
        for positions in gv.sperm_prev_cor_pos_array:
            pg.draw.circle(display, gv.BLUE, (int(positions[0]), int(positions[1])), 1)
        for current_sperm in sperm_population_objs:
            current_sperm.update(display)

        # Render everything drawn to the display
        pg.display.update()
        clock.tick(gv.frameRate)
        gv.delta_time = time.time() - tick_start

    # Main update loop
    while gv.simulationRunning:
        tick_start = time.time()
        # check for any keyboard or mouse inputs
        for event in pg.event.get():
            # if simulation cancelled and red X is pressed then close window and end program
            if event.type == pg.QUIT and gv.sim_fin:
                gv.simulationRunning = False
            # if the red X is pressed and simulation is running then cancel simulation but dont close window
            elif event.type == pg.QUIT and not gv.sim_fin:
                print("Sim Canceled\n")
                gv.sim_fin = True

        # Fill entire display eg background
        display.fill(gv.BLACK)

        # draw egg_obj
        egg_obj.update(display)

        # calculate mean postion of all sperm append them to array and plot all calculated mean postions
        gv.sperms_mean_pos[0] /= (len(sperm_population_objs))
        gv.sperms_mean_pos[1] /= (len(sperm_population_objs))
        gv.sperms_prev_mean_array.append(gv.sperms_mean_pos)
        gv.sperms_mean_pos = [0, 0]
        for positions in gv.sperms_prev_mean_array:
            pg.draw.circle(display, gv.LIGHT_BLUE, (int(positions[0]), int(positions[1])), 1)

        # draw a series of small dots at each recorded position of sperm to create a tracking effect
        for positions in gv.sperm_prev_pos_array:
            pg.draw.circle(display, gv.YELLOW, (int(positions[0]), int(positions[1])), 1)

        # draw a series of small dots at each recoreded position of sperm's centre of rotation postion to create a
        # tracking effect
        for positions in gv.sperm_prev_cor_pos_array:
            pg.draw.circle(display, gv.BLUE, (int(positions[0]), int(positions[1])), 1)

        # once 5 seconds has passed then print some stats
        if ((time.time() - five_sec_timer) > 5) and not gv.sim_fin:

            for current_sperm in sperm_population_objs:

                if not current_sperm.egg_found:
                    gv.failed_sperm_count += 1

            five_sec_timer = time.time()
            Statistics.live_stats(len(sperm_population_objs), start_time)
            gv.failed_sperm_count = 0

        # check difference between now and the start time if it is greater than the wait time then time is up
        if ((time.time() - start_time) > gv.end_time) or gv.sim_fin:
            gv.sim_fin = True
            gv.failed_sperm_count = 0
            # counts failed sperm for statistic collection and displays sperm
            for current_sperm in sperm_population_objs:

                if not current_sperm.egg_found and not gv.stats_calculated:
                    gv.failed_sperm_count += 1
                    current_sperm.die()

                # draw sperm to surface
                current_sperm.update(display)

            # ensures that end statistics are only calculated once
            if not gv.stats_calculated:
                Statistics.statistics(len(sperm_population_objs), start_time, fin_time, sperm_population_objs)
                gv.stats_calculated = True

        else:
            # compute every sperm's actions
            for current_sperm in sperm_population_objs:

                # if the sperm is dead or fround the egg_obj then just draw to surface no calculations required
                if not current_sperm.alive or current_sperm.egg_found:
                    # if all the sperm have completed there movements then end simulation and collect statistics
                    gv.sperm_fin += 1
                    if gv.sperm_fin == len(sperm_population_objs):
                        gv.sim_fin = True

                # if the distance from the centre of the sperm to the centre of the segg is less than or equal to the
                # sum of the egg_obj's and the sperm's radii then the two have collided therefore the egg_obj is found.
                elif (np.sqrt(np.square(current_sperm.pos[1] - egg_obj.pos[1]) + np.square(current_sperm.pos[0] -
                                                                                           egg_obj.pos[0])) <=
                      (current_sperm.size + egg_obj.size)):

                    current_sperm.egg_located()

                # else still looking for the egg_obj so keep swimming :)
                elif current_sperm.alive:
                    # get the position of the centre of rotation and actual position
                    # of the tracked sperm and store in arrays to be drawn later
                    if current_sperm.colour == gv.GREEN:
                        tracked_positions = current_sperm.get_prev_pos()
                        gv.sperm_prev_pos_array.append(tracked_positions[0])
                        gv.sperm_prev_cor_pos_array.append(tracked_positions[1])

                    # move the sperm
                    current_sperm.move()
                    # apply the specified egg search algorithm
                    current_sperm.do_algorithm(egg_obj)

                gv.sperms_mean_pos[0] += current_sperm.pos[0]
                gv.sperms_mean_pos[1] += current_sperm.pos[1]

                # draw sperm to surface
                current_sperm.update(display)

        # Render timer and blit to surface
        if gv.sim_fin:
            timer_surface = timer_font.render(str(fin_time), False, gv.WHITE)
            display.blit(timer_surface, (5, 0))

        else:
            timer_surface = timer_font.render(str(round(time.time() - start_time, 3)), False, gv.WHITE)
            display.blit(timer_surface, (5, 0))
            fin_time = round(time.time() - start_time, 3)

        # Render everything drawn to the display
        pg.display.update()
        clock.tick(gv.frameRate)
        # calculate delta time to make everything in simulation frame-rate independent
        gv.delta_time = time.time() - tick_start
        # reset finish sperm counter
        gv.sperm_fin = 0

    print("\nFin")
    pg.quit()
    quit()


# illustrates a multivariate distribution on a 3D graph
def distribution_plotter(egg_obj, display_width, display_height):
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats
    from mpl_toolkits.mplot3d import Axes3D

    # Create grid and multivariate normal
    x = np.linspace(0, display_width, 500)
    y = np.linspace(0, display_height, 500)
    mesh_x, mesh_y = np.meshgrid(x, y)
    pos = np.empty(mesh_x.shape + (2,))
    pos[:, :, 0] = mesh_x
    pos[:, :, 1] = mesh_y
    mv = stats.multivariate_normal(egg_obj.pos, gv.egg_dist_cov_matrix)

    # Make Plot
    fig = plt.figure()
    axes = fig.gca(projection='3d')
    axes.invert_yaxis()
    axes.plot_surface(mesh_x, mesh_y, mv.pdf(pos), cmap='viridis', linewidth=0)
    axes.set_xlabel('X axes')
    axes.set_ylabel('Y axes')
    axes.set_zlabel('Z axes')
    axes.set_title('Guassian Distribution of egg Chemicals')
    plt.show()


if __name__ == '__main__':
    # generate egg_obj
    egg = Sim_Init.egg_generate(gv.egg_radius)
    # generates all the sperm
    sperm_population = Sim_Init.sperm_generate(gv.sperm_pop, gv.sperm_tracked)

    # compute the graph and simulation in parallel so that both keep their functionality during program run time.
    p_plt = multiprocessing.Process(target=distribution_plotter,
                                    args=[egg, gv.display_width, gv.display_height])
    p_main = multiprocessing.Process(target=main, args=[egg, sperm_population])

    p_main.start()
    p_plt.start()
