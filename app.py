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
        root.protocol("WM_DELETE_WINDOW", lambda: self.close_window())

        embed = tk.Frame(root, width = 600, height = 600, bg="red") #creates embed frame for pygame window
        embed.grid(columnspan = (600), rowspan = 600) # Adds grid
        embed.pack(side = tk.LEFT) #packs window to the left
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        #fixed init twice
        # print('inited ', self)
        self.graph_screen = GraphScreen()

        system.app = self
        
        #Solver_frame = Table + Button
        solver_frame = tk.Frame(root, width = 600, height = 600, bg="red")
        solver_frame.pack(side=tk.LEFT)
        solver_frame.pack_propagate(0)

        #Table
        self.tablewin = tk.Frame(solver_frame, width = 600, height = 500)
        self.tablewin.pack()
        self.tablewin.pack_propagate(0)
        self.init_table()

        #Button
        buttonwin = tk.Frame(solver_frame, width = 600, height = 100) 
        buttonwin.pack(side = tk.LEFT)
        button_next_step = tk.Button(buttonwin,text = 'Step', width = 10,  command=lambda: self.solver_step())
        button_next_step.pack(side=tk.LEFT, padx=15)
        button_restart = tk.Button(buttonwin,text = 'Restart', width = 10,  command=lambda: self.init_table())
        button_restart.pack(side=tk.LEFT, padx=15)
        buttonwin.pack_propagate(0)

        #Input
        self.input_frame = tk.Frame(root, width= 300, height=600,bg="orange")
        self.input_frame.pack(side=tk.RIGHT)
        self.input_frame.pack_propagate(0)

        #Solver
        self.solver = DijkstraSolver(system.graph)
        self.solver.start()

        # print(solver_frame.winfo_width())


    def init_table(self):
        node = list(range(len(system.graph.nodes)))
        table = ttk.Treeview(self.tablewin, columns=node, show='headings')
        self.table = table
        for i in node:
            table.heading(i, text=str(i))
            table.column(i, minwidth=0, width=100, stretch=tk.NO)
        
        scroll_bar_h = ttk.Scrollbar(self.tablewin, orient="horizontal", command=table.xview)
        scroll_bar_h.pack(side='bottom', fill='x')
        table.configure(xscrollcommand=scroll_bar_h.set)
        
        scroll_bar_v = ttk.Scrollbar(self.tablewin, orient="vertical", command=table.yview)
        scroll_bar_v.pack(side=tk.RIGHT, fill=tk.Y)
        table.configure(yscrollcommand=scroll_bar_v.set)

        table.pack(fill='both', expand=1, padx=15)
        
    def table_append(self, row):
        self.table.insert(parent='',index = 'end', values = row)

    def table_edit(self, value, idx = -1, col = None):
        row_id = self.table.get_children()[idx]
        if (col!=None):
            row = self.table.item(row_id)['values']
            row[col] = value
            self.table.item(row_id, values = row)
        else:
            self.table.item(row_id, values = value)

    def solver_step(self):
        self.solver.step()

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