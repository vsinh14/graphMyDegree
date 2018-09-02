from subject import *
from data_structure import *
import json as js
import matplotlib.pyplot as plotting
import networkx as nx
from graphviz import Digraph as dg
from draw_graph import *
from sys import exit

dataStructure = Data_structure()
graph = dataStructure.getGraph()
data = dataStructure.getData()
orCounter = 0

def courseCheck(dataDict, string):
    if string in dataDict:
        return true
    return false

def recursiveRelation(dataStruct, key, part):
    if(isinstance(part, list)):
        #only one subject
        dataStruct.addPreRequisite(part[0], key)
        return
    #actual recursion
    actualRecursion(dataStruct, key, part)


def actualRecursion(dataStruct, key, part):
    #type all base case do nothing different
    global orCounter 
    if(part['type'] == "all"):
        for i in part['children']:
            if(isinstance(i, str)):
                dataStruct.addPreRequisite(i, key)
            else:
                actualRecursion(dataStruct, key, i)
    #type any or node before 
    
    if(part['type'] == "any"):
        orName = "orNode" + str(orCounter)
        orCounter+=1
        dataStruct.addSubject(orName, Subject(orName))
        for i in part["children"]:
            if(isinstance(i, str)):
                dataStruct.addPreRequisite(i, orName)
            else:
                actualRecursion(dataStruct, orName, i)
        dataStruct.addPreRequisite(orName, key)
        
#adding all subjects and information associated with subject
with open("data/SOFTWX2342/course_data.json") as json_file:
    data1= js.load(json_file)
    for k, p in data1.items():
        print(k)
        print(p['semesters'])
        courseSubject = Subject(p)
        courseSubject.addValues(p['course_name'], p['semesters'], p['major_part'] )
        dataStructure.addSubject(k, courseSubject)
# add prereqs
with open("data/SOFTWX2342/prerequisites.json") as pre_file:
    data2= js.load(pre_file)
    for k, p in data2.items():
        if(len(p) == 0):
            continue
        recursiveRelation(dataStructure, k, p)

graph = dataStructure.getGraph()


edited = True
while edited:
    edited = False 
    for i, node in enumerate(dict(graph.nodes())):
        if node.startswith('or'):
            if graph.in_degree(node) == 0 or graph.out_degree(node) == 0:
                print('Removing', node)
                graph.remove_node(node)
                del dataStructure.data[node]
                edited = True
            elif graph.in_degree(node) == 1:
                print('One in degree', node)
                single_parent = list(graph[node].keys())[0]
                print('', single_parent)
                for child in graph.predecessors(node):
                    print('', 'Has child', child)
                    dataStructure.addPreRequisite(child, single_parent)
                graph.remove_node(node)
                del dataStructure.data[node]
                edited = True


draw_graph(dataStructure)