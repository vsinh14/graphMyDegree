import os
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
import json

from prereq import parse_prereq

def main():
    decoder = JSONDecoder()
    encoder = JSONEncoder(indent=4)
    # Loop over every file in the course_data folder.
    # These files are dictionaries of data for single courses.
    for course_file in os.listdir('./course_data'):
        with open(os.path.join('./course_data', course_file)) as c:
            data = decoder.decode(c.read())
        if data is None:
            continue
        print('Parsing', data['course_code'])
        with open('./prerequisites/'+data['course_code']+'.json', 'w') as out:
            out.write(encoder.encode(
                parse_prereq(data['prerequisites'], data['course_code'])
            ))

if __name__ == '__main__':
    main()