from scraper import *
from sys import exit

if __name__ == '__main__':
    write_course_to_file('SOFTWX2342', 'software_engineering_courses.json')
    exit()
    raise 'a'
    parse_one_major('https://my.uq.edu.au/programs-courses/plan_display.html?acad_plan=SOFTWX2342')
