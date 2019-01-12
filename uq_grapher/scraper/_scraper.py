import bs4 

from ..course_list import CourseList

class ProgramParser:
    """Abstract class representing a parser for a whole degree's course list.

    Concrete subclasses should define methods to parse a certain page.

    """
    
    def __init__(self):
        self.root_course_list = None
        self.current_course_list = None

    def parse_program_course_list(self, html: bs4.BeautifulSoup):
        root = html.find('div', {'id': 'program-course-list'})
        self.parse_program_title(root.find('h1').decode_contents())

        
        for planlist in root.find_all('div', {'class': 'planlist'}):
            title = planlist.find('h1').decode_contents()
            self.parse_plan_list(planlist, title)

            for table in planlist.find_all('table', {'class': 'courses'}):
                prev = table.find_previous_sibling('p')
                self.parse_course_table(table, prev.decode_contents())

        self.parse_endnotes(root.find('div', {'id': 'endnotes'}))

    def parse_endnotes(self, div: bs4.Tag):
        #print(div)
        pass

    def parse_program_title(self, title: str):
        """Parsesb the course list object associated with the given degree.
        """
        raise NotImplementedError
    

    def parse_course_table(self, table: bs4.Tag, text: str):
        """Parses the given course table and attaches it to the current course
        list.
        
        Arguments:
            table {bs4.Tag} -- table.courses containing list of courses.
            text {str} -- text immediately preceding this table.
    
        Raises:
            NotImplementedError -- [description]
        """
        #print('Handling course table')

    def course_table_helper(self, prereq_node, table: bs4.Tag):
        pass

    def parse_plan_list(self, div: bs4.Tag, title: str):
        """Parses the course list object to use for the given plan list div.
        
        Arguments:
            div {bs4.Tag} -- div.planlist to parse.
        
        Raises:
            NotImplementedError -- [description]
        """
        raise NotImplementedError

class BMathParser(ProgramParser):
    def parse_program_title(self, h1: str):
        self.current_course_list = CourseList(h1)
        self.root_course_list = self.current_course_list

    def parse_plan_list(self, div, title: str):
        course_list = CourseList(title)
        if title.startswith('Part '):
            course_list.set_depth(self.current_course_list, 1)
        else:
            course_list.set_depth(self.current_course_list, 2)
        self.current_course_list = course_list

    def parse_course():
        pass

def main():
    print('Scraper test')
    with open('bmath_list.html') as f:
        soup = bs4.BeautifulSoup(f)
        parser = BMathParser()
        parser.parse_program_course_list(soup)
        print(str(parser.root_course_list))