from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph import Graph

from config import *
import system
from copy import copy


class DijkstraSolver:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.num_nodes = len(self.graph.nodes)
        self.table = []
        self.is_end = False
        self.is_locked = [False]*self.num_nodes

    def start(self, start_node = 0):
        self.start_node = start_node
        row = [(INF,start_node)]*self.num_nodes
        row[self.start_node] = (0,start_node)
        self.graph.nodes[self.start_node].hightlight1()
        self.add_row(row)

    def add_row(self, row):
        self.table.append(row)
        system.app.table_append(row)

    def step(self):
        if (self.is_end): return
        u = -1
        last = copy(self.table[-1])
        for i in range(self.num_nodes):
            if ((u==-1 or last[u]>last[i]) 
                and not self.is_locked[i]
                and not last[i][0]==INF):
                u = i
        if (u==-1):
            self.is_end = True
            return
        self.is_locked[u] = True

        system.app.table_edit(
            str(last[u][0])+' '+str(last[u][1])+'*'
            ,col=u)

        
        nodeU = system.graph.nodes[u]
        for edge in nodeU.adj:
            nodeV = edge.nodeV if edge.nodeV!=nodeU else edge.nodeU
            v = self.graph.nodes.index(nodeV)
            c = edge.weight if edge.weight else 0
            if (not self.is_locked[v] and last[u][0]+c<last[v][0]):
                nodeV.hightlight1()
                last[v] = (last[u][0]+c, u)

        last[u] = '-'
        nodeU.hightlight2()
        self.add_row(last)

    def update(self):
        pass