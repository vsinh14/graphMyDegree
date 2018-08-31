class Subject:
    def __init__(self, stringName, duration, Faculty, School, offering):
        self.name = stringName
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

    def addPreRequisite(subject):
        self.preRequisites.append(subject)

    def addFutureSubject(subject):
        self.futureSubject.append(subject)

    def getPreRequisiteList():
        return self.preRequisites

    def getFutureList():
        return self.futureSubject

    def getPreRequisiteNumber():
        return len(self.preRequisites)

    def getFutureNumber:
        return len(self.futureSubject)
    
    def getSchool():
        return self.School
    
    def getFaculty():
        return self.Faculty
    
    def getOffering():
        return self.offering