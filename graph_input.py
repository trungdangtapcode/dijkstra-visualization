from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph import Graph

from config import *
import system

class GraphInput:
    def __init__(self):
        self.graph = system.graph
    
    def convert_from_string(self, s: str):
        lines = s.strip().split('\n')
        self.graph.__init__()

        dic = {}
        def get_key(s):
            if (s not in dic):
                dic[s] = len(dic)
            return dic[s]
        
        for line in lines:
            tmp = line.strip().split(' ')
            lst = []
            for x in tmp:
                if (x==''): continue
                lst.append(x)
            if (len(lst)==2):
                x, y = lst
                nodeU = self.graph.get_node_from_label(x)
                nodeV = self.graph.get_node_from_label(y)
                self.graph.connect_node(nodeU, nodeV)
            elif (len(lst)==3):
                x, y, c = lst
                c = int(c)
                nodeU = self.graph.get_node_from_label(x)
                nodeV = self.graph.get_node_from_label(y)
                self.graph.connect_node(nodeU, nodeV, c)
            else:
                print('[ERROR] wrong input')
