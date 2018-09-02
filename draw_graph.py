from subject import *
from data_structure import *
import json as js
import matplotlib.pyplot as plotting
import networkx as nx
from graphviz import Digraph
import graphviz

colorDict ={"A":'orange', "B":'green', "C":"yellow", "D":"blue", None: 'white'}
def draw_graph(ds: Data_structure, file_name):
    drawn = Digraph('course plan', filename = file_name, format = 'pdf')
    drawn.attr('node', shape='box')
    data = ds.getData()
    graph = ds.getGraph()
    drawn.attr(fontname='Arial')
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
            name = graphviz.nohtml(data[key].getName()).replace('&', '&amp;')
            try:
                colour = colorDict[col]
            except KeyError:
                colour = 'white'
            drawn.node(key, label=f'<<FONT FACE="Arial"><TABLE BORDER="0"><TR><TD></TD></TR>{top}<TR><TD>{key}</TD></TR>{bottom}<TR><TD><FONT POINT-SIZE="10">{name}</FONT></TD></TR></TABLE></FONT>>', style='filled', fillcolor = colour)
    for edge in graph.edges:
        drawn.edge(edge[0], edge[1])
    drawn.attr(label=r'\n\nOrange is part A electives\nGreen is part B electives\nYellow is part C electives\nBlue is part D electives\nWhite is other')
    drawn.attr(fontsize='20')
    drawn.view()

    