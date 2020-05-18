from Modules.General.general_tools import ImagesManager
import pygame as pg


#virtual
class MoreIntuitiveSprite(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)

    @property
    def pos(self):
        return self.rect.center

    @pos.setter
    def pos(self, value):
        self.rect.center = value

#virtual
class SSmallSquare(MoreIntuitiveSprite):

    color = None
    size = None

    def __init__(self):
        super(SSmallSquare, self).__init__()
        self.image = pg.Surface(SSmallSquare.size)
        self.image.fill(self.__class__.color)
        self.rect = self.image.get_rect()


class SRangefinder(SSmallSquare):

    pass

class SRadar(SSmallSquare):

    pass


#virtual
class SRotatableRect(MoreIntuitiveSprite):

    baseImage = None

    def __init__(self):
        super(SRotatableRect, self).__init__()
        self.rot = None
        self.image = self.__class__.baseImage
        self.rect = self.image.get_rect()

    @property
    def rectSize(self):
        return None

    @rectSize.setter
    def rectSize(self, value):

        buff = self.rect.center
        self.rect = value
        self.rect.center = buff


class SBarrier(SRotatableRect):

    def __init__(self):
        super(SBarrier, self).__init__()

    def Create(self, barrier):

        # Translate sprite to the right place.
        self.pos = barrier.pos

        # Make sprite has proper rotation and scale.
        self.CreateImage(barrier.rot, barrier.scale)

    def CreateImage(self, rot, scale):

        # Create object's image by transforming base image for the class.
        self.image = ImagesManager.transformedImage(self.__class__.baseImage, scale, rot)

        # Set size of "rect" attribute. Notice, that position of "rect" attribute has been set before.
        self.rectSize = self.image.get_rect()



class SCar(SRotatableRect):

    def __init__(self):
        super(SCar, self).__init__()


    def Update(self, record):

        # Translate sprite to the right place.
        self.pos = record.pos

        # Make sprite has proper image.
        self.CreateImage(record.rot)


    def CreateImage(self, rot):

        # Create object's image by transforming base image for the class.
        self.image = ImagesManager.rotatedImage(self.__class__.baseImage, rot)

        # Set size of "rect" attribute. Notice, that position of "rect" attribute was set before.
        self.rectSize = self.image.get_rect()

