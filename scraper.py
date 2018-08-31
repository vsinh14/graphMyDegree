import enum
import urllib.request
from datetime import datetime
import json

import bs4 

import subject

class SemesterFlags(enum.Flag):
    SEMESTER_1 = 1 
    SEMESTER_2 = 2
    SUMMER = 4

    @classmethod
    def from_str(cls, string):
        if string == 'Semester 1':
            return cls.SEMESTER_1
        elif string == 'Semester 2':
            return cls.SEMESTER_2
        elif string == 'Summer Semester':
            return cls.SUMMER
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

def parse_course_code(course_code: str):
    url = 'https://my.uq.edu.au/programs-courses/course.html?course_code='+course_code
    with urllib.request.urlopen(url) as html_file:
        soup = bs4.BeautifulSoup(html_file.read())

        # Get the course title by deleting " (ABCD1234)" from the heading.
        course_name = soup.find('h1', {'id': 'course-title'}).text.replace(' ('+course_code+')', '', 1)
        # Gets everything else
        faculty = soup.find('p', {'id': 'course-level'}).text.strip()
        school = soup.find('p', {'id': 'course-faculty'}).text
        units = int(soup.find('p', {'id': 'course-units'}).text)

        duration = soup.find('p', {'id': 'course-duration'}).text

        this_year = str(datetime.today().year)

        offerings = SemesterFlags(0)
        semester_elements = soup.find_all('a', {'class': 'course-offering-year'})
        for sem_elem in semester_elements:
            # TODO: Will break for the first half of a year!!
            if this_year in sem_elem.text: # only consider offerings in this year.
                offerings |= SemesterFlags.from_str(sem_elem.text.replace(', '+this_year, '', 1))

        return Subject(
            course_name,
            course_code,
            duration,
            faculty,
            school,
            (offerings).int()
        )

def write_course_to_file(major_code: str, file_name: str):
    with open(file_name, 'w') as f:
        f.write(json.encoder.JSONEncoder(indent=4).encode(
            list(parse_one_major(major_code))
        ))

