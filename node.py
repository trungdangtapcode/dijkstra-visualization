from __future__ import annotations
from config import *
import system
import pygame
from math import exp
from text import Text
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from edge import Edge

class Node(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, 
            groups: pygame.sprite.Group, 
            label = 'x',
            zindex = 0):
        super().__init__(groups)
        self.zindex = zindex
        self.type = 'node'
        self.image = pygame.surface.Surface(NODE_SIZE, pygame.SRCALPHA).convert_alpha()
        self.size = pygame.math.Vector2(NODE_SIZE)
        self.radius = self.size[0]/2
        pygame.draw.circle(self.image, RED, self.size/2, self.radius)       
        self.rect = self.image.get_rect(center = pos)
        self.__pos = pygame.math.Vector2(pos)
        self.is_drag = False
        self.drag_shift = pygame.math.Vector2(0,0)

        self.veclocity = pygame.math.Vector2(0,-100)
        self.last_pressed = False
        self.veclocity_decay = 0.5 #cycle

        self.force_push_dist_limit = 200
        self.force_push_scale = 10**5
        self.force_push_max = 100
        self.force_pull_dist_limit = 200
        self.force_pull_scale = 5*10**-3
        self.force_pull_max = 100

        self.connected_nodes = []
        self.adj = []
        self.text_sprite = Text(str(label), 32, "Green", center = self.size/2)
        self.text_sprite_hightlighted = Text(str(label), 32, "Blue", center = self.size/2)
        self.is_hightlight1 = False
        self.is_hightlight2 = False

        self.frame_image = pygame.surface.Surface(NODE_SIZE, pygame.SRCALPHA).convert_alpha()
        pygame.draw.circle(self.frame_image, RED, self.size/2, self.radius)     
        pygame.draw.circle(self.frame_image, WHITE, self.size/2, self.radius/4*3)     
        self.frame_image.set_colorkey(WHITE)

    @property
    def pos(self):
        return self.__pos
    @pos.setter
    def pos(self, new_pos):
        new_pos = pygame.math.Vector2(new_pos)
        self.rect.center = new_pos
        self.__pos = new_pos
    
    def add_forces(self, acc):
        self.veclocity += acc

    def is_hover(self):
        mouse_pos = system.camera.get_mouse_world_pos()
        return ((mouse_pos-self.pos).magnitude()<=self.radius)
    
    def connect_node(self, node:Node = None, edge: Edge = None):
        assert edge
        if node:
            assert node==edge.nodeU or node==edge.nodeV

        if node==None:
            node = edge.nodeU if edge.nodeU != self else edge.nodeV
        self.connected_nodes.append(node)
        self.adj.append(edge)

    def update(self):
        self.update_color()

        mouse = pygame.mouse
        new_is_drag = self.is_drag or self.is_hover() \
            and mouse.get_pressed()[0] and not self.last_pressed
        if (not mouse.get_pressed()[0]): new_is_drag = False
        self.last_pressed = mouse.get_pressed()[0]

        #start holding
        if (new_is_drag and not self.is_drag):
            mouse_pos = system.camera.get_mouse_world_pos()
            self.drag_shift = mouse_pos-self.pos
        
        self.is_drag = new_is_drag
        
        #maintain holding
        if (self.is_drag):
            mouse_pos = system.camera.get_mouse_world_pos()
            self.pos = mouse_pos - self.drag_shift

        self.update_force()
    
    def update_force(self):
        self.veclocity *= exp(-system.delta_time/self.veclocity_decay)
        if (self.is_drag): return
        self.pos += self.veclocity*system.delta_time
        for node in system.graph.nodes:
            if (node==self): continue

            #push
            vec = (self.pos - node.pos)
            if (vec.magnitude()<=self.force_push_dist_limit): 
                dist2 = vec.magnitude()**2
                force = vec.normalize()*\
                    min(self.force_push_scale/(dist2+10**-6), self.force_push_max)
                self.add_forces(force)

        for node in self.connected_nodes:
            #pull
            vec = node.pos - self.pos
            if (vec.magnitude()>=self.force_pull_dist_limit):
                dist2 = vec.magnitude()**2
                force = vec.normalize()\
                    *min(self.force_pull_scale*dist2,self.force_pull_max)
                self.add_forces(force)

    def hightlight1(self):
        self.is_hightlight1 = True
    def unhightlight1(self):
        self.is_hightlight1 = False
    
    def hightlight2(self):
        self.is_hightlight2 = True
    def unhightlight2(self):
        self.is_hightlight2 = False

    def update_color(self):
        mouse = pygame.mouse

        change_color = self.is_hover() or self.is_drag
        if (self.is_hover() and  mouse.get_pressed()[0] and not self.is_drag): change_color = False
        if (change_color):
            pygame.draw.circle(self.image, RED, self.size/2, self.radius)    
        else:
            pygame.draw.circle(self.image, WHITE, self.size/2, self.radius)  

        if (self.is_hightlight1):
            self.image.blit(self.text_sprite_hightlighted.image, self.text_sprite_hightlighted.rect.topleft)
        else:
            self.image.blit(self.text_sprite.image, self.text_sprite.rect.topleft)
        
        if (self.is_hightlight2):
            self.image.blit(self.frame_image, (0,0))

    
    