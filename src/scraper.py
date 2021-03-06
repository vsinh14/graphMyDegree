import enum
import urllib.request
import datetime as dt
import json
import os
from collections import defaultdict

import multiprocessing.dummy as mp

import bs4 

from subject import *

class SemesterFlags(enum.Flag):
    SEMESTER_1 = 1 
    SEMESTER_2 = 2
    SUMMER = 4
    TRIMESTER_1 = 8
    TRIMESTER_2 = 16 
    TRIMESTER_3 = 32

    @classmethod
    def from_str(cls, string):
        if string == 'Semester 1':
            return cls.SEMESTER_1
        elif string == 'Semester 2':
            return cls.SEMESTER_2
        elif string == 'Summer Semester':
            return cls.SUMMER
        elif string == 'Trimester 1':
            return cls.TRIMESTER_1
        elif string == 'Trimester 2':
            return cls.TRIMESTER_2
        elif string == 'Trimester 3':
            return cls.TRIMESTER_3
        raise ValueError('Unknown semester string ' + string)

    """
    Returns the flag represented as an int. 
    """
    def int(self):
        value = 0
        if self & self.SEMESTER_1:
            value += 1
        if self & self.SEMESTER_2:
            value += 2
        if self & self.SUMMER:
            value += 4
        if self & self.TRIMESTER_1:
            value += 8 
        if self & self.TRIMESTER_2:
            value += 16 
        if self & self.TRIMESTER_3:
            value += 32
        return value


"""
Parses the requirements of a major.

Returns an iterable of course codes.
"""
def parse_one_major(major_code: str):
    major_url = 'https://my.uq.edu.au/programs-courses/plan_display.html?acad_plan=' + major_code
    with urllib.request.urlopen(major_url) as url_object:
        soup = bs4.BeautifulSoup(url_object.read())
        course_codes = list(_parse_course_codes(soup))
        return _parse_course_codes(soup)

"""
Gets the course codes from a major page's soup and yields them.
"""
def _parse_course_codes(major_soup: bs4.BeautifulSoup):
    links = major_soup.select('.courses > tbody tr a[href^="/programs-courses/course.html"]')
    for l in links:
        yield l.attrs['href'].replace('/programs-courses/course.html?course_code=', '', 1)

_id_mapping = {
    'course-level': 'level',
    'course-faculty': 'faculty',
    'course-school': 'school',
    'course-units': 'units',
    'course-duration': 'duration',
    'course-contact': 'contact',
    'course-restricted': 'restricted',
    'course-incompatible': 'incompatible',
    'course-prerequisite': 'prerequisites',
    'course-assessment-methods': 'assessment-methods',
    'course-coordinator': 'coordinator',
    'course-studyabroard': 'study-abroad',
    'course-summary': 'description',
}

def course_html_opener(code): 
    html_path = f'./html/{code}.html'
    if os.path.exists(html_path):
        print('loading from html', code)
        return open(html_path, encoding='utf-8')
    else:
        print('downloading', code)
        return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}))

def parse_course_code(course_code: str):
    url = 'https://my.uq.edu.au/programs-courses/course.html?course_code='+course_code
    with course_html_opener(course_code) as html_file:
        soup = bs4.BeautifulSoup(html_file.read())

        dictionary = {}
        def _find_section(element_id, output_key):
            try:
                dictionary[output_key] = soup.find('p', {'id': element_id}).text.strip()
            except AttributeError:
                dictionary[output_key] = ''

        # Get the course title by deleting " (ABCD1234)" from the heading.
        try:
            course_name = soup.find('h1', {'id': 'course-title'}).text.replace(' ('+course_code+')', '', 1)
        except AttributeError:
            return None

        dictionary['course_code'] = course_code
        dictionary['course_name'] = course_name


        # this_year = str(dt.datetime.today().year)
        # offerings = SemesterFlags(0)
        semesters = []
        semester_elements = soup.find('div', {'id': 'description'}).find_all('a', {'class': 'course-offering-year'})
        for sem_elem in semester_elements:
            sem = sem_elem['href'].split('&offer=')[1].split('&')[0]
            if '&year=' in sem_elem['href']:
                year = int(sem_elem['href'].split('&year=')[1].split('+')[0])
            else:
                year = dt.datetime.today().year
            teaching_period = None 
            sem_elem: bs4.Tag = sem_elem
            if '(' in sem_elem.text:
                print(sem_elem.text)
                teaching_period = sem_elem.text.split('(')[1].split(')')[0]
                if teaching_period == 'Standard':
                    teaching_period = None
            semesters.append({'code': sem, 'year': year, 'teaching_period': teaching_period})
            # # TODO: Will break for the first half of a year!!
            # if this_year in sem_elem.text: # only consider offerings in this year.
            #     offerings |= SemesterFlags.from_str(sem_elem.text.replace(', '+this_year, '', 1).strip().split(' (')[0])

        dictionary['semesters'] = semesters

        for k, v in _id_mapping.items():
            _find_section(k, v)
        # gets everything else

        dictionary['last_updated'] = dt.datetime.now(dt.timezone.utc).isoformat()

        return dictionary

class MajorPart(dict):
    def __init__(self, parent, label):
        self.parent = parent
        self['label'] = label
        self['children'] = []

    def add_child(self, child):
        self['children'].append(child)

def first_element_child(tag: bs4.Tag):
    for c in tag.children:
        if isinstance(c, bs4.Tag):
            return c

def remove_left_bracket(text):
    return text.replace('[\t\r\n\t', '', 1).replace('[\u00a0', '', 1)


def parse_major_properly(major_code):
    url = 'https://my.uq.edu.au/programs-courses/plan_display.html?acad_plan='+major_code
    with urllib.request.urlopen(url) as html_file:
        soup = bs4.BeautifulSoup(html_file.read())

        parts = []
        current_object = None
        current_part = None
        course_parts = defaultdict(lambda: set()) # Set for uniqueness.

        major_name = soup.find('h1', {'class': 'trigger'}).text
        intro_html = ''
        for part in soup.find('div', {'class': 'block'}).children:
            if isinstance(part, bs4.NavigableString):
                continue
            part: bs4.Tag = part
            if not part.text.strip():
                continue
            if part.name in ('p', 'ol'):
                intro_html += part.decode_contents()
            elif 'courselist' in part.attrs['class']: 
                # This is the case type we'll see. Almost everything is here.
                first_child = first_element_child(part)
                table = part.find('table', {'class': 'courses'})
                if first_child.name == 'h2': # Part A, B, ... heading.
                    current_part = first_child.text
                if table is not None:
                    for r in table.find_all('tr'):
                        link = first_element_child(r)
                        code = remove_left_bracket(link.text.strip())
                        if code in ('or', 'Course Code'):
                            continue # Blacklist.
                        course_parts[code].add(current_part)
        
        return {k: list(v) for k, v in course_parts.items()}



def write_course_to_file(major_code: str, file_name: str):
    courses = list(parse_one_major(major_code))
    with open(file_name, 'w') as f:
        f.write(json.encoder.JSONEncoder(indent=4).encode(
            courses
    ))
    return courses

def write_course_data_to_file(course_list, file_name):
    courses_dict = {}
    for c in course_list:
        print('Getting course data for', c)
        courses_dict[c] = parse_course_code(c)
    with open(file_name, 'w') as f:
        f.write(json.encoder.JSONEncoder(indent=4).encode(courses_dict))
    return courses_dict

def scrape_one_course_worker(course_code, folder_name):
    print('Start', course_code)
    result = parse_course_code(course_code)
    with open(folder_name + '/'+course_code+'.json', 'w') as f:
        f.write(json.encoder.JSONEncoder(indent=4).encode(result))
    print('Finished', course_code)

def multithread_write_course_data_to_file(course_list, folder_name):
    # for c in course_list:
    #     scrape_one_course_worker(c, folder_name)
    import time
    import random
    with mp.Pool(50) as pool:
        for c in course_list:
            pool.apply_async(
                func=scrape_one_course_worker, 
                args=(c, folder_name)
            )
            time.sleep(3.5+1*random.random())
        pool.close() 
        pool.join()


def write_major_parts_to_file(major_code, file_name):
    parts = parse_major_properly(major_code)
    with open(file_name, 'w') as f:
        f.write(json.encoder.JSONEncoder(indent=4).encode(
            parts
        ))
    return parts

if __name__ == '__main__':
    write_major_parts_to_file('SOFTWX2342', 'soft_eng_major_parts.json')


