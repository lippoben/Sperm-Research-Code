# Bank of all Global Variables

import numpy as np

# Custom baked files

# Scale
# If each sperm is 4 pixel big. The average size of a spermazoa head is 5.1 by 3.1 micro metres.
# thats approxmiatly 15 micro-metre squared in area therefore by calling the sperm head a square each pixel
# is the equivlilent of a 1.85 by 1.85 micro-metre square.


# Bank of colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (30, 144, 255)
YELLOW = (255, 255, 0)

# pygame stuff
# 900 by 1400 is test enviroment size
display_height = 900
display_width = 1400
# boolean flag to keep simulation running
simulationRunning = False
sim_start = False
sim_fin = False
sperm_fin = 0
frameRate = 100


# Bank of egg properties
# pixels
egg_radius = 50
# Generates a normal distribution from centre of egg to cover entire display
egg_dist_cov_matrix = np.array([[np.square(display_width/3), 0], [0, np.square(display_height/3)]])


# Bank of sperm properties
sperm_pop = 300
sperm_tracked = 1
# each pixel = 1.875 micro-metres
sperm_radius = 2
# Units: Degrees per second scale number is 396
sperm_turning_speed = 396
# Units: 1.875 micro-metres per second scale number is 13
sperm_turning_radius = 13
# units: 1.875 micro-metres per second scale number is 50 as the modulus of a vector(50,50) is 70
sperm_top_speed = 50
# sperms sensitivity to chemical concentration, 0 sensitivity means concentration is not taken into account when appling
# velocity.
# N.B sensitivity 10**10 is perfect for real time method (1) and scale values
# N.B sensitivity 10**10 is perfect for ear method (2) and scale values
sperm_sensitivity = 10**10
# select the sperms algorithm
# 1 is real time method, 2 is ear method, 3 is run and tumble
sperm_method = 1


# Interesting patterns:
# r = 2, pop = 3, turn speed = 396, turn r = 4, top speed = 200, sens = 10**11
# r = 2, pop = 1, turn speed = 396, turn r = 13, top_speed = 15, sens = 10**9

# sperm tracking
sperm_prev_pos_array = []
sperm_prev_cor_pos_array = []
# mean position of all sperm
sperms_mean_pos = [0, 0]
sperms_prev_mean_array = []


# Timer stuff
# units: seconds
end_time = 120
delta_time = 0

# Data Collection
stats_calculated = False
failed_sperm_count = 0
