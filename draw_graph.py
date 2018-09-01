from subject import *
from data_structure import *
import json as js
import matplotlib.pyplot as plotting
import networkx as nx
from graphviz import Digraph

def draw_graph(ds):
    drawn = Digraph('course plan', filename = 'courseplan.pdf', format = 'pdf')
    data = ds.getData()
    graph = ds.getGraph()
    for key in data.keys():
        drawn.node(key)
    for edge in graph.edges:
        drawn.edge(edge[0], edge[1])
    drawn.view()

    