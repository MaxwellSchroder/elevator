class Person:
    #initialise person to have simple paramters
    def __init__(self, level: int):
        self.level = level
        self.givenDestination = None
        self.upOrDown = None

'''
Lift is a simple object. Just holds numbers about itself basically
'''
class Lift:
    def __init__(self):
        self.level = 0
        self.maxCapacity = 10
        self.currentCapacity = 0
        self.currentPeople: list[Person] = []

'''
LiftManager class represents how people will actually request lifts, and what will schedule the lift
'''
class LiftManager:
    def __init__(self, lift: Lift):
        self.liftQueue = []
        self.nextDestination = None
        self.upOrDown = None
        self.lift = lift
        self.liftAreas = []
    
    def getOnLift(self, people: Person):
        return True

    def getOffLift(self, people: Person):
        pass

    # destination currently adds it last
    def addDestination(self, destination: int):
        self.liftQueue.append(destination)


'''
A lift area is an area where you can request lifts
'''
class LiftArea:
    def __init__(self, level: int, liftManager: LiftManager):
        self.level = level
        self.peopleHere: list[Person] = []
        self.goUpSelected = False
        self.goDownSelected = False
        self.liftManager = liftManager
    
    def joinLiftArea(self, person: Person):
        self.peopleHere.append(person)
    
    def leaveLiftArea(self, person: Person):
        self.peopleHere.remove(person)
    
    def alertPeopleLiftHere(self):
        for person in self.peopleHere:
            # if the person has selected up or down, and the persons direction selection matches that of the lift, or the lift has no given direction
            if person.upOrDown != None and (person.upOrDown == self.liftManager.upOrDown or self.liftManager.upOrDown == None):
                # attempt to add person
                if (self.liftManager.getOnLift(person) == True):
                    # remove person from this area, they are on lift
                    self.leaveLiftArea(person)
                else:
                    print("Person failed to get on lift")


if __name__ == "__main__":
    print("hello world")