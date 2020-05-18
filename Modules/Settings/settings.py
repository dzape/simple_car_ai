from Modules.General.general_types import Colors
from deap import tools
import numpy as np


class SETTINGS:
    class COMMON_FOR_MANY:
        NUMBER_OF_RANGEFINDERS = 3
    ###############################

    class BASE_CAR:
        DElTA_TIME = 0.033
        VALUE_OF_VELOCITY = 140
        SIDE_ACCELERATION_FACTOR = 4
        LONGITUDINAL_ACCELERATION_FACTOR = 10
        VOLUNTARY_CHANGE_OF_SLIP_ANGLE = 1
        CHANGE_OF_SLIP_ANGLE_DURING_RETURNING = 0.6
        MAXIMAL_SLIP_ANGLE = 25

        MAXIMAL_RANDOM_ROTATION_CHANGE = 20


    class RADAR_EQUIPPED_CAR:
        RADAR_COEFFICIENT = 84 / 128
        RANGE_OF_RADAR = 100

    class TRAINABLE_CAR:
        pass

    class DISPLAYER:
        MESH_COLOR = Colors.LIGHTGREY
        BACKGROUND_COLOR = Colors.DARKGREY
        FRAMES_PER_SECOND = 100
        WINDOW_WIDTH = 1280

        WINDOW_HEIGHT = 720

        CAPTION_COLOR = Colors.LIGHTBROWN
        CAPTION_FONT_NAME = "timesnewroman"
        CAPTION_FONT_SIZE = 27

    class GENETICS:
        SIZE_OF_POPULATION_AFTER_SELECTION = 30
        SIZE_OF_POPULATION_BEFORE_SELECTION = 60
        NUMBER_OF_GENERATIONS = 45

        class CROSSING:
            PROBABILITY = 0.5
            METHOD = tools.cxTwoPoints

        class MUTATION:
            PROBABILITY = 0.2
            METHOD = tools.mutGaussian
            PROBABILITY_OF_ATTRIBUTE_MUTATION = 0.2
            class GAUSSIAN:
                MEAN_OF_THE_DISTRIBUTION = 0
                STD_DEVIATION_OF_THE_DISTRIBUTION = 1

        class SELECTION:
            METHOD = tools.selTournament
            class TOURNAMENT:
                SIZE = 3

        class STATISTICS:
            MIN = np.min
            MAX = np.max
            AVERAGE = np.mean

    class GEOMETRY:
        pass

    class MAP:
        MARGIN = 50

    class NEURAL_NETWORKS:
        NN_ARCHITECTURE_DEEP_FACTORS = [4, 3]
        WAGE_MIN, WAGE_MAX = -1., 1.

    class SPRITES:
        SMALL_SQUARE_SIZE = (12, 12)
        class COLORS:
            RADAR_COLOR = Colors.GOLD
            RANGEFINDER_COLOR = Colors.YELLOW


