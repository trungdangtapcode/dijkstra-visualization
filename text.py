import pygame
from config import *
import system

class Font:
    """
    Provides a method for retrieving fonts.

    Methods:
        get_font(size): Returns a font object with the given size.
    """
    def get_font(size):
        path = PATH + 'font/slkscr.ttf'
        return pygame.font.Font(path, size)
    
class Text:
    """
    Represents a text object for rendering text on the screen.

    Attributes:
        image (Surface): Surface containing the rendered text.
        rect (Rect): Rectangular area representing the text position and size.

    Methods:
        None
    """
    def __init__(self, text, size, color = "Red", center = None, topleft = None):
        self.image = Font.get_font(size).render(text, False, color)
        if (center!=None):
            self.rect = self.image.get_rect(center = center)
        elif (topleft!=None):
            self.rect = self.image.get_rect(topleft = topleft)
        else: raise Exception("Dm topleft hay center")