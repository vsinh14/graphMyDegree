from subject import *
from data_structure import *
import json as js
import matplotlib.pyplot as plotting
import networkx as nx
from graphviz import Digraph

colorDict ={"A":'orange', "B":'green', "C":"yellow", "D":"blue"}
def draw_graph(ds: Data_structure):
    drawn = Digraph('course plan', filename = 'courseplan', format = 'pdf')
    drawn.attr('node', shape='box')
    data = ds.getData()
    graph = ds.getGraph()
    for key in data.keys():
        if(key.startswith('or')):
            drawn.attr('node', shape="circle", color = "grey", style='filled', fillcolor = 'grey')
            drawn.node(key, "or")
            drawn.attr('node', shape='box', style='filled')
        else:
            semester = data[key].getOffering()
            col = data[key].getMajorPart()

            top = '<HR/>' if semester & 1 else ''
            bottom = '<HR/>' if semester & 2 else '' 
            drawn.node(key, label=f'<<TABLE BORDER="0"><TR><TD></TD></TR>{top}<TR><TD>{key}</TD></TR>{bottom}<TR><TD></TD></TR></TABLE>>', style='filled', fillcolor = colorDict[col] )
    for edge in graph.edges:
        drawn.edge(edge[0], edge[1])
    drawn.attr(label=r'\n\nOrange is part A electives\nGreen is part B electives\nYellow is part C electives\nBlue is part D electives')
    drawn.attr(fontsize='20')
    drawn.view()

    