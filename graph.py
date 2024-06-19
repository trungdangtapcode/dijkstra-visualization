from typing import Iterable
from pygame.sprite import AbstractGroup
from config import *
import system
import pygame
from node import Node
from edge import Edge

class Graph:
    def __init__(self):
        self.screen = system.screen
        self.visible_sprites = Camera()
        self.nodes = [Node(pos  = pos, 
            label = idx,
            groups = [self.visible_sprites]) 
            for idx, pos in enumerate([(-42,42), (42, 42), (-42,-42), (42,-42)])]
        self.edges = []
        system.graph = self
        self.connect_node(0,1)
        self.connect_node(1,2)
        self.nodes[0].hightlight1()
        self.nodes[0].hightlight2()

    def connect_node(self, index1, index2):
        assert max(index1,index2) < len(self.nodes), "index is out of list of nodes"
        if (index1==index2): 
            return
        nodeU = self.nodes[index1]
        nodeV = self.nodes[index2]
        edge = Edge(nodeU, nodeV, weight=2)
        if (nodeU not in nodeV.connected_nodes):
            nodeV.connect_node(nodeU, edge)
        if (nodeV not in nodeU.connected_nodes):
            nodeU.connect_node(nodeV, edge)
        self.edges.append(edge)

    def update(self):
        self.visible_sprites.draw() 
        self.visible_sprites.update()
        

class Camera(pygame.sprite.Group):
    def __init__(self, pos = (0,0)):
        super().__init__()
        self.size = CAMERA_SIZE
        self.screen = system.screen
        self.scale = 1 #~zoom out
        self.pos = pygame.math.Vector2(pos)
        system.camera = self

        self.is_drag = False
        self.drag_fixed_point = pygame.math.Vector2(0,0)

    def update(self):
        super().update()
        self.update_input()

    def update_input(self):
        self.scale -= system.mouse_scroll*0.2
        self.scale = pygame.math.clamp(self.scale, 0.2, 5)

        new_is_drag = self.is_drag
        if (pygame.mouse.get_pressed()[0] and not self.is_node_drag()):
            new_is_drag = True
        if (not pygame.mouse.get_pressed()[0]):
            new_is_drag = False

        if (not self.is_drag and new_is_drag):
            mouse_pos = self.get_mouse_world_pos()
            self.drag_fixed_point = mouse_pos
        self.is_drag = new_is_drag

        if (self.is_drag):
            diff = self.drag_fixed_point - self.get_mouse_world_pos()
            self.pos += diff


    def is_node_drag(self):
        for node in system.graph.nodes:
            if (node.is_drag):
                return True
        return False
    
    def draw(self):
        for edge in system.graph.edges:
            edge.draw()

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.zindex*10**9+sprite.rect.centery):
            self.draw_spirte(sprite)

    def pos_screen_to_wolrd(self, pos):
        pos = pygame.math.Vector2(pos)
        center = pygame.math.Vector2(self.size)/2
        pos = pos-center

        pos *= self.scale
        pos += self.pos
        return pos
    
    def pos_wolrd_to_screen(self, pos):
        pos = pygame.math.Vector2(pos)

        #world pos
        camera_topleft = self.pos \
            - self.scale*pygame.math.Vector2(self.size)/2
        pos = pos-camera_topleft
        
        #screen pos
        pos /= self.scale

        return pos

    def get_mouse_world_pos(self):
        mouse = pygame.mouse.get_pos()
        mouse = self.pos_screen_to_wolrd(mouse)

        return mouse

    def draw_spirte(self, sprite: Node):
        rect = sprite.rect
        img = sprite.image
        sz = pygame.math.Vector2(rect.size)/self.scale
        img = pygame.transform.scale(img, sz)

        pos = self.pos_wolrd_to_screen(rect.topleft)
        self.screen.blit(img, pos)