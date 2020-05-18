from Modules.AI.NeuralNetworks.neural_networks import Brain
from Modules.Simulation.data_containers import BlackBox, CarRecord
from Modules.Simulation.car_radar_equipped import RadarEquippedCar
import copy




class TrainableCar(RadarEquippedCar):

    lengthOfCompleteDrive = None


    def __init__(self):
        super(TrainableCar, self).__init__()
        self.brain = Brain()
        self.record = CarRecord(self.radar.record)
        self.blackBox = BlackBox()
        self.stepCounter = 0


    def PerformStep(self):
        ''' Method which is looped during simulation. It contains all necessary methods to drive autonomously.
        '''
        self.UseRadar()
        self.CalculateNextMove()
        super(TrainableCar, self).PerformStep()
        self.CheckCollisions()


    def PerformDrive(self):

        # Initializion necessary before complex loop
        self.PrepareToDrive()

        # One step per iteration
        while self.ifCollided == False:
            self.PerformStep()
            self.Save()
            self.stepCounter += 1

            # Check if car is on the end of race track.
            if self.stepCounter == self.__class__.lengthOfCompleteDrive:
                break


    def PrepareToDrive(self):
        ''' Decorator
        '''
        self.PlaceOnTheMap()
        self.ResetMemory()


    def ResetMemory(self):

        # Reset black box
        self.blackBox = BlackBox()

        # Reset other attributes
        self.ifCollided = False
        self.stepCounter = 0

    def Save(self):
        ''' Save current status on record.
        '''
        self.record.pos = self.pos
        self.record.rot = self.rot
        self.radar.Save()

        # We need copy, because "record" attribute is changing dynamically.
        self.blackBox.AddCarRecord(copy.deepcopy(self.record))

    def CalculateNextMove(self):
        ''' Method which choosing next move using brain. "Brain.CalculateMove()" could be potentially complex method, so
            we need to pass all car's attributes using "self".
        '''
        self.nextMove = self.brain.CalculateMove(self)
