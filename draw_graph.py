from subject import *
from data_structure import *
import json as js
import matplotlib.pyplot as plotting
import networkx as nx
from graphviz import Digraph

TOP_BORDER_STYLE = '''
border-top-width: 2px;
border-top-color: black;
border-top-style: solid;
'''
BOTTOM_BORDER_STYLE = '''
border-bottom-width: 2px;
border-bottom-color: black;
border-bottom-style: solid;
'''
BOTH_BORDER_STYLE = TOP_BORDER_STYLE + BOTTOM_BORDER_STYLE

border_styles = {
    1: TOP_BORDER_STYLE,
    2: BOTTOM_BORDER_STYLE,
    3: BOTH_BORDER_STYLE,
}

def draw_graph(ds: Data_structure):
    drawn = Digraph('course plan', filename = 'courseplan', format = 'pdf')
    drawn.attr('node', shape='box')
    data = ds.getData()
    graph = ds.getGraph()
    for key in data.keys():
        if(key.startswith('or')):
            drawn.attr('node', shape="circle", color = "grey", style='filled', fillcolor = 'grey')
            drawn.node(key, "or")
            drawn.attr('node', shape='box')
        else:
            
            style = border_styles[data[key].getOffering() & 3]
            drawn.node(key, label=f'''<<TABLE><TR><TD>{key}</TD></TR></TABLE>>''')
    for edge in graph.edges:
        drawn.edge(edge[0], edge[1])
    drawn.view()

    