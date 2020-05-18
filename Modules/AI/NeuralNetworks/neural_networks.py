from keras.models import Sequential
from keras.layers.core import Dense
from Modules.General.general_types import Move
import numpy as np


class InputTransformator:

    inputArchitecturalFactor = None

    @classmethod
    def TransformedInput(cls, car):

        # Data will consist of distances between car and environment.
        listOfDistances = []
        for rangeFinder in car.radar.listOfRangefinders:
            listOfDistances.append(rangeFinder.distance)

        # Return as a structure which KERAS accepts.
        return np.array([listOfDistances])


class OutputTransformator:

    outputArchitecturalFactor = 3

    @classmethod
    def TransformedOutput(cls, output):

        # Get proper output from KERAS's output structure.
        output = output[0]

        # The decision depends on which element of output is maximal.
        choice = np.argmax(output)
        if choice == 0:
            result = Move.RIGHT
        elif choice == 1:
            result = Move.NONE
        elif choice == 2:
            result = Move.LEFT

        return result


class Brain:

    neuralNetwork = None
    inputTransformator = None
    outputTransformator = None
    deepArchitecturalFactors = []

    @classmethod
    def Create(cls, inputTransformator, outputTransformator):

        # Set transformators
        cls.inputTransformator = inputTransformator
        cls.outputTransformator = outputTransformator

        # Create full architecture from all necessary data.
        architecture = [inputTransformator.inputArchitecturalFactor] + cls.deepArchitecturalFactors + [outputTransformator.outputArchitecturalFactor]

        # Create right neural network.
        cls.CreateNeuralNetwork(architecture)

    @classmethod
    def CreateNeuralNetwork(cls, architecture):

        # Initialize neural network. Notice that first element from architecture is passed as "input_shape", not as a
        # number of neurons in layer.
        cls.neuralNetwork = Sequential([Dense(architecture[1], input_shape=(architecture[0],), activation='relu'),
                                         Dense(architecture[2], activation='relu'),
                                         Dense(architecture[3], activation='softmax')])

    def SetPattern(self, pattern):

        # Get weights from neural network in order to get its structure shape.
        weights = self.neuralNetwork.get_weights()

        # Put elements from list of weights (pattern.wages) into appropriate slots (in KERAS's "weights" structure).
        index = 0
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                try:
                    for k in range(len(weights[i][j])):
                        weights[i][j][k] = pattern.wages[index]
                        index += 1
                except:
                    weights[i][j] = pattern.wages[index]
                    index += 1

        # Set changed weights to neural network.
        self.neuralNetwork.set_weights(weights)

    def CalculateMove(self, car):

        # Conduct signal through input transformator
        input = self.inputTransformator.TransformedInput(car)

        # Conduct signal through neural network
        output = self.neuralNetwork.predict(input)

        # Conduct signal through output transformator
        move = self.outputTransformator.TransformedOutput(output)

        return move
