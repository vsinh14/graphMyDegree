import networkx as nx
from subject import *
"""

This stores the graph of the major

"""
class Data_structure:

    """
    Initalises the data structure
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self.data = {}

    """
    adding a subject node
    """
    def addSubject(self, courseKey, course):
        self.data[courseKey] = course 
        self.graph.add_node(courseKey)

    """
    adding a prereq edge
    course1 is a prerequisite for course2
    """
    def addPreRequisite(self, course1, course2):
        if self.graph.has_node(course1) & self.graph.has_node(course2):
            self.graph.add_edge(course1, course2)

    def deletePreRequisite(self, course1, course2):
        if self.graph.has_node(course1) & self.graph.has_node(course2):
            self.graph.remove_edge(course1, course2)
    """
    return graph object
    """
    def getGraph(self):
        return self.graph
    """
    return dict with data
    """
    
    def getData(self):
        return self.data