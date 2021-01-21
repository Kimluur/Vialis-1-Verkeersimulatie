"""Extra functies voor pygame die we gemaakt hebben om leven makkelijker en mooier temaken."""
import pygame
from pygame.math import Vector2
import pandas as pd
import numpy as np
import math
import json
import pygame_textinput

def createAlphaRect(size, alpha, colour):
    """Maakt een rectangle die ook transparant kan zijn,
    de gewone draw van pygame kan dit niet.
    Vergeet deze niet te blitten naar het scherm!(comment voor example!)"""
    s = pygame.Surface(size)  # the size of your rect
    s.set_alpha(alpha)  # alpha level
    s.fill(colour)  # this fills the entire surface
    # after this use this is a blits:
    # windowSurface.blit(createalpharect(), (0, 0))  # (0,0) are the top-left coordinates
    return s


def aspect_scale(img, bx, by):
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio """
    ix, iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx / float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by / float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx / float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (int(sx), int(sy)))