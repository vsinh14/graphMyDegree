import json


def main():
    major = 'ELECTX2342'
    with open(f'data/{major}/major_parts.json') as f:
        major_parts = json.load(f)

    with open(f'data/{major}/course_data.json') as f:
        course_data = json.load(f)

    for course, parts in major_parts.items():
        min_parts = min(x.split(' ')[1] for x in parts)
        print(course, parts, min_parts)
        course_data[course]['major_part'] = min_parts

    with open(f'data/{major}/course_data.json', 'w') as f:
        json.dump(course_data, f, indent=4)



if __name__ == '__main__':
    main()