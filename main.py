from scraper import *
from prereq import parse_prereq
from sys import exit
import os
import json

def update_course_data_folder(major_code):
    with open(f'data/{major_code}/course_data.json') as f:
        major_course_data = json.load(f)
    
    for c in major_course_data:
        with open(f'course_data/{c}.json') as f:
            old_data = json.load(f)
        if 'semesters' not in old_data:
            print('Updating', c)
            with open(f'course_data/{c}.json', 'w') as f:
                json.dump(major_course_data[c], f)


def write_all_data_for_major(major_code):
    os.makedirs('data/'+major_code, exist_ok=True)
    os.chdir('data/'+major_code)
    courses = write_course_to_file(major_code, 'course_list.json')
    course_data = write_course_data_to_file(courses, 'course_data.json')
    write_major_parts_to_file(major_code, 'major_parts.json')

    # with open('course_data.json') as f: course_data = json.load(f)

    prereq_dict = {}
    for course, data in course_data.items():
        prereq_dict[course] = parse_prereq(data['prerequisites'], course)
    with open('prerequisites.json', 'w') as f:
        f.write(json.encoder.JSONEncoder(indent=4).encode(prereq_dict))

    os.chdir('../..')

if __name__ == '__main__':
    for x in ('ELECTX2342', ):
        write_all_data_for_major(x)