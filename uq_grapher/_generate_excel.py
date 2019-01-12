import os 
import glob
import csv 
import json

def generate_course_list(folder_path) -> list:
    # data = []
    # for f in glob.iglob(folder_path):
    #     with open(f) as file:
    #         c_data = json.load(file)
    #         data.append(c_data)
    #     print(f)

    # with open('course_data.json', 'w') as f:
    #     json.dump(data, f)
    with open('course_data.json') as f:
        data = json.load(f)


    with open('course_list.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, ('course_code', 'course_name', 'prerequisites', 'incompatible', 'restricted', 'faculty', 'school', 'units', 'semesters', 'duration', 'description'))
        writer.writeheader()
        # for x in data:
        #     if not x:
        #         print(x)
        # return
        writer.writerows(x for x in data if x)

    
    

if __name__ == "__main__":
    generate_course_list('bin/course_data/*.json')

