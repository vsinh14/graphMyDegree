
class CourseList:
    def __init__(self, name: str):
        self.name = name
        self.children = []
        self.prereq_node = None
        self.parent = None
        self.depth = 0

    def set_parent(self, parent):
        parent.children.append(self)
        self.parent = parent
        self.depth = 0 if parent is None else (parent.depth + 1)

    def set_depth(self, parent: 'CourseList', depth: int):
        while parent.depth > depth-1:
            parent = parent.parent
        self.set_parent(parent)

    def __repr__(self):
        return f'CourseList(name={repr(self.name)}, depth={self.depth})'

    def __str__(self):
        if not self.children:
            return repr(self)
        else:
            return repr(self) + '\n  ' + '\n'.join(str(x) for x in self.children) \
                .replace('\n', '\n  ')