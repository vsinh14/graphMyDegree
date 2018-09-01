from subject import *
from data_structure import *
import json as js
import matplotlib.pyplot as plotting
import networkx as nx
from graphviz import Digraph as dg

data = Data_structure()
with open("software_engineering.json") as json_file:
    data1= js.load(json_file)
    for p in data1:
        courseSubject = Subject(p)
        data.addSubject(courseSubject)
data.addFutureSubject("ENGG1100","ENGG1200")
data.addPreRequisite("ENGG1211","ENGG1200")
graph = data.getGraph()
A=nx.nx_pydot.to_pydot(graph)
print(A.source)