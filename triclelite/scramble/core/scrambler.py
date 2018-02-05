class ScrambleObject():
    '''
        This class handles the [un]/scrambling an individual item.
    '''

    def __init__(self):
        mode = None
        pass

    def isScramble(self):
        '''
            Set the mode to scramble
        '''
        self.mode = "Scramble"

    def isUnscramble(self):
        '''
            Set the mode to scramble
        '''
        self.mode = "Unscramble"

    def run(self):
        '''
            This method runs the process
        '''
        pass

    def generateSeeds(self):
        '''
            This method generates a seed for each key
        '''
        pass

    def encodeArray(self):
        '''
            This method encodes an array for each seed
        '''
        pass

    def scramble(self):
        '''
            This method scrambles the image
        '''
        pass

    def unscramble(self):
        '''
            This method unscrambles the image
        '''
        pass
