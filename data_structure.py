import networkx as nx
from subject import *
class Data_structure:
    def __init__(self):
        self.graph = nx.DiGraph()

    def addSubject(self, course):
        self.graph.add_node(course)

    def addSubjects(self, courses):
        for course in courses:
            self.graph.add_node(course)
    
    def addPreRequisite(self, course1, course2):
        self.graph.has_node(course1)
        self.graph.has_node(course2)
        self.graph.add_edge(course1, course2)

    def addFutureSubject(self, course1, course2):
        self.graph.has_node(course1)
        self.graph.has_node(course2)
        self.graph.add_edge(course1, course2) 

    def getGraph(self):
        return self.graph