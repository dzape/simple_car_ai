import os
import pygame as pg
from Modules.Simulation.geometry import Vector


class PathsManager:

    mainPath = None
    files = {}
    directories = {}

    @classmethod
    def AddFile(cls, key, relativePath):

        cls.files[key] = cls.mainPath + relativePath

    @classmethod
    def AddDirectory(cls, key, relativePath):

        cls.directories[key] = cls.mainPath + relativePath

    @classmethod
    def GetPath(cls, key, filename=None):

        if filename is None:
            return cls.files[key]
        else:
            return cls.directories[key] + filename

class ImagesManager:

    images = {}

    @classmethod
    def Initialize(cls):

        pg.display.set_mode((1, 1))

    @classmethod
    def AddImage(cls, key, path, scale=1):

        if scale == 1:
            cls.images[key] = pg.image.load(path).convert_alpha()
        else:
            cls.images[key] = cls.scaledImage(pg.image.load(path).convert_alpha(), scale)

    @classmethod
    def GetImage(cls, key):

        return cls.images[key]

    @classmethod
    def scaledImage(cls, image, scale):

        # We can scale in two dimensions. Statements below solves problem when "scale" argument was passed as single
        # float. In that case, we scale image in two dimensions keeping the proportions.
        try:
            scale[0]
        except TypeError:
            scale = Vector(scale, scale)

        newSize = Vector(image.get_rect().size).ScaledByVector(scale)
        return pg.transform.scale(image, newSize.asInt())

    @classmethod
    def rotatedImage(cls, image, rot):

        return pg.transform.rotate(image, rot)

    @classmethod
    def transformedImage(cls, image, scale, rot):

        intermediateImage = cls.scaledImage(image, scale)
        return cls.rotatedImage(intermediateImage, rot)


class FilesManager:

    @classmethod
    def LinesFromFile(cls, filename):

        with open(filename, 'rt') as file:
            lines = file.readlines()
            return lines

    @classmethod
    def AddLineToFile(cls, line, filename):

        with open(filename, "a") as file:
            file.write(line + "\n")
            file.close()

    @classmethod
    def ClearFile(cls, filename):

        file = open(filename, "w")
        file.close()


class BuiltInTypesConverter:

    @classmethod
    def StringToInts(cls, line):

        return [int(element) for element in line.split()]

    @classmethod
    def StringToFloats(cls, string):

        return [float(element) for element in string.split()]

    @classmethod
    def IntsToString(cls, ints):

        result = ""
        for element in ints:
            result = result + str(int(element)) + " "
        return result

    @classmethod
    def FloatsToString(cls, floats):

        result = ""
        for element in floats:
            result = result + str(element) + " "
        return result

