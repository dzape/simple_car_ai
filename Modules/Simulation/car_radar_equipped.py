from Modules.Simulation.data_containers import RangefinderRecord, RadarRecord
from Modules.Simulation.car_base import BaseCar
from Modules.Simulation.geometry import Point, Vector,  Ray
import numpy as np





class RangefinderTransformCalculator:

    listOfRelativeRots = []


    @classmethod
    def CalculateRelativeRots(cls, lrange, numberOfRangefinders):

        cls.listOfRelativeRots = []
        for rot in np.linspace(-lrange/2, lrange/2, numberOfRangefinders):
            cls.listOfRelativeRots.append(rot)

    @classmethod
    def NewTransform(cls, radar, number):

        newPos = radar.pos
        newRot = radar.rot + cls.listOfRelativeRots[number]

        return newPos, newRot

class Rangefinder:

    def __init__(self, number=None):
        self.pos = None
        self.rot = None
        self.posOfBarrier = None
        self.distance = None
        self.record = RangefinderRecord()
        self.number = number

    def Save(self):
        ''' Save current status on record.
        '''
        self.record.pos = self.pos
        self.record.rot = self.rot
        self.record.posOfBarrier = self.posOfBarrier

    def MeasureDistance(self):
        ''' Calculate how far is car from the environment in direction designated by rangefinder.
        '''
        # Create ray from car in direction designated by rangefinder
        ray = Ray(Point(self.pos), rot=self.rot)

        # "SetOfRects" (elements of environment) has to be set before following line. That "set" is common
        # for all rangefinders and all moments, so this way has better performance.
        self.posOfBarrier = ray.BeginningProjectionOnSetOfRects()

        # Calculate distance. Distance is None when there is no point on the ray.
        try:
            self.distance = self.pos.Distance(self.posOfBarrier)
        except AttributeError:
            self.distance = None

class RadarTransformCalculator:

    originalRelativePos = None

    @classmethod
    def CalculateOriginalRelativePos(cls, originalRectOfCar, coeff):

        # Calculate position of radar if topleft(!) corner of car is placed on the beginning of coordinate system.
        originalPos = Vector(coeff * originalRectOfCar.width, 0.5 * originalRectOfCar.height)

        # Calculate position of radar if center(!) of car is placed on the beginning of coordinate system.
        cls.originalRelativePos = originalPos - originalRectOfCar.center

    @classmethod
    def NewTransform(cls, car):

        # To understand line below read definition of "originalRelativePos" and description in
        # "CalculateOriginalRelativePos" method
        newPos = cls.originalRelativePos.rotate(-car.rot) + car.pos

        return newPos, car.rot

class Radar:

    numberOfRangefinders = 3

    def __init__(self):
        self.pos = None
        self.rot = None

        # Create rangefinders.
        self.listOfRangefinders = [Rangefinder(_) for _ in range(self.__class__.numberOfRangefinders)]

        # Attach rangefinders's records to radar's record.
        self.record = RadarRecord(self.listOfRangefinders)

    def Save(self):
        ''' Save current status on record.
        '''
        self.record.pos = self.pos
        self.record.rot = self.rot

        for rangefinder in self.listOfRangefinders:
            rangefinder.Save()

    def MoveRangefinders(self):
        ''' We use this method from here (not from rangefinder), because its need radar's attributes (remember that
        radar is superior to rangefinders).
        '''

        for rangefinder in self.listOfRangefinders:
            rangefinder.pos, rangefinder.rot = RangefinderTransformCalculator.NewTransform(self, rangefinder.number)

    def MeasureDistances(self):
        ''' Take measurement from each rangefinder
        '''

        for rangeFinder in self.listOfRangefinders:
            rangeFinder.MeasureDistance()




class RadarEquippedCar(BaseCar):

    def __init__(self):
        super(RadarEquippedCar, self).__init__()
        self.radar = Radar()

    def PerformStep(self):
        super(RadarEquippedCar, self).PerformStep()

        # Radar also is a object, so we need to move it.
        self.MoveRadar()

    def PlaceOnTheMap(self):
        super(RadarEquippedCar, self).PlaceOnTheMap()

        # Radar also is a object, so we need to move it.
        self.MoveRadar()

    def MoveRadar(self):
        ''' Move all object which are installed on the car.
        '''

        #Move radar
        self.radar.pos, self.radar.rot = RadarTransformCalculator.NewTransform(self)

        #Move rangefinders
        self.radar.MoveRangefinders()

    def UseRadar(self):
        ''' Decorator
        '''
        self.radar.MeasureDistances()