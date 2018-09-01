from scraper import *
from prereq import parse_prereq
from sys import exit
import os

def write_all_data_for_major(major_code):
    os.makedirs('data/'+major_code, exist_ok=True)
    os.chdir('data/'+major_code)
    courses = write_course_to_file('SOFTWX2342', 'course_list.json')
    course_data = write_course_data_to_file(courses, 'course_data.json')
    write_major_parts_to_file('SOFTWX2342', 'major_parts.json')

    prereq_dict = {}
    for course, data in course_data.items():
        prereq_dict[course] = parse_prereq(data['prerequisites'], course)
    with open('prerequisites.json', 'w') as f:
        f.write(json.encoder.JSONEncoder(indent=4).encode(prereq_dict))

    os.chdir('../..')

if __name__ == '__main__':
    for x in ('ELECTX2342', 'CIVILX2342', 'ELCOMW2342', 'MECHAX2342'):
        write_all_data_for_major(x)