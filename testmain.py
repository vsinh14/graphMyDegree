from subject import *
from data_structure import *
import json as js
import matplotlib.pyplot as plotting
import networkx as nx
from graphviz import Digraph as dg
from draw_graph import *
data = Data_structure()
graph = data.getGraph()
with open("software_engineering.json") as json_file:
    data1= js.load(json_file)
    for p in data1:
        courseSubject = Subject(p)
        data.addSubject(p, courseSubject)
print(graph.nodes)
data.addPreRequisite("ENGG1100","ENGG1200")
data.addPreRequisite("ENGG1200", "ENGG1211")
print(graph.edges)
draw_graph(data)