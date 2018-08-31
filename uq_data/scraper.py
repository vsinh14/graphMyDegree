import bs4 
import urllib.request

"""
Parses the requirements of a major.

Returns an iterable of course codes.
"""
def parse_major_url(major_url):
    with urllib.request.urlopen(major_url) as url_object:
        soup = bs4.BeautifulSoup(url_object.read())
        course_codes = list(_parse_course_codes(soup))
        #_parse_major_soup(soup)

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
        faculty = soup.find('p', {'id': 'course-level'}).text
        school = soup.find('p', {'id': 'course-faculty'}).text
        units = int(soup.find('p', {'id': 'course-units'}).text)
        

    

if __name__ == '__main__':
    parse_course_code('MATH1051')
    raise 'a'
    parse_major_url('https://my.uq.edu.au/programs-courses/plan_display.html?acad_plan=SOFTWX2342')