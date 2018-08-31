import networkx as nx
import subject
class Data_structure(self):
    def __init__(self):
        self.graph = nx.DiGraph()

    def addSubjects(self, courses):
        if(isinstance(courses, str)):
            courseSubject = new subject(courses)
            self.graph.add_node(courses)
        else:
            for course in courses:
                
            self.graph.add_nodes_from(courses)
    