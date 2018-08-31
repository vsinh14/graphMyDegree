class Subject:
    def __init__(self, courseCode):
        self.courseCode = courseCode

    def addValues(self, stringName, duration, Faculty, School, offering):
        self.name = stringName
        self.duration = duration
        self.Faculty = Faculty
        self.School = School
        # 1 for sem 1
        # 2 for sem 2
        # 3 for sem 1 & 2
        # 4 for summer sm 
        # 5 for summer sem and sem 1
        # 6 for summer sem and sem 2
        # 7 for sem 1 sem 2 and summer sem 
        self.offering = offering

    def getDuration(self):
        return self.duration
    def getName(self):
        return self.name 

    def getSchool(self):
        return self.School
    
    def getFaculty(self):
        return self.Faculty
    
    def getOffering(self):
        return self.offering
    def getCourseCode(self):
        return self.courseCode