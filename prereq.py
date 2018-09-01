import re
import json.decoder

class Relation(dict):
    text = None 

    def __init__(self, children):
        self.children = children
        self['type'] = self.text
        self['children'] = children

class AndRelation(Relation):
    text = 'all'

class OrRelation(Relation):
    text = 'any'

# Replace operators with & and |
text_replaces = {
    '\n': ' ',
    # Strings to delete
    'At least 6 in ': '',
    ' (or equivalent)': '',
    ' preqreqs ': ' ',
    'prereq:': '',

    # High school subjects. Remove spaces.
    'HA in Yr 12 Maths C': '12_Maths_C_HA',
    'HA in Year 12 Maths C': '12_Maths_C_HA',
    'sound achievement or better in Qld Senior Maths C': '12_Maths_C_SA',
    'SA in Year 12 Maths C': '12_Maths_C_SA',
    'SA Yr 12 Maths C': '12_Maths_C_SA',
    'Maths B': '12_Maths_B',

    'Permission of Head of School': 'HOS_Permission',

    ' OR ': ' or ',
    ' + ': ' and ',
    ' & ': ' and ',
    ' | ': ' or ',
    '(': '( ',
    ')': ' )',
    ', ': ' ',
    ': ': ' ',
    '; ': ' ',
}

HIGHSCHOOL_SUBJECTS = ('12_Maths_C_HA', '12_Maths_C_SA', '12_Maths_B', 'HOS_Permission')
SKIP_TOKENS = ('prereq', 'prereqs')

COURSE_REGEX = re.compile(r'^[A-Z]{3,4}[0-9]{4}$')

OPERATIONS = {
    'and': AndRelation,
    'or': OrRelation,
}

"""Parses a fragment of a prereq string, split by spaces. 

Returns a 2-tuple of (relation, rest_of_elements).

The rest of the list should be parsed at the parent caller's level.
"""
def _parse_fragment(fragment, course_code, level=0):
    def _log(*args, **kwargs):
        print(' '*level, *args, **kwargs)
    _log('Parsing fragment', fragment)
    stack = []
    operation: Relation = None
    i = 0
    while i < len(fragment):
        token = fragment[i]
        if token in SKIP_TOKENS:
            _log('Skipping token:', token)
            pass
        elif COURSE_REGEX.match(token): # Add course codes to the stack.
            _log('Found course:', token)
            stack.append(token)
        elif token in HIGHSCHOOL_SUBJECTS:
            _log('Found high school subject:', token)
            stack.append(token)
        elif token.lower() == 'for': 
            # Continue only for our target course code.
            if fragment[i+1] != course_code:
                _log('Not our course.')
                break
            else:
                _log('Skipping 1 item.')
                i += 1
        elif token == '(':
            _log('Found (')
            len_remaining = len(fragment[i+1:]) # Number of tokens after this one.
            # Takes a fragment ['CSSE2002', ')', 'and', ...]
            # Returns ('CSSE2002', ['and', '...])
            this_elem, rest = _parse_fragment(fragment[i+1:], course_code, level+1) 
            len_of_rest = len(rest) # Number of tokens after the end of the brackets.
            if this_elem.children:
                stack.append(this_elem)
            i += (len_remaining-len_of_rest)+1
        elif token == ')':
            _log('Found )')
            break
        elif token in OPERATIONS:
            _log('Found operation:', token)
            if operation is None: 
                operation = OPERATIONS[token]
            elif OPERATIONS[token] == operation:
                pass # Operation is the same as current; continue.
            else:
                _log(' But operation already defined!')
        else:
            print(fragment)
            print('Unknown component', token)
        i += 1
    if operation is None:
        operation = lambda x: x
    return (operation(stack), fragment[i:])

"""
Parses a prereq string with operations into a relation.
"""
def parse_prereq(prereq_string: str, course_code: str):
    for k, v in text_replaces.items():
        prereq_string = prereq_string.replace(k, v)
    tokens = [x.strip() for x in prereq_string.split(' ') if x.strip()]
    return _parse_fragment(tokens, course_code)[0]

if __name__ == '__main__':
    print(parse_prereq('For COMS3000 prereq: CSSE2310; For COMS7003 prereq: CSSE7231', 'COMS3000'))

    prereq_dict = {}
    with open('course_data.json', 'r') as f:
        for course, data in json.decoder.JSONDecoder().decode(f.read()).items():
            print(course)
            prereq_dict[course] = parse_prereq(data['prerequisites'], course)
    with open('prerequisites.json', 'w') as f:
        f.write(json.encoder.JSONEncoder(indent=4).encode(prereq_dict))