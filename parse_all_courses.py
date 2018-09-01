from scraper import write_course_data_to_file
import json.decoder

def main():
    with open('course_codes.json') as f:
        course_list = json.decoder.JSONDecoder().decode(f.read())
    try:
        with open('full_course_data.json') as f:
            existing_courses = set(json.decoder.JSONDecoder().decode(f.read()).keys())
    except FileNotFoundError:
        pass
    write_course_data_to_file(set(course_list)-existing_courses, 'full_course_data.json')


if __name__ == '__main__':
    main()