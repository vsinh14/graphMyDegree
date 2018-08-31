class Subject:
    def __init__(self, stringName, courseCode, duration, Faculty, School, offering):
        self.name = stringName
        self.courseCode = courseCode
        self.preRequisites = []
        self.futureSubject = []
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

    def addPreRequisite(self, subject):
        self.preRequisites.append(subject)

    def addFutureSubject(self, subject):
        self.futureSubject.append(subject)

    def getPreRequisiteList(self):
        return self.preRequisites

    def getFutureList(self):
        return self.futureSubject

    def getPreRequisiteNumber(self):
        return len(self.preRequisites)

    def getFutureNumber(self):
        return len(self.futureSubject)
    
    def getSchool(self):
        return self.School
    
    def getFaculty(self):
        return self.Faculty
    
    def getOffering(self):
        return self.offering