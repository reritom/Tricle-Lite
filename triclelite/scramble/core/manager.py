from scramble.core.scrambler import ScrambleObject
from scramble.tools import mediaTools, urlTools, commonTools
from scramble.models import ActiveURL, ZipLock, KeyChain

from datetime import datetime, timedelta
from hashlib import sha1
from pathlib import Path
import shutil, zipfile, os, pickle
from PIL import Image

class ScramblerManager():
    '''
        This class handles the scrambling, unscrambling and saving of multiple images
    '''

    def __enter__(self):
        print("Entering manager object")
        return self

    def __init__(self, mediaPath, url):
        print("Manager init")
        self.keys = list()
        self.mediaPath = mediaPath
        self.url = url

        self.zipname = None
        self.zipadr = None
        self.zipfile = None
        self.zipcode = None # If a ZipLock is found, this is set to the value

        self.keys = None
        self.mode = None

        self.urlobj = None
        self.keychainobj = None
        self.ziplockobj = None

        self.retrieveActiveUrl()
        self.retrieveKeyChain()
        self.retrieveZipLock()

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting manager")

    def retrieveKeyChain(self):
        '''
            This method retrieves the keychain for this url
        '''
        pass

    def retrieveZipLock(self):
        '''
            This method attempts to retrieve the ziplock for this url (optional)
        '''
        print("Retrieving ziplock")
        try:
            self.ziplockobj = ZipLock.objects.get(active=self.urlobj)
            self.zipcode = self.ziplockobj.zipcode
        except:
            print("No ZipLock object found")

    def retrieveActiveUrl(self):
        '''
            This method retrieves the ActiveUrl for this object
        '''
        print("Retrieving ActiveUrl")
        self.urlobj = ActiveURL.objects.get(url=self.url)

    def run(self):
        '''
            This method processes each file passed to it
            :param path: Path of the files to process
        '''
        print("In Run")

        if not self.validatePathContents(): return False
        if not self.readData(): return False
        print("Passed validation")
        self.generateZip()

        for f in os.listdir(self.mediaPath):
            if f.lower().endswith(('bmp', 'jpg', 'png', 'jpeg')):
                image = Image.open(os.path.join(self.mediaPath, f))

                if self.mode == 'Scramble':
                    processedImage = self.scrambleFile(image)
                elif self.mode == 'Unscramble':
                    processedImage = self.unscrambleFile(image)

                self.saveFile(f, processedImage)

        self.deletePreprocessed()
        if self.ziplockobj is not None:
            print("Deleting the Ziplock")
            self.ziplockobj.delete()

    def protectZip(self):
        '''
            This method adds the password to the Zip
        '''
        print("In protectZip")
        if self.zipcode is not None:
            print("Protecting file")
            zf = zipfile.ZipFile(self.zipadr)
            zf.setpassword(self.zipcode.encode('utf-8'))
            zf.close()
        else:
            print("Not protecting file")

    def deletePreprocessed(self):
        '''
            Delete the original images and the data pkl
        '''
        print("In Delete")
        print(os.listdir(self.mediaPath))
        for prefile in os.listdir(self.mediaPath):
            print("Prefile " + prefile)
            print("Zipfile " + self.zipname)
            if prefile != self.zipname:
                print("Deleting " + prefile)
                mediaTools.delete_file(os.path.join(self.mediaPath, prefile))

    def validatePathContents(self):
        '''
            This method validates that there is a pickled dict with 3 keys and a mode,
            and that there are files to process
        '''
        return True

    def readData(self):
        '''
            This method reads the data pickle and stores the keys and mode
        '''
        try:
            print("Attempting to open " + os.path.join(self.mediaPath, 'data'))
            with open(os.path.join(self.mediaPath, 'data'), 'rb') as fp:
                form = pickle.load(fp)
                self.keys = [form['k1'], form ['k2'], form['k3']]
                self.mode = form['mode']
            print("Data read successful")
            return True
        except:
            print('Unable to read data')
            return False

    def addToZip(self, filename):
        '''
            This method saves the zipfile
        '''
        print("Adding " + filename + " to zipfile")
        zf = zipfile.ZipFile(self.zipadr, mode='a')
        try:
            zf.write(os.path.join(self.mediaPath, filename), arcname=filename)
        finally:
            zf.close()

    def generateZip(self):
        '''
            This method creates a zipfile
        '''
        print("Generating zip")
        timehash = sha1(str(datetime.now().isoformat()).encode("UTF-8")).hexdigest()[:5]
        self.zipname = timehash + ".zip"
        self.zipadr = os.path.join(self.mediaPath, self.zipname)

        if self.zipcode is not None:
            print("Protecting file")
            zf = zipfile.ZipFile(self.zipadr, mode='w')
            zf.setpassword(self.zipcode.encode('utf-8'))
        else:
            print("Not protecting file")
            zf = zipfile.ZipFile(self.zipadr, mode='w')


    def saveFile(self, filename, final):
        '''
            This method adds a processed file to the zipfile
        '''
        print("Saving file")
        if self.mode == "Scramble":
            name = str(Path(filename).with_suffix('')) + ".BMP"
            print("Saving as " + os.path.join(self.mediaPath, name))
            final.save(os.path.join(self.mediaPath, name))
        else:
            try:
                name = str(Path(filename).with_suffix('')) + ".JPG"
                final.save(os.path.join(self.mediaPath, name), format="JPEG", subsampling=0, quality=100)
            except Exception as e:
                print("Error saving as JPG for " + self.url + " : " + e)
                try:
                    name = str(Path(filename).with_suffix('')) + ".PNG"
                    final.save(os.path.join(self.mediaPath, name), format="PNG", subsampling=0, quality=100)
                except Exception as e:
                    print("Error saving as PNG for " + self.url + " : " + e)
                    try:
                        name = str(Path(filename).with_suffix('')) + ".BMP"
                        final.save(os.path.join(self.mediaPath, name))
                    except Exception as e:
                        print("Error saving as BMP for " + self.url + " : " + e)
                        print("Unable to save, expiring " + self.url)
                        urlTools.expire_url(url)

        self.addToZip(name)

    def scrambleFile(self, image):
        '''
            This method receives a file and scrambles it
            https://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
        '''
        print("In scrambleFile")
        with ScrambleObject() as instance:
            instance.isScramble()
            instance.keysAre(self.keys)
            instance.imageIs(image)
            return instance.runAndReturn()


    def unscrambleFile(self, image):
        '''
            This method receives a file to unscramble
        '''
        print("In unscrambleFile")
        with ScrambleObject() as instance:
            instance.isUnscramble()
            instance.keysAre(self.keys)
            instance.imageIs(image)
            return instance.runAndReturn()
