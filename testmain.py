from subject import *
from data_structure import *
import json as js

data = Data_structure()
with open("software_engineering_courses.json") as json_file:
    data1= js.load(json_file)
    for p in data1:
        courseSubject = Subject(p)
        data.addSubject(courseSubject)
for n in data.getGraph():
    print(n.getCourseCode())