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
from graph_input import GraphInput


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
        button_restart = tk.Button(buttonwin,text = 'Restart', width = 10,  command=lambda: self.reset_table())
        button_restart.pack(side=tk.LEFT, padx=15)
        buttonwin.pack_propagate(0)

        #Input
        self.input_frame = tk.Frame(root, width= 300, height=600)
        self.input_frame.pack(side=tk.RIGHT)
        self.input_frame.pack_propagate(0)

        self.graph_input = GraphInput()
        self.textbox_frame = tk.Frame(self.input_frame, width= 300, height= 400)
        self.textbox_frame.pack(side=tk.TOP)
        self.textbox = tk.Text(self.textbox_frame)
        self.textbox.pack(side=tk.TOP, expand=True,fill='both', padx=15, pady=15)
        self.textbox.pack_propagate(0)
        self.textbox.insert(tk.END, '1 2 2\n2 5 5\n2 3 4\n1 4 1\n4 3 3\n3 5 1\n')
        self.textbox.insert(tk.END, '5 6 3\n6 b 1\n5 b 5\n4 5 2\n5 a 3\n')

        self.button_tb_frame = tk.Frame(self.input_frame, width= 300, height= 200)
        self.button_tb_frame.pack(side=tk.TOP)
        self.button_tb = tk.Button(self.button_tb_frame,text = 'Enter', width = 10,  command=lambda: self.tb_to_graph())
        self.button_tb.pack(side=tk.TOP, padx=15)

        #Solver
        self.reset_table()

        # print(solver_frame.winfo_width())

    def tb_to_graph(self):
        self.graph_input.convert_from_string(self.textbox.get(1.0, tk.END))
        self.reset_table()

    def init_table(self):
        table = ttk.Treeview(self.tablewin, show='headings')
        self.table = table
        
        scroll_bar_h = ttk.Scrollbar(self.tablewin, orient="horizontal", command=table.xview)
        scroll_bar_h.pack(side='bottom', fill='x')
        table.configure(xscrollcommand=scroll_bar_h.set)
        
        scroll_bar_v = ttk.Scrollbar(self.tablewin, orient="vertical", command=table.yview)
        scroll_bar_v.pack(side=tk.RIGHT, fill=tk.Y)
        table.configure(yscrollcommand=scroll_bar_v.set)

        table.pack(fill='both', expand=1, padx=15)

    def reset_table(self):
        for row in self.table.get_children():
            self.table.delete(row)
        for col in self.table['columns']:
            self.table.heading(col, text='')

        node = list(range(len(system.graph.nodes)))
        self.table['columns'] = node
        for i in node:
            self.table.heading(i, text=system.graph.nodes[i].label)
            self.table.column(i, minwidth=0, width=100, stretch=tk.NO)
        self.solver = DijkstraSolver(system.graph)
        self.solver.start()  

        for node in system.graph.nodes:
            node.unhightlight2()
            node.unhightlight1()

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