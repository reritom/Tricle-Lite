from scramble.core.scrambler import ScrambleObject
from scramble.tools import media_tools, url_tools, common_tools
from scramble.models.active_url import ActiveURL
from scramble.models.zip_lock import ZipLock
from scramble.models.key_chain import KeyChain
from scramble.models.url_item import UrlItem

from datetime import datetime, timedelta
from hashlib import sha1
from pathlib import Path
import shutil, zipfile, os, pickle
from PIL import Image

from scramble.tools import media_tools

class ScramblerManager():
    '''
        This class handles the scrambling, unscrambling and saving of multiple images
    '''

    def __enter__(self):
        print("Entering manager object")
        return self

    def __init__(self, url):
        print("Manager init")
        self.keys = list()
        self.media_path = media_tools.get_media_path(url)
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

        self.retrieve_active_url()
        self.retrieve_key_chain()
        self.retrieve_zip_lock()

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting manager")

    def retrieve_key_chain(self):
        '''
            This method retrieves the keychain for this url
        '''
        print("Retrieving KeyChain")
        try:
            self.keychainobj = KeyChain.objects.get(active=self.urlobj)
        except:
            print("No KeyChain object found")

    def retrieve_zip_lock(self):
        '''
            This method attempts to retrieve the ziplock for this url (optional)
        '''
        print("Retrieving ziplock")
        try:
            self.ziplockobj = ZipLock.objects.get(active=self.urlobj)
            self.zipcode = self.ziplockobj.zipcode
        except:
            print("No ZipLock object found")

    def retrieve_active_url(self):
        '''
            This method retrieves the ActiveUrl for this object
        '''
        print("Retrieving ActiveUrl")
        self.urlobj = ActiveURL.objects.get(url=self.url)
        print("Setting mode as " + self.urlobj.mode)
        self.mode = self.urlobj.mode

    def run(self):
        '''
            This method processes each file passed to it
            :param path: Path of the files to process
        '''
        print("In Run")

        if not self.set_keys_from_key_chain(): return False
        print("Passed validation")
        self.generate_zip()

        for f in os.listdir(self.media_path):
            if f.lower().endswith(('bmp', 'jpg', 'png', 'jpeg')):
                image = Image.open(os.path.join(self.media_path, f))

                if self.mode == 'Scramble':
                    processedImage = self.scramble_file(image)
                elif self.mode == 'Unscramble':
                    processedImage = self.unscramble_file(image)

                self.save_file(f, processedImage)

        self.delete_preprocessed()

        # Delete the ZipLock
        if self.ziplockobj is not None:
            print("Deleting the Ziplock")
            self.ziplockobj.delete()

        # Mark as processed
        self.urlobj.set_processed()

    def protect_zip(self):
        '''
            This method adds the password to the Zip
        '''
        print("In protect_zip")
        if self.zipcode is not None:
            print("Protecting file")
            zf = zipfile.ZipFile(self.zipadr)
            zf.setpassword(self.zipcode.encode('utf-8'))
            zf.close()
        else:
            print("Not protecting file")

    def delete_preprocessed(self):
        '''
            Delete the original images
        '''
        print("In Delete")
        print(os.listdir(self.media_path))
        for prefile in os.listdir(self.media_path):
            print("Prefile " + prefile)
            print("Zipfile " + self.zipname)
            if prefile != self.zipname:
                print("Deleting " + prefile)
                media_tools.delete_file(os.path.join(self.media_path, prefile))

    def set_keys_from_key_chain(self):
        '''
            This method sets the keys from the KeyChain object
        '''
        try:
            self.keys = self.keychainobj.get_keys()
            return True
        except:
            print("Failed to get keys from keychain")
            return False


    def add_file_to_zip(self, filename):
        '''
            This method saves the zipfile
        '''
        print("Adding " + filename + " to zipfile")
        zf = zipfile.ZipFile(self.zipadr, mode='a')
        try:
            zf.write(os.path.join(self.media_path, filename), arcname=filename)
        finally:
            zf.close()

    def generate_zip(self):
        '''
            This method creates a zipfile
        '''
        print("Generating zip")
        timehash = sha1(str(datetime.now().isoformat()).encode("UTF-8")).hexdigest()[:5]
        self.zipname = timehash + ".zip"
        self.zipadr = os.path.join(self.media_path, self.zipname)

        if self.zipcode is not None:
            print("Protecting file")
            zf = zipfile.ZipFile(self.zipadr, mode='w')
            zf.setpassword(self.zipcode.encode('utf-8'))
        else:
            print("Not protecting file")
            zf = zipfile.ZipFile(self.zipadr, mode='w')


    def save_file(self, filename, final):
        '''
            This method adds a processed file to the zipfile
        '''
        print("Saving file")
        if self.mode == "Scramble":
            name = str(Path(filename).with_suffix('')) + ".BMP"
            print("Saving as " + os.path.join(self.media_path, name))
            final.save(os.path.join(self.media_path, name))
        else:
            try:
                name = str(Path(filename).with_suffix('')) + ".JPG"
                final.save(os.path.join(self.media_path, name), format="JPEG", subsampling=0, quality=100)
            except Exception as e:
                print("Error saving as JPG for " + self.url + " : " + e)
                try:
                    name = str(Path(filename).with_suffix('')) + ".PNG"
                    final.save(os.path.join(self.media_path, name), format="PNG", subsampling=0, quality=100)
                except Exception as e:
                    print("Error saving as PNG for " + self.url + " : " + e)
                    try:
                        name = str(Path(filename).with_suffix('')) + ".BMP"
                        final.save(os.path.join(self.media_path, name))
                    except Exception as e:
                        print("Error saving as BMP for " + self.url + " : " + e)
                        print("Unable to save, expiring " + self.url)
                        url_tools.expire_url(url)

        self.add_file_to_zip(name)

    def scramble_file(self, image):
        '''
            This method receives a file and scrambles it
        '''
        print("In scramble_file")
        with ScrambleObject() as instance:
            instance.is_scramble()
            instance.keys_are(self.keys)
            instance.image_is(image)
            return instance.run_and_return()


    def unscramble_file(self, image):
        '''
            This method receives a file to unscramble
        '''
        print("In unscramble_file")
        with ScrambleObject() as instance:
            instance.is_unscramble()
            instance.keys_are(self.keys)
            instance.image_is(image)
            return instance.run_and_return()
