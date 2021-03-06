from scraper import multithread_write_course_data_to_file
import json.decoder
import asyncio
import os
import scraper

def main():
    with open('course_codes.json') as f:
        course_list = json.decoder.JSONDecoder().decode(f.read())
    os.makedirs('./course_data/', exist_ok=True)
    existing_courses = set(os.path.basename(x).replace('.json', '', 1) for x in os.listdir('./course_data/'))    
    print(f'Parsed {len(existing_courses)} of {len(course_list)} courses.')
    # URL: https://my.uq.edu.au/programs-courses/browse.html?level=ugpg

    # s = []
    # for c in set(course_list) - existing_courses:
    #     s.append(f'wget \'https://my.uq.edu.au/programs-courses/course.html?course_code={c}\' -O {c}.html')
    # with open('wget.sh', 'w', newline='\n') as f:
    #     f.write('\n'.join(s))
    # return

    for c in set(course_list) - existing_courses:
        scraper.scrape_one_course_worker(c, './course_data/')
    # multithread_write_course_data_to_file(
    #     set(course_list)-existing_courses, './course_data/')
    return
    d = {}
    with open('all_course_data.json', 'w') as out:
        for f in os.listdir('./course_data/'):
            if f == 'all_course_data.json':
                continue
            with open('./course_data/'+f) as in_:
                obj = json.decoder.JSONDecoder().decode(in_.read())
                key = f.replace('.json', '', 1)
                d[key] = obj 
        out.write(json.encoder.JSONEncoder(indent=4).encode(d))


if __name__ == '__main__':
    main()