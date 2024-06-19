from config import *
import system
import pygame
from math import exp
from text import Text
import node
# from node import Node


class Edge:
    def __init__(self, nodeU: node.Node, nodeV: node.Node, directed = False, weight = None):
        self.screen = system.screen
        self.weight = weight
        self.directed = directed
        self.nodeU = nodeU
        self.nodeV = nodeV
        self.center = (self.nodeU.pos+self.nodeV.pos)/2

    def draw(self):
        posU = system.camera.pos_wolrd_to_screen(self.nodeU.pos)
        posV = system.camera.pos_wolrd_to_screen(self.nodeV.pos)
        pygame.draw.line(self.screen, "Gray", 
                posU, posV, width=4)
    
        if (self.weight):
            self.center = (self.nodeU.pos+self.nodeV.pos)/2
            pos = self.center.copy()
            pos.y -= 16
            text = Text(str(self.weight), 16, "White", center=pos)
            system.camera.draw_spirte(text)
