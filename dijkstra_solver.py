from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph import Graph

from config import *
import system


class DijkstraSolver:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.num_nodes = len(self.graph.nodes)
        self.table = []
        print(self.num_nodes)
    
    def step(self):
        pass

    def update(self):
        pass