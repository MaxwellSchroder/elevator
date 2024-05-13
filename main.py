import time

'''
Person class represents a person who will request and get on lifts.
'''
class Person:
    def __init__(self, startingLevel: int):
        self.level = startingLevel
        self.onLift = None
        self.myDestination = None

    def pressLevel(self, destination: int):
        if (self.onLift != None):
            self.onLift.addDestination(destination)
            self.myDestination = destination

    def alertedOfFloor(self):
        # if my elevator is on my destination, get off
        if (self.onLift != None):
            if (self.onLift.getLevel == self.myDestination):
                self.onLift.leaveLift(self)
                print("I left eleavtor")

'''
Lift object represents a singular lift which can exist within a lift area. Lifts will be instructed where to go by the lift manager
'''
class Lift:
    def __init__(self):
        self.currentLevel = 0
        self.maxCapacity = 10
        self.currentHeadcount = 0
        self.peopleOnboard = [Person]
        self.liftq = []
    
    def setLevel(self, newLevel):
        self.currentLevel = newLevel
        # alert passengers that we are now on this level
        for passenger in self.peopleOnboard:
            passenger.alertedOfFloor()
    
    def addPerson(self, person: Person):
        # if you are already at max capacity, do not accept person to join elevator
        if (len(self.peopleOnboard) >= self.maxCapacity):
            pass
        else:
            self.peopleOnboard.append(person)

    def requestLift(self, goToLevel: int):
        self.liftq.append(goToLevel)
        self.goToLevel()
    
    def goToLevel(self):
        destination = self.liftq.pop()
        if (destination == self.currentLevel):
            pass
        elif (destination > self.currentLevel):
            for i in range(self.currentLevel + 1, destination + 1):
                time.sleep(1)
                self.setLevel(i)
        else:
            # TODO: need to test this
            for i in range(self.currentLevel - 1, destination):
                time.sleep(1)
                self.setLevel(i)

    def getLevel(self):
        return self.currentLevel

    def leaveLift(self, person: Person):
        self.peopleOnboard.remove(person)
    

    # Function to be moved later
    def getOnLift(self, person: Person):
        if (self.currentLevel == person.level):
            # attempt to add person to lift
            self.addPerson(person)

'''
LiftManager object reprents an area that contains one or more lifts. This is essential, because it manager for scheduling lifts to floors.   
'''
# class LiftManager:
#     def __init__(self, numLevels: int, lifts: list[Lift]):
#         self.numLevels = numLevels
#         self.lifts = lifts

#     # take requests handle all new requests for a lift to a level
#     def takeRequest(self, level):
#         # take the first lift from list of lists
#         lift = self.lifts

#         # move it to a level
#         lift.setLevel(level)

#     def getOnLift(self, person: Person):
#         lift = self.lifts[0]

#         if (lift.currentLevel == person.level):
#             # attempt to add person to lift
#             lift.addPerson(person)


if __name__ == "__main__":
    # create a lift shaft that has 10 levels
    lift1: Lift =  Lift()
    # liftManager: LiftManager = LiftManager(10, lift1)

    # someone requests a lift from level 1
    # create people
    person1: Person = Person(1)
    person2: Person = Person(2)
    person3: Person = Person(3)
    person4: Person = Person(4)

    # person1 requests a lift
    lift1.requestLift(1)
    lift1.getOnLift(person1)
    

    

    # person1 gets on lift
    # liftManager.getOnLift(person1)

    # someone gets on a lift, and requests to go to level 2

    # someone gets off at level 2
    print("success")