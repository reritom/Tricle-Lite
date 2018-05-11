import numpy as np
import os, time, random, sys
from PIL import Image

class ScrambleObject():
    '''
        This class handles the [un]/scrambling an individual item.
    '''
    def __enter__(self):
        print("In object enter")
        return self

    def __init__(self):
        self.mode = None
        self.keys = dict()
        self.seeds = list()
        self.encoded_arrays = [None, None, None]

        self.original = None
        self.proc_round_one = None
        self.proc_round_two = None

        self.grid_size = 5

        # The number of elements that the image is split into in each dimension based on the grid_size
        self.xNum = None
        self.yNum = None

    def __exit__(self, exc_type, exc_value, traceback):
        '''
            Exit layer
        '''
        print("In object exit")

    def validate_init(self):
        '''
            Validate that the keys, mode, and original image have been set before running
        '''
        if ((self.mode is not None) and (self.original is not None) and (self.keys)):
            return True
        else:
            return False

    def image_is(self, image):
        '''
            The image to process
        '''
        self.original = np.array(image)
        self.proc_round_one = np.copy(self.original)
        self.proc_round_two = np.copy(self.original)

        # Set the image dimensions
        self.colx = self.original.shape[0]
        self.rowy = self.original.shape[1]

    def is_scramble(self):
        '''
            Set the mode to scramble
        '''
        self.mode = "Scramble"

    def is_unscramble(self):
        '''
            Set the mode to scramble
        '''
        self.mode = "Unscramble"

    def keys_are(self, keys):
        '''
            Set the keys
            :param keys (list): format [key1, key2, key3]
        '''
        self.keys = keys

    def run_and_return(self):
        '''
            This method runs the process
        '''
        if not self.validate_init():
            return False

        self.generate_seeds()
        self.encode_arrays()

        if self.mode == "Scramble":
            return self.scramble()
        elif self.mode == "Unscramble":
            return self.unscramble()

    def generate_seeds(self):
        '''
            This method generates a seed for each key
        '''
        seeds = list()
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
            seeds.append(this_seed)

        seeds[0] = seeds[0] + seeds[1][1:] + seeds[2][1:]
        seeds[1] = seeds[1] + seeds[0][1:] + seeds[2][1:]
        seeds[2] = seeds[2] + seeds[0][1:] + seeds[1][1:]

        for seed in seeds:
            self.seeds.append(seed)

    def encode_arrays(self):
        '''
            This method encodes an array for each seed
        '''
        self.encoded_arrays[0] = list(range(0, self.colx))
        self.encoded_arrays[1] = list(range(0, self.rowy))

        self.xNum = int((self.colx - self.colx%self.grid_size)/self.grid_size)
        self.yNum = int((self.rowy - self.rowy%self.grid_size)/self.grid_size)

        self.encoded_arrays[2] = list(range(0, self.xNum*self.yNum))

        random.Random(self.seeds[0]).shuffle(self.encoded_arrays[0])
        random.Random(self.seeds[1]).shuffle(self.encoded_arrays[1])
        random.Random(self.seeds[2]).shuffle(self.encoded_arrays[2])

    def scramble(self):
        '''
            This method scrambles the image
        '''

        # Switch the x and y indices with those of the encoded_arrays (encoded_arrays[0] for x, encoded_arrays[1] for y)
        for x in range(self.colx):
            for y in range(self.rowy):
                self.proc_round_one[x][y] = self.original[self.encoded_arrays[0][x]][self.encoded_arrays[1][y]]

        self.proc_round_two = np.copy(self.proc_round_one)

        ind = 0
        for x in range(self.xNum):
            for y in range(self.yNum):
                # TODO - Deconstruct this logic
                blue = self.encoded_arrays[2][ind]
                xEn = blue%self.xNum
                yEn = int((blue - xEn)/self.xNum)

                self.proc_round_two[x*self.grid_size:x*self.grid_size+self.grid_size,y*self.grid_size:y*self.grid_size+self.grid_size,:] = self.proc_round_one[xEn*self.grid_size:xEn*self.grid_size+self.grid_size,yEn*self.grid_size:yEn*self.grid_size+self.grid_size,:]

                ind = ind + 1

        return Image.fromarray(self.proc_round_two)

    def unscramble(self):
        '''
            This method unscrambles the image
        '''
        ind = 0
        for x in range(self.xNum):
            for y in range(self.yNum):
                blue = self.encoded_arrays[2][ind]
                xEn = blue%self.xNum
                yEn = int((blue - xEn)/self.xNum)

                self.proc_round_one[xEn*self.grid_size:xEn*self.grid_size+self.grid_size,yEn*self.grid_size:yEn*self.grid_size+self.grid_size,:] = self.original[x*self.grid_size:x*self.grid_size+self.grid_size,y*self.grid_size:y*self.grid_size+self.grid_size,:]

                ind = ind + 1

        self.proc_round_two = np.copy(self.proc_round_one)

        for x in range(self.colx):
            for y in range(self.rowy):
                self.proc_round_two[self.encoded_arrays[0][x]][self.encoded_arrays[1][y]] = self.proc_round_one[x][y]

        return Image.fromarray(self.proc_round_two)
