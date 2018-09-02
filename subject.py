"""
This class stores all the basic subject information
"""
class Subject:
    """
    Initalises the subject with just a courseCode
    """
    def __init__(self, courseCode):
        self.courseCode = courseCode
    """
    Add all other values relating to the subjects
    """
    def addValues(self, stringName, offering, part):
        self.name = stringName
        # 1 for sem 1
        # 2 for sem 2
        # 3 for sem 1 & 2
        # 4 for summer sm 
        # 5 for summer sem and sem 1
        # 6 for summer sem and sem 2
        # 7 for sem 1 sem 2 and summer sem 
        self.part = part
        self.offering = offering

    """

    """
    def getMajorPart(self):
        return self.part    
    """
    returns full name of subject
    """
    def getName(self):
        return self.name 
    """
    returns offering int
    """
    
    def getOffering(self):
        return self.offering
    """
    returns courseCode
    """
    def getCourseCode(self):
        return self.courseCode