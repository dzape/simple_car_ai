from Modules.Simulation.geometry import Vector, MobileRotatedRect
from Modules.General.general_types import Move
import random

class CarTransformCalculator:

    deltaTime = None
    sideAccelerationFactor = None
    longitudinalAccelerationFactor = None
    voluntaryChangeOfSlipAngle = None
    changeOfSlipAngleDuringReturning = None
    maximalSlipAngle = None


    @classmethod
    def NewTransform(cls, car, nextMove):


        # Cases when vehicle want to change intensity of turning (turning more or less). We need to check if it is not
        # turned to its limits.
        if nextMove == Move.LEFT and car.slipAngle > -cls.maximalSlipAngle:
            car.slipAngle -= cls.voluntaryChangeOfSlipAngle
        elif nextMove == Move.RIGHT and car.slipAngle < cls.maximalSlipAngle:
            car.slipAngle += cls.voluntaryChangeOfSlipAngle
        else:
            # If vehicle don't want to change the intensity of turning it will go back to driving straight ahead by default,
            if car.slipAngle > 0:
                car.slipAngle -= cls.changeOfSlipAngleDuringReturning
            elif car.slipAngle < 0:
                car.slipAngle += cls.changeOfSlipAngleDuringReturning

        # Define some abbreviations
        f_s = cls.sideAccelerationFactor
        f_l = cls.longitudinalAccelerationFactor
        v_0 = cls.velocityValue

        # Determine acceleration
        sideAcceleration = Vector(f_s * car.slipAngle, 0).rotate(-car.rot + 90)
        longitudinalAcceleration = Vector(f_l * (v_0 - car.velocity.length()), 0).rotate(-car.rot)
        resultantAcceleration = sideAcceleration + longitudinalAcceleration

        # Determine transform parameters (we determined acceleration before. It was necessary for this step)
        newVelocity = car.velocity + cls.deltaTime * resultantAcceleration
        newPos = car.pos + cls.deltaTime * car.velocity

        return newPos, newVelocity.angle, newVelocity


class BaseCar(MobileRotatedRect):

    map = None
    original_rect = None
    maximalRandomRotChange = None
    velocityValue = None

    def __init__(self):
        super(BaseCar, self).__init__()

        # Each of cars has the same original_rect. See: class description.
        self.original_rect = BaseCar.original_rect

        self.pos = None
        self.rot = None


        self.transformCalculator = CarTransformCalculator()

        self.nextMove = None
        self.ifCollided = False

        self.velocity = None
        self.slipAngle = 0


    def InitialVelocity(self):

        return Vector(self.__class__.velocityValue, 0).rotate(-self.rot)


    def PerformStep(self):

        self.pos, self.rot, self.velocity = self.transformCalculator.NewTransform(self, self.nextMove)

        # Necessary for algorithms to work properly
        self.UpdateCorners()

    def PlaceOnTheMap(self):

        # Place at the "START" of the chosen map. Notice that we change primary rotation slightly.
        self.pos = self.__class__.map.carSuggestedPos
        self.rot = self.__class__.map.carSuggestedRot + random.randint(-self.__class__.maximalRandomRotChange, self.__class__.maximalRandomRotChange)

        # Necessary for algorithms to work properly
        self.CreateCorners()

        # Initialize rest of transform parameters.
        self.velocity = self.InitialVelocity()
        self.slipAngle = 0


    def CheckCollisions(self):

        self.ifCollided = self.CollideWithSetOfRRects(self.__class__.map.listOfBarriers)