from Modules.AI.Genetics.genetics import AlbumWriter, EvolutonaryAlgorithm
from Modules.General.general_tools import PathsManager
from Modules.Settings.settings import SETTINGS
from Modules.Settings.set_up_manager import SetUpManager

# Set number of first experiment.
numberOfFirstExperiment = 512

class SolutionFinder:

    # Notice: "numberOfExperiment" will be incremented for next experiments in the same script.
    numberOfExperiment = numberOfFirstExperiment

    @classmethod
    def PerformExperiment(cls, poolNumber = None):

        # Set up environment
        SetUpManager.SetUp()

        # Load population if experiment doesn't start from the random beginning.
        if poolNumber is not None:
            EvolutonaryAlgorithm.LoadPopulation("data/genePools/pool" + str(poolNumber) + ".txt")

        # Perform experiment
        EvolutonaryAlgorithm.Execute()

        # Create album
        album = AlbumWriter.AlbumFromAlgorithm(EvolutonaryAlgorithm)

        # Save results
        cls.SaveAlbum(album)
        cls.SaveGenePool()
        cls.AddSummaryToRegistry()

        # Increment counter (next experiment will have another number)
        cls.numberOfExperiment += 1

    @classmethod
    def SaveAlbum(cls, album):

        album.SaveToFile(PathsManager.GetPath("albums", "album" + str(cls.numberOfExperiment) + ".txt"))

    @classmethod
    def SaveGenePool(cls):

        EvolutonaryAlgorithm.SavePopulation(PathsManager.mainPath + "Scripts/Data/genePools/pool" + str(cls.numberOfExperiment) + ".txt")


    @classmethod
    def AddSummaryToRegistry(cls):

        with open(PathsManager.mainPath + "Scripts/data/registry.txt", "a") as file:

            # Write number of experiment.
            file.write("album no: " + str(cls.numberOfExperiment) + " ")

            # Write optional information. Typically, parameters which are tuned at this time.
            # Here is an example:
            # file.write("after" + str(SETTINGS.GENETICS.SIZE_OF_POPULATION_AFTER_SELECTION) + " ")
            # file.write("before" + str(SETTINGS.GENETICS.SIZE_OF_POPULATION_BEFORE_SELECTION) + " ")

            # Write average and best fitnesse.
            file.write("avg" + str(EvolutonaryAlgorithm.logbook.select("avg")[-1]) + " ")
            file.write("best" + str(EvolutonaryAlgorithm.logbook.select("max")[-1]) + "\n")

            file.close()

# At this place you can change parameters of experiment, which are in "Settings" module by default.
SETTINGS.GENETICS.CROSSING.PROBABILITY = 0.5
SETTINGS.GENETICS.MUTATION.PROBABILITY = 0.2

SETTINGS.GENETICS.SIZE_OF_POPULATION_AFTER_SELECTION = 30
SETTINGS.GENETICS.SIZE_OF_POPULATION_BEFORE_SELECTION = 60
SETTINGS.GENETICS.NUMBER_OF_GENERATIONS = 10

# Perform experiment as many times as you want by using line below multiple times.
SolutionFinder.PerformExperiment()

