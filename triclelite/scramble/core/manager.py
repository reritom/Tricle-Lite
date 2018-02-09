from scrambler import ScrambleObject

class ScramblerManager():
    '''
        This class handles the scrambling, unscrambling and saving of multiple images
    '''

    def __init__(self, urlPath):
        self.keys = list()
        self.urlPath = urlPath


    def run(self):
        '''
            This method processes each file passed to it
            :param path: Path of the files to process
        '''
        '''
        validate path contents
        read data
        create zipfile

        For each file in path:
            load file if ends with accepted filetype
            process
            name the file
            add file to zip

        save the zip (optional password if in data)
        '''
        pass

    def validatePathContents(self):
        '''
            This method validates that there is a pickled dict with 3 keys and a mode,
            and that there are files to process
        '''
        pass

    def save(self):
        '''
            This method saves the zipfile
        '''
        pass

    def generateZip(self):
        '''
            This method creates a zipfile
        '''
        pass

    def nameFile(self):
        '''
            This method names the file with the correct extension
        '''
        pass

    def addToZip(self):
        '''
            This method adds a processed file to the zipfile
        '''
        pass

    def scrambleFile(self, image):
        '''
            This method receives a file and scrambles it
            https://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
        '''
        instance = ScrambleObject()
        instance.isScramble()
        instance.keysAre(self.keys)
        instance.imageIs(image)
        return instance.runAndReturn()

    def unscrambleFile(self, image):
        '''
            This method receives a file to unscramble
        '''
        instance = ScrambleObject()
        instance.isUnscramble()
        instance.keysAre(self.keys)
        instance.imageIs(image)
        return instance.runAndReturn()
