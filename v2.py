import time
import threading

class Person:
    # initialise person to have simple paramters
    # TODO: name is just for debugging
    def __init__(self, level: int, name: int, liftManager, startingLiftArea):
        self.level = level
        self.givenDestination = None
        self.upOrDown = None
        self.name = name
        self.liftManager = liftManager
        self.liftArea = startingLiftArea
    
    def goUp(self):
        self.liftArea.requestGoUp()
    
    def goDown(self):
        self.liftArea.requestGoDown()

'''
Lift is a simple object. Just holds numbers about itself basically
'''
class Lift:
    def __init__(self):
        self.level = 1
        self.maxCapacity = 10
        self.currentCapacity = 0
        self.currentPeople: list[Person] = []

'''
LiftManager class represents how people will actually request lifts, and what will schedule the lift
'''
class LiftManager:
    def __init__(self, lift: Lift, numLevels: int):
        self.liftQueue = []
        self.nextDestination: int = -1
        self.upOrDown: str = ""
        self.lift = lift
        #initialise to empty list, going from floor level to the LiftArea associated with it
        self.liftAreas = dict()
        self.numLevels = numLevels
        self.setup_liftAreas()
    
    
    def setup_liftAreas(self):
        # add to the dictionary of lift area's the area for each level
        for i in range(1, self.numLevels+1):
            self.liftAreas[i] = LiftArea(i, self)
    
    def getOnLift(self, person: Person):
        if (len(self.lift.currentPeople) < self.lift.currentCapacity):
            self.lift.currentPeople.append(person)
            return True
        return False

    def getOffLift(self, person: Person):
        self.lift.currentPeople.remove(person)

    # destination currently adds it last
    def addDestination(self, destination: int):
        self.liftQueue.append(destination)

    # create function to continuosly poll the liftQueue and go to that level
    def liftDestinationButtonPressed(self, destination: int):
        self.liftQueue.append(destination)
    
    

    # this function runs indefinitely, and moves the lift based on the queue
    def functionThatMovesLift(self):
        # run indefinitely
        
        while True:
            if (self.nextDestination != -1):
                # go to this level
                
                # is lift at its destionation level right now
                if (self.nextDestination == self.lift.level):
                    # lift arrived at level
                    # alert everyone on lift that lift is at this level
                    for person in self.lift.currentPeople:
                        if person.givenDestination == self.lift.level:
                            # person gets off lift and join's lift area
                            self.getOffLift(person)
                            self.liftAreas[self.lift.level].joinLiftArea(person)

                    # alert everyone in lift area at this level lift is here
                    self.liftAreas[self.lift.level].alertPeopleLiftHere()
                elif (self.nextDestination > self.lift.level):
                    # going up to level
                    print("going up past " + str(self.lift.level))
                    self.lift.level += 1
                    
                else:
                    #going down to level
                    print("going down past " + str(self.lift.level))
                    self.lift.level -= 1
                    print("going down past " + self.lift.level)
            elif (len(self.liftQueue) > 0):
                self.nextDestination = self.liftQueue.pop()
                print(" new target acquired ")
            else:
                print("waiting idle...")
                time.sleep(1)


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
    
    def requestGoUp(self):
        if not (self.goUpSelected):
            # add this level as a desetination it has to go to
            self.liftManager.addDestination(self.level)
    
    def requestGoDown(self):
        if not (self.goDownSelected):
            # add this level as a destination it's going to
            self.liftManager.addDestination(self.level)

    def joinLiftArea(self, person: Person):
        self.peopleHere.append(person)
    
    def leaveLiftArea(self, person: Person):
        self.peopleHere.remove(person)
    
    def alertPeopleLiftHere(self):
        for person in self.peopleHere:
            # if the person has selected up or down, and the persons direction selection matches that of the lift, or the lift has no given direction
            if person.upOrDown != "" and (person.upOrDown == self.liftManager.upOrDown or self.liftManager.upOrDown == ""):
                # attempt to add person
                if (self.liftManager.getOnLift(person) == True):
                    # remove person from this area, they are on lift
                    self.leaveLiftArea(person)
                else:
                    print("Person failed to get on lift")


if __name__ == "__main__":
    print("hello world")

    # create lift1
    lift1 = Lift()
    # create lift1 manager
    numLevels: int = 3
    lift1Manager = LiftManager(lift1, numLevels)

    # threadify the scheduler
    # scheduler_thread = threading.Thread(target=lift1Manager.functionThatMovesLift, name="scheduler")
    # scheduler_thread.start()
    

    people: list[Person] = []
    # create 3 people
    for i in range(1,numLevels+1):
        people.append(Person(i, name=i, liftManager=lift1Manager, startingLiftArea=lift1Manager.liftAreas[i]))
    
    # add people to their respective area
    for i in range(0, len(people)):
        lift1Manager.liftAreas[i+1].joinLiftArea(people[i])

    # person2 requests lift
    people[2].goUp()



    # lift should move up to level 2, open and let person 2 know to get on.

    # person 2 selects go to level 3

    # lift goes to level 3, person 2 gets out and enters level 3 area.

    # person 1 requests lift

    # lift comes down to level 1



