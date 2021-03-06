from subject import *
from data_structure import *
import json as js
import networkx as nx
from graphviz import Digraph as dg
from draw_graph import *
from sys import exit, argv

from main import write_all_data_for_major

dataStructure = Data_structure()
graph = dataStructure.getGraph()
data = dataStructure.getData()
orCounter = 0

def generate_graph(major_code):

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
    with open(f"../data/{major_code}/course_data.json") as json_file:
        data1= js.load(json_file)
        for k, p in data1.items():
            courseSubject = Subject(p)
            courseSubject.addValues(p['course_name'], p['semesters'], p['major_part'] )
            dataStructure.addSubject(k, courseSubject)
    # add prereqs
    with open(f"../data/{major_code}/prerequisites.json") as pre_file:
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
                    graph.remove_node(node)
                    del dataStructure.data[node]
                    edited = True
                elif graph.in_degree(node) == 1:
                    single_parent = list(graph[node].keys())[0]
                    for child in graph.predecessors(node):
                        dataStructure.addPreRequisite(child, single_parent)
                    graph.remove_node(node)
                    del dataStructure.data[node]
                    edited = True


    draw_graph(dataStructure, major_code)

def go(code):
    write_all_data_for_major(code)
    generate_graph(code)

if __name__ == '__main__':
    '''l = [
        'https://my.uq.edu.au/programs-courses/plan.html?acad_plan=CHBIOW2342',
        'https://my.uq.edu.au/programs-courses/plan.html?acad_plan=CHENVW2342',
        'https://my.uq.edu.au/programs-courses/plan.html?acad_plan=CHMATW2342',
        'https://my.uq.edu.au/programs-courses/plan.html?acad_plan=CHMETW2342',
        'https://my.uq.edu.au/programs-courses/plan.html?acad_plan=MINGEW2342',
        'https://my.uq.edu.au/programs-courses/plan.html?acad_plan=ELCOMW2342',
        'https://my.uq.edu.au/programs-courses/plan.html?acad_plan=ELBIOW2342'
    ]
    for c in l:
        go(c.split('=')[-1])
    exit(1)'''
    if len(argv) > 1:
        go(argv[1])
    else:
        while True:
            url = input('Enter major URL: ')
            try:
                code = url.split('=')[-1]
                write_all_data_for_major(code)
                generate_graph(code)
            except Exception:
                print('Invalid URL.')