from Modules.General.general_tools import FilesManager, BuiltInTypesConverter
from Modules.Simulation.geometry import Point




class RangefinderRecord:

    def __init__(self):
        self.pos = Point()
        self.rot = None
        self._posOfBarrier = Point()

    @property
    def posOfBarrier(self):
        return self._posOfBarrier

    @posOfBarrier.setter
    def posOfBarrier(self, value):
        if value is not None:
            self._posOfBarrier = value
        else:
            self._posOfBarrier = Point([0, 0])

    def SaveToFile(self, filename):
        ''' Save object's parameters in specific order.
        '''
        listOfData = [self.pos[0], self.pos[1], self.rot, self.posOfBarrier[0], self.posOfBarrier[1]]
        FilesManager.AddLineToFile(BuiltInTypesConverter.IntsToString(listOfData), filename)

    def LoadFromLine(self, line):

        self.pos.x, self.pos.y, self.rot, self.posOfBarrier.x, self.posOfBarrier.y = BuiltInTypesConverter.StringToInts(line)




class RadarRecord:

    numberOfRangefinderRecords = None

    def __init__(self, listOfRangefinders=None):
        self.pos = Point()
        self.rot = None
        self.listOfRangefinderRecords = [RangefinderRecord()] * self.__class__.numberOfRangefinderRecords

        if listOfRangefinders is not None:
            for _ in range(self.__class__.numberOfRangefinderRecords):
                self.listOfRangefinderRecords[_] = listOfRangefinders[_].record

    def SaveToFile(self, filename):
        ''' Save object's parameters in specific order.
        '''

        #Save data about radar exclusively
        with open(filename, "a") as file:
            listOfData = [self.pos[0], self.pos[1], self.rot]
            file.write(BuiltInTypesConverter.IntsToString(listOfData) + "\n")

        #Save data about rangefinders
        for rangefinderRecord in self.listOfRangefinderRecords:
            rangefinderRecord.SaveToFile(filename)

    def LoadFromLines(self, lines):

        first_line, rest = lines[0], lines[1:]

        # Load data about radar exclusively
        self.pos.x, self.pos.y, self.rot = BuiltInTypesConverter.StringToInts(first_line)

        # Load data about rangefinders
        for _, line in zip(range(self.__class__.numberOfRangefinderRecords), rest):
            rangefinderRecord = RangefinderRecord()
            rangefinderRecord.LoadFromLine(line)
            self.listOfRangefinderRecords[_] = rangefinderRecord




class CarRecord:

    def __init__(self, radarRecord=None):
        self.pos = Point()
        self.rot = None

        if radarRecord is None:
            self.radarRecord = RadarRecord()
        else:
            self.radarRecord = radarRecord

        self.number = None

    def SaveToFile(self, filename):
        ''' Save object's parameters in specific order
        '''

        # Save data about car exclusively
        with open(filename, "a") as file:
            listOfData = [self.pos[0], self.pos[1], self.rot]
            file.write(BuiltInTypesConverter.IntsToString(listOfData) + "\n")

        # Save data about radar
        self.radarRecord.SaveToFile(filename)

    def LoadFromLines(self, lines):


        first_line, rest = lines[0], lines[1:]

        # Load data about car exclusively
        self.pos.x, self.pos.y, self.rot = BuiltInTypesConverter.StringToInts(first_line)

        # Load data about radar
        self.radarRecord.LoadFromLines(rest)

class BlackBox:

    def __init__(self):
        self.listOfCarRecords = []
        self.number = None

    @property
    def numberOfCarRecords(self):
        return None

    @numberOfCarRecords.getter
    def numberOfCarRecords(self):
        return len(self.listOfCarRecords)

    def AddCarRecord(self, carRecord):

        carRecord.number = self.numberOfCarRecords
        self.listOfCarRecords.append(carRecord)


    def SaveToFile(self, filename):


        # Line which we writing using code below will be usable during loading process
        with open(filename, "a") as file:
            file.write(str(self.numberOfCarRecords) + "\n")

        # Save records
        for roc in self.listOfCarRecords:
            roc.SaveToFile(filename)

    def LoadFromLines(self, lines):

        first_line, rest = lines[0], lines[1:]

        numberOfCarRecords = BuiltInTypesConverter.StringToInts(first_line)[0]
        linesPerSingleCarRecord = int(len(rest)/numberOfCarRecords)

        #Read one car record per single iteration
        while len(rest) >= 1:
            carRecord = CarRecord()
            carRecord.LoadFromLines(rest[:linesPerSingleCarRecord])
            self.AddCarRecord(carRecord)

            #Remove already read data from rest of data to read.
            rest = rest[linesPerSingleCarRecord:]




class Track:

    def __init__(self):
        self.listOfBlackBoxes = []
        self.length = 0
        self.number = None

    @property
    def numberOfBlackBoxes(self):
        return None

    @numberOfBlackBoxes.getter
    def numberOfBlackBoxes(self):
        return len(self.listOfBlackBoxes)

    def AddBlackBox(self, blackBox):
        ''' Augmented "listOfBlackBoxes.append".
        '''

        blackBox.number = self.numberOfBlackBoxes
        self.listOfBlackBoxes.append(blackBox)
        self.RevaluateLength(len(blackBox.listOfCarRecords))


    def RevaluateLength(self, potentialNewLength):
        ''' Update "length" attribute
        '''

        if potentialNewLength > self.length:
            self.length = potentialNewLength

    def SaveToFile(self, filename):
        ''' Save object
        '''

        with open(filename, "a") as file:

            # Lines which we writing using code below will be usable during loading process
            numberOfCarRecords = sum([len(blackbox.listOfCarRecords) for blackbox in self.listOfBlackBoxes])
            linesPerSingleCarRecord = RadarRecord.numberOfRangefinderRecords+2
            file.write(str(linesPerSingleCarRecord)+" "+str(numberOfCarRecords)+"\n")

        #Save black boxes
        for blackbox in self.listOfBlackBoxes:
            blackbox.SaveToFile(filename)

    def LoadFromLines(self, lines):

        first_line, rest = lines[0], lines[1:]

        linesPerSingleCarRecord = BuiltInTypesConverter.StringToInts(first_line)[0]

        # Read one black box record per single iteration
        while len(rest) >= 1:
            numberOfCarRecordsInNextBlackBox = BuiltInTypesConverter.StringToInts(rest[0])[0]

            # Comment: " + 1" on the end of next line of code results from fact, that black box need one additional line
            # with information which are necessary to properly loading.
            numberOfLinesForNextBlackBox = numberOfCarRecordsInNextBlackBox * linesPerSingleCarRecord + 1
            blackbox = BlackBox()
            blackbox.LoadFromLines(rest[:numberOfLinesForNextBlackBox])
            self.AddBlackBox(blackbox)

            # Remove already read data from rest of data to read.
            rest = rest[numberOfLinesForNextBlackBox:]

class Album:

    def __init__(self):
        self.listOfTracks = []

    @property
    def numberOfTracks(self):
        return None

    @numberOfTracks.getter
    def numberOfTracks(self):
        return len(self.listOfTracks)


    def AddTrack(self, track):
        ''' Augmented "listOfBlackBoxes.append".
        '''
        track.number = self.numberOfTracks
        self.listOfTracks.append(track)


    def SaveToFile(self, filename):
        ''' Save object
        '''

        #Clear the file
        file0 = open(filename, "w")
        file0.close()

        with open(filename, "a") as file:
            # Lines which we writing using code below will be usable during loading process
            linesPerSingleCarRecord = RadarRecord.numberOfRangefinderRecords+2
            blackboxesPerTrack = len(self.listOfTracks[0].listOfBlackBoxes)
            file.write(str(linesPerSingleCarRecord)+" "+str(blackboxesPerTrack)+"\n")

        #Save tracks
        for track in self.listOfTracks:
            track.SaveToFile(filename)

    def LoadFromLines(self, lines):

        first_line, rest = lines[0], lines[1:]

        linesPerSingleCarRecord, blackboxesPerTrack = BuiltInTypesConverter.StringToInts(first_line)

        # Read one track record per single iteration
        while len(rest) >= 1:
            firstLineFromNextTrack = rest[0]
            numberOfRocsInNextTrack = BuiltInTypesConverter.StringToInts(firstLineFromNextTrack)[1]

            # Comment about line below:
            # " + blackboxesPerTrack" results from fact, that black box need one additional line with information which
            # are necessary for properly loading. We have "blackboxesPerTrack" black boxes in next track, so that
            # addition.
            # " + 1" results from fact, that track also requires one additional line.
            numberOfLinesForNextTrack = linesPerSingleCarRecord * numberOfRocsInNextTrack + blackboxesPerTrack + 1
            track = Track()
            track.LoadFromLines(rest[:numberOfLinesForNextTrack])
            self.AddTrack(track)

            # Remove already read data from rest of data to read.
            rest = rest[numberOfLinesForNextTrack:]

    def LoadFromFile(self, filename):
        ''' Load album from file
        '''

        file = open(filename, "r")
        lines = file.readlines()
        self.LoadFromLines(lines)
        file.close()


    @classmethod
    def MergedAlbums(cls, listOfAlbums):

        result = Album()
        for album in listOfAlbums:
            for track in album.listOfTracks:
                result.AddTrack(track)
        return result
