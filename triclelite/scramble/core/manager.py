from scrambler import ScrambleObject

class ScramblerManager():
    '''
        This class handles the scrambling, unscrambling and saving of multiple images
    '''

    def __init__(self):
        pass

    def run(self):
        '''
            This method processes each file passed to it
            :param path: Path of the files to process
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

    def scrambleFile(self):
        '''
            This method receives a file and scrambles it
        '''
        instance = ScrambleObject()
        instance.isScramble()
        instance.keysAre(self.keys)
        instance.run()
        processed_image = instance.result()
        pass

    def unscrambleFile(self):
        '''
            This method receives a file to unscramble
        '''
