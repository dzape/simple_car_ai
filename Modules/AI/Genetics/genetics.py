from Modules.General.general_tools import BuiltInTypesConverter, FilesManager
from Modules.Simulation.data_containers import Album, Track, BlackBox
from deap import base, creator, tools
from deap.algorithms import varOr
import random
import copy




class Pattern(list):

    length = None

    wageMin = None
    wageMax = None

    def __init__(self, *args):
        list.__init__(self, *args)
        self.fitness = creator.FitnessMax()
        self.blackBox = BlackBox()

    @property
    def wages(self):
        return self

    @classmethod
    def RandomWage(cls):

        return random.uniform(cls.wageMin, cls.wageMax)

    @classmethod
    def CalculateLength(cls, architecture):

        result = 0

        # To understand how lines written below works you need to understand how neural networks are constructed.
        # After that, it is easy mathematical exercise to determine number of connections depending on architecture
        # (number of layers, number of neurons per each layer).
        for index in range(len(architecture)-1):
            result += architecture[index] * architecture[index+1]

        result += sum(architecture)
        result -= architecture[0]

        cls.length = result



class FitnessEvaluator:

    verbose = False
    car = None

    @classmethod
    def EvaluatePattern(cls, pattern):

        # Set pattern (individual) on object that will allow to measure fitness.
        cls.car.brain.SetPattern(pattern)

        # Proper simulation.
        cls.car.PerformDrive()

        # Copy record of drive. REMEMBER: there are many patterns and only one car, so we have to do that.
        pattern.blackBox = cls.car.blackBox

        # See: "verbose" description in class documentation.
        if cls.verbose:
            print("next", cls.car.stepCounter)

        return copy.deepcopy(cls.car.stepCounter),



class EvolutonaryAlgorithm:

    startFromRandomPopulation = True
    startingPopulation = None

    toolbox = base.Toolbox()
    lverbose = False

    #INDIVIDUALS
    lengthOfIndividual = None
    geneRandomizingFunction = None

    #LAWS
    fitnessEvaluator = FitnessEvaluator

    probabilityOfCrossing = None
    crossingMethod = None
    crossingParameters = {}

    probabilityOfMutation = None
    mutationMethod = None
    mutationParameters = {}

    selectionMethod = None
    selectionParameters = {}

    #MAKRO
    paramMu = None
    paramLambda = None
    numberOfGenerations = None


    #STATISTICS
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    dictWithStatistics = {}

    #RESULTS
    listOfPopulations = None
    logbook = None
    finalPopulation = None

    @classmethod
    def Prepare(cls):

        # Set method which will choose genes.
        cls.toolbox.register("attr_float", cls.geneRandomizingFunction)

        # A necessary line that we would be able to create individuals
        cls.toolbox.register("individual", tools.initRepeat, Pattern, cls.toolbox.attr_float, n=cls.lengthOfIndividual)

        # A necessary line that we would be able to create populations.
        cls.toolbox.register("population", tools.initRepeat, list, cls.toolbox.individual)

        # Create methods which will be used during algorithm.
        cls.toolbox.register("evaluate", cls.fitnessEvaluator.EvaluatePattern)
        cls.toolbox.register("mate", cls.crossingMethod, **cls.crossingParameters)
        cls.toolbox.register("mutate", cls.mutationMethod, **cls.mutationParameters)
        cls.toolbox.register("select", cls.selectionMethod, **cls.selectionParameters)

        # Create set of statistics.
        for name, method in cls.dictWithStatistics.items():
            cls.stats.register(name, method)

    @classmethod
    def LoadPopulation(cls, filename):


        lines = FilesManager.LinesFromFile(filename)
        cls.startingPopulation = cls.toolbox.population(len(lines))
        for individual, line in zip(cls.startingPopulation, lines):
            importedWages = BuiltInTypesConverter.StringToFloats(line)
            for _ in range(len(individual)):
                # Remember that "Pattern" derives from "list", so we need to use old-fashioned style.
                individual.wages[_] = importedWages[_]

        # Starting population won't be randomly generated.
        cls.startFromRandomPopulation = False


    @classmethod
    def SavePopulation(cls, filename):

        FilesManager.ClearFile(filename)

        for individual in cls.finalPopulation:
            nextLine = BuiltInTypesConverter.FloatsToString(individual.wages)
            FilesManager.AddLineToFile(nextLine, filename)


    @classmethod
    def Execute(cls):

        # Creates randomly generated population, if none has been loaded.
        if cls.startFromRandomPopulation:
            cls.startingPopulation = cls.toolbox.population(cls.paramMu)

        # The core of algorithm
        cls.eaMuCommaLambda(population=cls.startingPopulation,
                            toolbox=cls.toolbox,
                            mu=cls.paramMu,
                            lambda_=cls.paramLambda,
                            cxpb=cls.probabilityOfCrossing,
                            mutpb=cls.probabilityOfMutation,
                            ngen=cls.numberOfGenerations,
                            stats=cls.stats)

        # Reset flag for next execution.
        cls.startFromRandomPopulation = True

    @classmethod
    def eaMuCommaLambda(cls, population, toolbox, mu, lambda_, cxpb, mutpb, ngen, stats=None):

        assert lambda_ >= mu, "lambda must be greater or equal to mu."

        # Create new logbook
        cls.logbook = tools.Logbook()
        cls.logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the statistics with the new population
        record = stats.compile(population) if stats is not None else {}
        cls.logbook.record(gen=0, nevals=len(invalid_ind), **record)

        cls.listOfPopulations = []
        cls.listOfPopulations.append(copy.deepcopy(population))

        # Begin the generational process
        for gen in range(1, ngen + 1):
            if cls.lverbose:
                print("generation no:", gen)

            # Vary the population
            offspring = varOr(population, toolbox, lambda_, cxpb, mutpb)

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Select the next generation population
            population[:] = toolbox.select(offspring, mu)

            # Update the statistics with the new population
            record = stats.compile(population) if stats is not None else {}
            cls.logbook.record(gen=gen, nevals=len(invalid_ind), **record)

            cls.listOfPopulations.append(copy.deepcopy(population))

        # Get final population
        cls.finalPopulation = population


class AlbumWriter:

    @classmethod
    def AlbumFromAlgorithm(cls, algorithm):

        album = Album()

        for population in algorithm.listOfPopulations:
            track = Track()
            for pattern in population:
                track.AddBlackBox(pattern.blackBox)
            album.AddTrack(track)

        return album


