#fixed init twice
from app import App
import pygame
from graph import Camera, Graph

app: App
# app = None
screen: pygame.Surface
delta_time: float
delta_time = 10**-6
camera: Camera
graph: Graph
mouse_scroll = 0