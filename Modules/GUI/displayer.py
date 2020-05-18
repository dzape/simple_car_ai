from Modules.GUI.sprites import SRadar, SRangefinder, SBarrier, SCar
import pygame as pg


class CarRelatedSpritesContainer:

    numberOfSrangefinders = None

    def __init__(self):
        self.scar = SCar()
        self.sradar = SRadar()
        self.listOfSrangefinders = [SRangefinder() for _ in range(self.__class__.numberOfSrangefinders)]

        self.frameNumber = None
        self.blackBox = None

    @property
    def sprites(self):
        return None

    @sprites.getter
    def sprites(self):

        return [self.scar, self.sradar] + self.listOfSrangefinders

    def SetNewBlackBox(self, blackBox):

        self.frameNumber = 0
        self.blackBox = blackBox

    def LoadFromNextRecord(self):

        try:
            self.LoadFromRecord(self.blackBox.listOfCarRecords[self.frameNumber])
            self.frameNumber += 1
        except IndexError:
            pass

    def LoadFromRecord(self, record):

        # Update sprite of car
        self.scar.Update(record)

        # Update sprite of radar
        self.sradar.pos = record.radarRecord.pos

        # Update sprites of rangefinders.
        for srangefinder, rangefinderRecord in zip(self.listOfSrangefinders, record.radarRecord.listOfRangefinderRecords):
            srangefinder.pos = rangefinderRecord.posOfBarrier

class SpritesManager:

    sprites = None
    listOfCRSContainers = []
    bestCarContainer = None

    @classmethod
    def CreateSBarriers(cls, map):

        # Create barriers
        listOfSBarriers = [SBarrier() for _ in map.listOfBarriers]
        for sbarrier, barrier in zip(listOfSBarriers, map.listOfBarriers):
            sbarrier.Create(barrier)

        # Add them to set of all displayed sprites.
        cls.sprites.add(listOfSBarriers)

    @classmethod
    def CreateCarRelatedSprites(cls, numberOfBlackBoxes):

        # Create sprites related with cars. Notice than at the beginning sprites are empty (They will be filled before
        # first frame).
        cls.listOfCRSContainers = [CarRelatedSpritesContainer() for _ in range(numberOfBlackBoxes)]

        # Add them to set of all displayed sprites.
        for crsContainer in cls.listOfCRSContainers:
            cls.sprites.add(crsContainer.sprites)

    @classmethod
    def SetNewTrack(cls, track):

        # Set new black boxes for containers
        for crsContainer, blackBox in zip(cls.listOfCRSContainers, track.listOfBlackBoxes):
            crsContainer.SetNewBlackBox(blackBox)

        # Find container related with best car. See: class description.
        # Remember that although container was initialized only at the beginning of play, their black boxes are changing.
        # So in every track another container has the longest black box. Each time we have to find it.
        cls.FindBestCarContainer()

    @classmethod
    def FindBestCarContainer(cls):

        # Create dictionary which connect containers with lengths of theirs black boxes.
        lengthsToContainers = dict((container, container.blackBox.numberOfCarRecords) for container in cls.listOfCRSContainers)

        # Get container with longest black box.
        cls.bestCarContainer = max(lengthsToContainers, key=lengthsToContainers.get)

    @classmethod
    def UpdateCarRelatedSprites(cls):

        for crsContainer in cls.listOfCRSContainers:
            crsContainer.LoadFromNextRecord()


class Camera:

    mapSize = None
    windowSize = None

    restrictingRect = None
    targetRelativePos = None
    topleftCornerPos = None

    @classmethod
    def Create(cls):

        cls.restrictingRect = pg.Rect(0, 0, cls.mapSize.x - cls.windowSize.x, cls.mapSize.y - cls.windowSize.y)
        cls.targetRelativePos = 0.5 * cls.windowSize

    @classmethod
    def FocusOn(cls, target):

        # Ultimately target should be at the center of view.
        cls.topleftCornerPos = target.rect.center - cls.targetRelativePos

        # If we are close to the border we need to move view towards center of the map. For this purpose we are using
        # restricting rectangle.
        if cls.topleftCornerPos.x < cls.restrictingRect.left:
            cls.topleftCornerPos.x = cls.restrictingRect.left
        elif cls.topleftCornerPos.x > cls.restrictingRect.right:
            cls.topleftCornerPos.x = cls.restrictingRect.right

        if cls.topleftCornerPos.y < cls.restrictingRect.top:
            cls.topleftCornerPos.y = cls.restrictingRect.top
        elif cls.topleftCornerPos.y > cls.restrictingRect.bottom:
            cls.topleftCornerPos.y = cls.restrictingRect.bottom

    @classmethod
    def relativePos(cls, sprite):

        return sprite.rect.topleft - cls.topleftCornerPos




class Displayer:

    sprites = pg.sprite.Group()
    spritesManager = SpritesManager

    camera = Camera

    clock = pg.time.Clock()
    framesPerSecond = None

    screen = None
    windowSize = None
    backgroundColor = None
    meshColor = None

    caption = None
    captionFont = None

    captionColor = None
    captionFontName = None
    captionFontSize = None

    album = None
    numberOfCars = 3

    @classmethod
    def ConnectSpritesManager(cls):

        cls.spritesManager.sprites = cls.sprites

    @classmethod
    def PlayAlbum(cls, album):

        # Get number of cars in single generation. It will be used later to create appropriate number of sprites.
        cls.numberOfCars = album.listOfTracks[0].numberOfBlackBoxes

        # Create screen on which everything will be drawn
        cls.CreateScreen()

        # Create sprites which will be drawn on the screen.
        cls.CreateSprites()

        # Create caption. See: "caption" in class description.
        cls.CreateCaption()

        # Album are divided into tracks. Hence this loop.
        for track in album.listOfTracks:
            cls.PlayTrack(track)

    @classmethod
    def CreateScreen(cls):

        cls.screen = pg.display.set_mode(cls.windowSize.asInt())

    @classmethod
    def CreateSprites(cls):

        cls.spritesManager.CreateSBarriers(cls.map)
        cls.spritesManager.CreateCarRelatedSprites(cls.numberOfCars)

    @classmethod
    def CreateCaption(cls):

        cls.captionFont = pg.font.SysFont(cls.captionFontName, cls.captionFontSize)

    @classmethod
    def PlayTrack(cls, track):

        # Manager will work on every iteration of loop, so at the beginning we have to pass him new data.
        cls.spritesManager.SetNewTrack(track)

        # Core loop. 1 iteration = 1 frame.
        for _ in range(track.length):
            cls.Wait()
            cls.UpdateSprites()
            cls.UpdateCaption(track)
            cls.DrawFrame()

    @classmethod
    def Wait(cls):
        ''' Freeze the work of the program.
        '''
        cls.dt = cls.clock.tick(cls.framesPerSecond) / 1000.0

    @classmethod
    def UpdateSprites(cls):
        ''' Perform necessary updates on sprites in order to display them properly in next frame.
        '''
        cls.spritesManager.UpdateCarRelatedSprites()

    @classmethod
    def UpdateCaption(cls, track):
        ''' Increment number of generation displayed on the screen.

        :param track: Track
            need to get its number in order to show it on screen.
        '''
        cls.caption = cls.captionFont.render("Generation no " + str(track.number + 1), True, cls.captionColor)

    @classmethod
    def DrawFrame(cls):
        ''' Draw frame.
            The process has two steps.
            1. Draw everything on "virtual screen".                        blit() method
            2. Update screen (make it be same as "virtual screen").        flip() method
        '''

        # Focus camera on chosen target.
        # It determines which sprites will be displayed on the screen
        cls.camera.FocusOn(cls.spritesManager.bestCarContainer.scar)

        # Draw background
        cls.DrawBackground()

        # Draw sprites
        for sprite in cls.sprites:
            cls.screen.blit(sprite.image, cls.camera.relativePos(sprite))

        # Draw caption
        cls.screen.blit(cls.caption, (cls.camera.windowSize.x - 210, 10))

        # Update screen.
        pg.display.flip()

    @classmethod
    def DrawBackground(cls):
        ''' Draw view background.
        '''

        # Set color of view's background.
        cls.screen.fill(cls.backgroundColor)

        # Draw mesh (vertical and horizontal lines).
        for x in range(0, cls.screen.get_width(), 100):
            pg.draw.line(cls.screen, cls.meshColor, (x, 0), (x, cls.screen.get_height()))
        for y in range(0, cls.screen.get_height(), 100):
            pg.draw.line(cls.screen, cls.meshColor, (0, y), (cls.screen.get_width(), y))


