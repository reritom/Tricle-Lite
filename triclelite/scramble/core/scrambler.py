import numpy as np
import os, time, random, sys
from PIL import Image

class ScrambleObject():
    '''
        This class handles the [un]/scrambling an individual item.
    '''

    def __init__(self):
        self.mode = None
        self.keys = dict()
        self.seeds = list()
        self.encodedArrays = [None, None, None]

        self.original = None
        self.proc_round_one = None
        self.proc_round_two = None

        self.gridSize = 5

        # The number of elements that the image is split into in each dimension based on the gridSize
        self.xNum = None
        self.yNum = None

    def validateInit(self):
        '''
            Validate that the keys, mode, and original image have been set before running
        '''
        if ((self.mode is not None) and (self.original is not None) and (self.keys)):
            return True
        else:
            return False

    def imageIs(self, image):
        '''
            The image to process
        '''
        self.original = np.array(image)
        self.proc_round_one = np.copy(self.original)
        self.proc_round_two = np.copy(self.original)

        # Set the image dimensions
        self.colx = self.original.shape[0]
        self.rowy = self.original.shape[1]

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

    def keysAre(self, keys):
        '''
            Set the keys
            :param keys (list): format [key1, key2, key3]
        '''
        self.keys = keys

    def runAndReturn(self):
        '''
            This method runs the process
        '''
        if not self.validateInit():
            return False

        print("Generating seeds")
        self.generateSeeds()

        print("Encoding arrays")
        self.encodeArrays()

        print("Encoded arrays are: " + str(self.encodedArrays))

        if self.mode == "Scramble":
            print("Scrambling")
            return self.scramble()
        elif self.mode == "Unscramble":
            print("Unscrambling")
            return self.unscramble()

    def generateSeeds(self):
        '''
            This method generates a seed for each key
        '''
        for i in range(3):
            this_key = self.keys[i]

            # List of the ord values for each letter of the key
            uniKey = list()

            # Key length
            uniVal = len(this_key)

            # For each letter, add the ord value to the list
            count = 0
            for i in range(len(this_key)):
                uniKey.append(ord(this_key[i]))

                # Manipulate the uniVal using the ord of this letter and whether the index is even or odd
                if count%2 == 0:
                    uniVal = uniVal * uniKey[i]
                else:
                    uniVal = uniVal / uniKey[i]

            # The ord of the first and last character
            this_seed = str((uniKey[0] + uniKey[len(uniKey) - 1]))

            # Plus the uniVal and the length of the key
            this_seed = this_seed + str(uniVal) + str(len(this_key))

            self.seeds.append(this_seed)

    def encodeArrays(self):
        '''
            This method encodes an array for each seed
        '''
        self.encodedArrays[0] = list(range(0, self.colx))
        self.encodedArrays[1] = list(range(0, self.rowy))

        self.xNum = int((self.colx - self.colx%self.gridSize)/self.gridSize)
        self.yNum = int((self.rowy - self.rowy%self.gridSize)/self.gridSize)

        self.encodedArrays[2] = list(range(0, self.xNum*self.yNum))

        random.Random(self.seeds[0]).shuffle(self.encodedArrays[0])
        random.Random(self.seeds[1]).shuffle(self.encodedArrays[1])
        random.Random(self.seeds[2]).shuffle(self.encodedArrays[2])

    def scramble(self):
        '''
            This method scrambles the image
        '''

        # Switch the x and y indices with those of the encodedArrays (encodedArrays[0] for x, encodedArrays[1] for y)
        for x in range(self.colx):
            for y in range(self.rowy):
                self.proc_round_one[x][y] = self.original[self.encodedArrays[0][x]][self.encodedArrays[1][y]]

        self.proc_round_two = np.copy(self.proc_round_one)

        ind = 0
        for x in range(self.xNum):
            for y in range(self.yNum):
                # TODO - Deconstruct this logic
                blue = self.encodedArrays[2][ind]
                xEn = blue%self.xNum
                yEn = int((blue - xEn)/self.xNum)

                self.proc_round_two[x*self.gridSize:x*self.gridSize+self.gridSize,y*self.gridSize:y*self.gridSize+self.gridSize,:] = self.proc_round_one[xEn*self.gridSize:xEn*self.gridSize+self.gridSize,yEn*self.gridSize:yEn*self.gridSize+self.gridSize,:]

                ind = ind + 1

        return Image.fromarray(self.proc_round_two)

    def unscramble(self):
        '''
            This method unscrambles the image
        '''
        ind = 0
        for x in range(self.xNum):
            for y in range(self.yNum):
                blue = self.encodedArrays[2][ind]
                xEn = blue%self.xNum
                yEn = int((blue - xEn)/self.xNum)

                self.proc_round_one[xEn*self.gridSize:xEn*self.gridSize+self.gridSize,yEn*self.gridSize:yEn*self.gridSize+self.gridSize,:] = self.original[x*self.gridSize:x*self.gridSize+self.gridSize,y*self.gridSize:y*self.gridSize+self.gridSize,:]

                ind = ind + 1

        self.proc_round_two = np.copy(self.proc_round_one)

        for x in range(self.colx):
            for y in range(self.rowy):
                self.proc_round_two[self.encodedArrays[0][x]][self.encodedArrays[1][y]] = self.proc_round_one[x][y]

        return Image.fromarray(self.proc_round_two)
