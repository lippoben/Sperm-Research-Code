# File containing simulation inisilistation functions
import Global_Variables as gv
import Sperm
import Egg
import random
from scipy import stats


# generate a requested number of sperm in random postions at random points on their circular path
def sperm_generate(sperm_num, sperm_tracked):

    # define array to return will conatin all the objects of sperms generated
    sperm_array = []

    # generate the number of sperm requested at random locations and angle on circle within the display
    for i in range(0, sperm_num - sperm_tracked):
        sperm_start_pos = [random.randint(0, gv.display_width), random.randint(0, gv.display_height)]
        sperm_start_angle = random.uniform(0, 360)
        sperm_array.append(Sperm.Sperm(gv.sperm_radius, gv.sperm_turning_radius, gv.sperm_turning_speed,
                                       random.randint(0, 1), gv.sperm_top_speed, sperm_start_pos, sperm_start_angle,
                                       gv.WHITE, gv.sperm_method))

    # generate sperm of a different colour so that its motion can be tracked more easily
    for x in range(0, sperm_tracked):
        sperm_start_pos = [random.randint(0, gv.display_width), random.randint(0, gv.display_height)]
        sperm_start_angle = random.uniform(0, 360)
        sperm_array.append(Sperm.Sperm(gv.sperm_radius, gv.sperm_turning_radius, gv.sperm_turning_speed,
                                       random.randint(0, 1), gv.sperm_top_speed, sperm_start_pos, sperm_start_angle,
                                       gv.GREEN, gv.sperm_method))

    return sperm_array


# generate a random position for the egg to be
def egg_generate(egg_size):

    egg_start_pos = [random.randint(0, gv.display_width), random.randint(0, gv.display_height)]
    # egg_start_pos = [int(gv.display_width/2), int(gv.display_height/2)]
    return Egg.Egg(egg_size, egg_start_pos)

