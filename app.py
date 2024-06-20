import tkinter

from config import *
import system
import pygame
from graph import Graph
import threading
import tkinter as tk
from tkinter import ttk
import os
from dijkstra_solver import DijkstraSolver


class GraphScreen:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode(GRAPH_SIZE)
        pygame.display.set_caption('Dijkstra')
        self.screen = pygame.display.get_surface()
        system.screen = self.screen
        self.graph = Graph()
        self.clock = pygame.time.Clock()

    def update(self):
        mouse_wheel_event_check = False
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                system.app.is_run = False
            if event.type == pygame.MOUSEWHEEL:
                mouse_wheel_event_check = True
                system.mouse_scroll = event.y
            if event.type == pygame.KEYDOWN:
                if (event.key==pygame.K_t):
                    system.app.is_run = False
        if (not mouse_wheel_event_check): system.mouse_scroll = 0

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a]):
            system.app.is_run = False
    
        self.screen.fill(BLACK)
        self.graph.update()
        pygame.display.update()
        system.delta_time = self.clock.tick(FPS)/1000
        
        

class App:
    def __init__(self):
        self.root = tk.Tk()
        root = self.root
        embed = tk.Frame(root, width = 600, height = 600) #creates embed frame for pygame window
        embed.grid(columnspan = (600), rowspan = 600) # Adds grid
        embed.pack(side = tk.LEFT) #packs window to the left
        # buttonwin = tk.Frame(root, width = 100, height = 100)
        # buttonwin.pack(side = tk.LEFT)
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        root.protocol("WM_DELETE_WINDOW", lambda: self.close_window())

        #fixed init twice
        # print('inited ', self)
        self.graph_screen = GraphScreen()

        # button1 = tk.Button(buttonwin,text = 'Draw', width = 10,  command=lambda: self.hightlight(1))
        # button1.pack(side=tk.LEFT)

        system.app = self
        
        tablewin = tk.Frame(root, width = 600, height = 600)
        node = list(range(5))
        table = ttk.Treeview(tablewin, columns=node, show='headings')
        table.pack(fill='both')
        for i in node:
            table.heading(i, text=str(i))
            table.column(i, minwidth=0, width=100, stretch=tk.NO)
        scroll_bar = ttk.Scrollbar(tablewin, orient="horizontal", command=table.xview)
        scroll_bar.pack(side='bottom', fill='x')
        table.configure(xscrollcommand=scroll_bar.set)
        tablewin.pack()
        tablewin.pack_propagate(0)

        row = [9]*5
        table.insert(parent='',index = 0, values = row)


    def run(self):
        self.is_run = True
        while self.is_run:
            self.graph_screen.update()
            self.root.update()

    def hightlight(self, index):
        system.graph.nodes[1].hightlight1()

    def close_window(self):
        self.is_run = False





#fixed init twice
if __name__=="__main__":

    app = App()
    app.run()