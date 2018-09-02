from scraper import *
from prereq import parse_prereq
from sys import exit
import os
import json

def write_all_data_for_major(major_code):
    major_dir = './data/'+major_code+'/'
    os.makedirs(major_dir, exist_ok=True)
    # Writes the list of only course codes.
    print('Reading courses for', major_code)
    courses = write_course_to_file(major_code, major_dir+'course_list.json')

    # Dict of all course data in this major.
    course_data = {}

    for c in courses:
        print('Finding data for', c)
        # If the course is already parsed and updated with a semester code,
        # use that.
        if os.path.isfile(f'course_data/{c}.json'):
            try:
                with open(f'course_data/{c}.json') as f:
                    old_data = json.load(f)
            except json.JSONDecodeError:
                old_data = {} # Corrupted data, re-scrape.
            if 'semesters' in old_data:
                print(' ... using existing data.')
                course_data[c] = old_data
                continue 
        print(' ... scraping data.')
        # Otherwise, scrape and update the course data.
        new_data = parse_course_code(c)
        course_data[c] = new_data
        # Write to folder of all courses ever.
        with open(f'course_data/{c}.json', 'w') as f:
            json.dump(new_data, f, indent=4)

    # Handled writing course data manually above and further below.
    # print('Writing course data.')
    # course_data = write_course_data_to_file(courses, major_dir+'course_data.json')

    print('Writing major parts.')
    major_parts = write_major_parts_to_file(major_code, major_dir+'major_parts.json')

    # Adds the part letter to the major's course_data.json.
    for course, parts in major_parts.items():
        try:
            min_parts = min(x.split(' ')[1] for x in parts)
            print(course, parts, min_parts)
        except AttributeError:
            min_parts = None
        course_data[course]['major_part'] = min_parts

    for k, v in course_data.items():
        if 'major_part' not in v:
            v['major_part'] = None

    print('Rewriting with added part letter.')
    with open(major_dir+'course_data.json', 'w') as f:
        json.dump(course_data, f, indent=4)

    print('Analysing prereqs.')
    prereq_dict = {}
    for course, data in course_data.items():
        prereq_dict[course] = parse_prereq(data['prerequisites'], course)
    print('Writing prereqs.')
    with open(major_dir+'prerequisites.json', 'w') as f:
        f.write(json.encoder.JSONEncoder(indent=4).encode(prereq_dict))

if __name__ == '__main__':
    for x in ('ELECTX2342', 'MECHAX2342', 'CIVILX2342', 'CHEMIX2342', 'MININX2342'):
        write_all_data_for_major(x)