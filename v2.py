import time
import threading
from enum import Enum

# Enum class for standard values of no destination or no direction given
class elevatorDirection(Enum):
    noDestination = "none"
    noUpOrDown = "none"
    up = "up"
    down = "down"

'''
A person 
'''
class Person:
    # initialise person to have simple paramters
    # TODO: name is just for debugging
    def __init__(self, level: int, name: int, liftManager, startingLiftArea):
        self.level = level
        self.givenDestination = elevatorDirection.noDestination
        self.upOrDown = elevatorDirection.noUpOrDown
        self.name = name
        self.liftManager: LiftManager = liftManager
        self.liftArea: Area = startingLiftArea
        self.inLift = False

    # person requests to go up
    def goUp(self):
        self.liftArea.requestGoUp()
        self.givenDestination = elevatorDirection.up
    
    # person requests to go down
    def goDown(self):
        self.liftArea.requestGoDown()
        self.givenDestination = elevatorDirection.down
    
    # request lift to go to a specific level
    def goToLevel(self, destination: int):
        if self in self.liftManager.getCurrentPeople():
            # attempts to add the new destination through the lift interface
            self.liftManager.addDestination(destination)
            # save the successful given dsetination
            self.givenDestination = destination

    # TODO: Exiting lift is done automatically, by the lift manager letting everyone know what level we have gone to.
    def exitLift(self):
        pass

    # TODO: PEOPLE WHO HAVEN'T CLICKED UP OR DOWN WILL NOT BE AUTOMATICLALY PUT ON LIFTS, AS IT IS DONE THROUGH THE AREA
    def enterLift(self):
        pass
    


'''
Lift is a simple object. Just holds attributes about itself basically
'''
class Lift:
    def __init__(self):
        self.level = 1
        self.maxCapacity = 10
        self.currentCapacity = 0
        self.currentPeople: list[Person] = []    

'''
The LiftManager class extends lift, since it needs to access its variables all the time, but acts more as a manager/scheduler of the lift itself.
'''
class LiftManager(Lift):
    # initialise the lift manager
    def __init__(self, numLevels: int):
        super.__init__
        self.liftQueue = []
        self.nextDestination: int = -1
        self.upOrDown: str = ""
        #initialise to empty list, going from floor level to the LiftArea associated with it
        self.liftAreas = dict()
        self.numLevels = numLevels
        self.setup_liftAreas()
    
    def getCurrentPeople(self):
        return self.currentPeople.copy

    # areas represent the spaces that are outside of the lift where you can call the lift
    def setup_liftAreas(self):
        # add to the dictionary of area's the area for each level
        for i in range(1, self.numLevels+1):
            self.liftAreas[i] = Area(i, self)

    # add person to lift if there is space
    def getOnLift(self, person: Person):
        if (len(self.currentPeople) < self.currentCapacity):
            self.currentPeople.append(person)
            return True
        return False

    # get person off lift
    def getOffLift(self, person: Person):
        try:
            self.currentPeople.remove(person)
        except:
            print("Person not in lift")

    # destination currently adds it last
    def addDestination(self, destination: int):
        self.liftQueue.append(destination)
    
    # this function runs indefinitely, and moves the lift based on the queue
    def functionThatMovesLift(self):
        # run indefinitely
        while True:
            if (self.nextDestination != -1):
                # go to this level
                # is lift at its destionation level right now
                if (self.nextDestination == self.level):
                    # lift arrived at level
                    # alert everyone on lift that lift is at this level
                    for person in self.currentPeople:
                        if person.givenDestination == self.level:
                            # person gets off lift and join's lift area
                            self.getOffLift(person)
                            self.liftAreas[self.level].joinLiftArea(person)

                    # alert everyone in lift area at this level lift is here
                    self.liftAreas[self.level].alertPeopleLiftHere()
                elif (self.nextDestination > self.level):
                    # going up to level
                    print("going up past " + str(self.level))
                    self.level += 1
                    
                else:
                    #going down to level
                    print("going down past " + str(self.level))
                    self.level -= 1
                    print("going down past " + self.level)
            elif (len(self.liftQueue) > 0):
                self.nextDestination = self.liftQueue.pop()
                print(" new target acquired ")
            else:
                print("waiting idle...")
                time.sleep(1)


'''
An area is an area where you can request lifts
'''
class Area:
    def __init__(self, level: int, liftManager: LiftManager):
        self.level = level
        self.peopleInArea: list[Person] = []
        self.goUpSelected = False
        self.goDownSelected = False
        self.liftManager = liftManager
    
    def requestGoUp(self):
        if not (self.goUpSelected):
            # add this level as a desetination it has to go to
            self.liftManager.addDestination(self.level)
            self.goUpSelected = True
    
    def requestGoDown(self):
        if not (self.goDownSelected):
            # add this level as a destination it's going to
            self.liftManager.addDestination(self.level)
            self.goDownSelected = True

    def joinArea(self, person: Person):
        self.peopleInArea.append(person)
    
    def leaveArea(self, person: Person):
        self.peopleInArea.remove(person)
    
    # this function is run when the lift has arrived at this area
    def alertPeopleLiftHere(self):
        for person in self.peopleInArea:
            # if the person has selected up or down, and the persons direction selection matches that of the lift, or the lift has no given direction
            if person.upOrDown != elevatorDirection.noDestination and (person.upOrDown == self.liftManager.upOrDown or self.liftManager.upOrDown == elevatorDirection.noDestination):
                # attempt to add person
                if (self.liftManager.getOnLift(person) == True):
                    # remove person from this area, they are on lift
                    self.leaveArea(person)
                    print(person.__str__ +  " got on lift successfully")
                else:
                    print("Lift was full. Could not add person")
        
        # reset the go up and down buttons to not being pressed
        self.goDownSelected = False
        self.goUpSelected = True


if __name__ == "__main__":
    print("hello world")


    # create lift1 manager
    numLevels: int = 3
    lift1Manager = LiftManager(numLevels=3)

    # threadify the scheduler
    # scheduler_thread = threading.Thread(target=lift1Manager.functionThatMovesLift, name="scheduler")
    # scheduler_thread.start()
    

    people: list[Person] = []
    # create 3 people
    for i in range(1,numLevels+1):
        people.append(Person(i, name=i, liftManager=lift1Manager, startingLiftArea=lift1Manager.liftAreas[i]))
    
    # add people to their respective area
    for i in range(0, len(people)):
        lift1Manager.liftAreas[i+1].joinArea(people[i])

    # person2 and  3 requests lift
    people[1].goUp()
    people[2].goDown()
    people[1].goUp()
    print(lift1Manager.liftQueue)



    # lift should move up to level 2, open and let person 2 know to get on.

    # person 2 selects go to level 3

    # lift goes to level 3, person 2 gets out and enters level 3 area.

    # person 1 requests lift

    # lift comes down to level 1



