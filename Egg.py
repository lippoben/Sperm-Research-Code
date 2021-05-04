# This is the Egg class file
import Global_Variables as gv
import pygame as pg


class Egg:

    # Egg constructor
    def __init__(self, egg_size, egg_pos):
        self.size = egg_size
        self.pos = egg_pos

    # updates the location of the egg
    def update(self, display):
        pg.draw.circle(display, gv.RED, (self.pos[0], self.pos[1]), self.size)

