##---------------------------------------------------------------------------##
##
## pyChing -- a Python program to cast and interpret I Ching hexagrams
##
## Copyright (C) 1999-2006 Stephen M. Gava
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be of some
## interest to somebody, but WITHOUT ANY WARRANTY; without even the 
## implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING or COPYING.txt. If not, 
##  write to the Free Software Foundation, Inc.,
## 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
## The license can also be found at the GNU/FSF website: http://www.gnu.org
##
## Stephen M. Gava
## <elguavas@users.sourceforge.net>
## http://pyching.sourgeforge.net
##
##---------------------------------------------------------------------------##
"""
engine module for pyching
classes and utility functions
"""
#python library imports
import sys
import os
import random
import pickle
import json
import time
from functools import reduce
from pathlib import Path
from typing import Optional, Any

#
# classes
################

#private classes - should not be directly accessed from outside this module
class Hexagram:
    """
    single Hexagram data structure template, private class

    should only be accessed as an attribute of an instance of the Hexagrams class (below)
    this class is defined at module level to enable pickling of Hexagrams instances
    """
    def __init__(self) -> None:
        self.number: str = ''
        self.name: str = ''
        self.lineValues: list[int] = [0,0,0,0,0,0]
        self.infoSource: Optional[str] = None

#public classes
class PychingAppDetails:
    """
    holds information about a running instance of the pyching application, public class
    """
    def __init__(self, createConfigDir: int = 1) -> None:
        self.title: str = 'pyChing'
        self.version: str = '1.2.2'
        self.os: str = sys.platform
        self.osType: str = os.name
        self.execPath: Path = self.GetProgramDir()
        self.configPath: Path = self.GetUserCfgDir('.pyching')
        self.savePath: Path = self.configPath
        self.configFile: Path = self.configPath / 'config.json'
        self.saveFileExt: str = '.psv'
        self.internalImageExt: str = '.#@~'
        self.internalHtmlExt: str = '.~@#'
        self.saveFileID: tuple[str, str] = ('pyching_save_file', self.version)
        self.emailAddress: str = 'elguavas@users.sourceforge.net'
        self.webAddress: str = 'http://pyching.sourceforge.net'

    def GetProgramDir(self) -> Path:
        """
        return the filesystem directory where this program file resides.
        (ie the applications exec or import directory.)
        """
        if __name__ != '__main__':  # we were imported
            appDir = Path(__file__).parent
        else:  # we were exec'ed (for testing only)
            appDir = Path(sys.path[0]).resolve()
        return appDir

    def GetUserCfgDir(self, cfgDir: str) -> Path:
        """
        Creates (if required) and returns a filesystem directory for storing
        user config files.
        """
        userDir = Path.home()
        try:
            # Verify home directory exists
            if not userDir.exists():
                warn = (f'\n Warning: HOME environment variable points to\n {userDir}\n'
                        ' but the path does not exist.\n')
                sys.stderr.write(warn)
                userDir = Path.cwd()
        except (RuntimeError, OSError):
            # Path.home() can raise RuntimeError if home not found
            userDir = Path.cwd()  # hack for no real homedir

        userDir = userDir / cfgDir
        if not userDir.exists():
            try:  # make the config dir if it doesn't exist yet
                userDir.mkdir(parents=True, exist_ok=True)
            except IOError:
                warn = f'\n Warning: unable to create user config directory\n {userDir}\n'
                sys.stderr.write(warn)
        return userDir

# create an instance of the app details for use throughout this module
#
pyching = PychingAppDetails()
#
#

class Hexagrams:
    """
    holds both Hexagrams for a reading, public class
    """
    def __init__(self, oracleType: str = 'coin') -> None:
        """
        initialise self by setting oracle type
        defaults to coin, if specified must be a valid oracle type (coin or yarrow)
        """
        #public data attributes - should read but not written to from outside this module
        #any attributes that need to be modified from outside this module have a 'set_xxx'
        #method available below
        self.question: str = ''  # use SetQuestion (below) to set this attribute from outside this module
        self.oracle: str = oracleType  # oracle being used
        self.hex1: Hexagram = Hexagram()  # Hexagram 1 data structure
        self.hex2: Hexagram = Hexagram()  # Hexagram 2 data structure
        self.currentLine: int = 0  # current line being cast in Hex1
        self.currentOracleValues: list[int] = []  # list of oracle values for current line

    def __GetHexDetails(self, hexKey: list[int]) -> tuple[str, str]:
        """
        lookup hex name and number, private method

        hexKey value should be a list of the non-moving line numbers for the
        Hexagram being enquired upon (Hex?.Key)
        returns a tuple of Hexagram details in the form (number, name)
        """
        if hexKey == [7,7,7,7,7,7]: return ('1', "Tch'ien")
        elif hexKey == [8,8,8,8,8,8]: return ('2', "Koun")
        elif hexKey == [7,8,8,8,7,8]: return ('3', "T'oun")
        elif hexKey == [8,7,8,8,8,7]: return ('4', "Mong")
        elif hexKey == [7,7,7,8,7,8]: return ('5', "Hsu")
        elif hexKey == [8,7,8,7,7,7]: return ('6', "Song")
        elif hexKey == [8,7,8,8,8,8]: return ('7', "Cheu")
        elif hexKey == [8,8,8,8,7,8]: return ('8', "Pi")
        elif hexKey == [7,7,7,8,7,7]: return ('9', "Siao Tch'ou")
        elif hexKey == [7,7,8,7,7,7]: return ('10', "Li")
        elif hexKey == [7,7,7,8,8,8]: return ('11', "T'ai")
        elif hexKey == [8,8,8,7,7,7]: return ('12', "P'i")
        elif hexKey == [7,8,7,7,7,7]: return ('13', "Tong Jen")
        elif hexKey == [7,7,7,7,8,7]: return ('14', "Ta You")
        elif hexKey == [8,8,7,8,8,8]: return ('15', "Tchien")
        elif hexKey == [8,8,8,7,8,8]: return ('16', "Yu")
        elif hexKey == [7,8,8,7,7,8]: return ('17', "Souei")
        elif hexKey == [8,7,7,8,8,7]: return ('18', "Kou")
        elif hexKey == [7,7,8,8,8,8]: return ('19', "Lin")
        elif hexKey == [8,8,8,8,7,7]: return ('20', "Kouan")
        elif hexKey == [7,8,8,7,8,7]: return ('21', "Che Ho")
        elif hexKey == [7,8,7,8,8,7]: return ('22', "Pi")
        elif hexKey == [8,8,8,8,8,7]: return ('23', "Po")
        elif hexKey == [7,8,8,8,8,8]: return ('24', "Fou")
        elif hexKey == [7,8,8,7,7,7]: return ('25', "Wou Wang")
        elif hexKey == [7,7,7,8,8,7]: return ('26', "Ta Tch'ou")
        elif hexKey == [7,8,8,8,8,7]: return ('27', "I")
        elif hexKey == [8,7,7,7,7,8]: return ('28', "Ta Kouo")
        elif hexKey == [8,7,8,8,7,8]: return ('29', "K'an")
        elif hexKey == [7,8,7,7,8,7]: return ('30', "Li")
        elif hexKey == [8,8,7,7,7,8]: return ('31', "Hsien")
        elif hexKey == [8,7,7,7,8,8]: return ('32', "Hong")
        elif hexKey == [8,8,7,7,7,7]: return ('33', "Toun")
        elif hexKey == [7,7,7,7,8,8]: return ('34', "Ta Tch'ouang")
        elif hexKey == [8,8,8,7,8,7]: return ('35', "Tchin")
        elif hexKey == [7,8,7,8,8,8]: return ('36', "Ming Yi")
        elif hexKey == [7,8,7,8,7,7]: return ('37', "Tchia Jen")
        elif hexKey == [7,7,8,7,8,7]: return ('38', "K'ouei")
        elif hexKey == [8,8,7,8,7,8]: return ('39', "Tch'ien")
        elif hexKey == [8,7,8,7,8,8]: return ('40', "Tchieh")
        elif hexKey == [7,7,8,8,8,7]: return ('41', "Soun")
        elif hexKey == [7,8,8,8,7,7]: return ('42', "Yi")
        elif hexKey == [7,7,7,7,7,8]: return ('43', "Kouai")
        elif hexKey == [8,7,7,7,7,7]: return ('44', "Keou")
        elif hexKey == [8,8,8,7,7,8]: return ('45', "Ts'ouei")
        elif hexKey == [8,7,7,8,8,8]: return ('46', "Cheng")
        elif hexKey == [8,7,8,7,7,8]: return ('47', "K'oun")
        elif hexKey == [8,7,7,8,7,8]: return ('48', "Tsing")
        elif hexKey == [7,8,7,7,7,8]: return ('49', "Keu")
        elif hexKey == [8,7,7,7,8,7]: return ('50', "Ting")
        elif hexKey == [7,8,8,7,8,8]: return ('51', "Tchen")
        elif hexKey == [8,8,7,8,8,7]: return ('52', "Ken")
        elif hexKey == [8,8,7,8,7,7]: return ('53', "Tchien")
        elif hexKey == [7,7,8,7,8,8]: return ('54', "Kouei Mei")
        elif hexKey == [7,8,7,7,8,8]: return ('55', "Fong")
        elif hexKey == [8,8,7,7,8,7]: return ('56', "Lu")
        elif hexKey == [8,7,7,8,7,7]: return ('57', "Hsuan")
        elif hexKey == [7,7,8,7,7,8]: return ('58', "Touei")
        elif hexKey == [8,7,8,8,7,7]: return ('59', "Houan")
        elif hexKey == [7,7,8,8,7,8]: return ('60', "Tchieh")
        elif hexKey == [7,7,8,8,7,7]: return ('61', "Tchong Fou")
        elif hexKey == [8,8,7,7,8,8]: return ('62', "Siao Kouo")
        elif hexKey == [7,8,7,8,7,8]: return ('63', "Tchi Tchi")
        elif hexKey == [8,7,8,7,8,7]: return ('64', "Wei Tchi")
        else: #raise an exception
            return (0, "lookup error")
            # pass

    def NewLine(self) -> None:
        """
        builds next line in Hex1 and completes both Hexagrams after line 6, public method
        """
        if self.currentLine < 6: #build a new Hex1 line
            rc = random.choice #returns a random value from the specified sequence 
            #handle each oracle type
            if self.oracle == 'coin':
                self.currentOracleValues = [rc([2,3]), rc([2,3]), rc([2,3])]
                #for item in self.currentOracleValues: #line value = sum of oracle values 
                # self.hex1.lineValues[self.currentLine] = self.hex1.lineValues[self.currentLine] + item
            self.hex1.lineValues[self.currentLine] = reduce(lambda x,y: x+y, self.currentOracleValues) #line value = sum of oracle values
            #elif self.oracle == 'yarrow':
            # self.oracleValues = [0, 0, 0] #dummy results
            # self.hex1.lineValues[CurrentLine] = 0 #dummy result
            self.currentLine = self.currentLine + 1 #next line is current
        if self.currentLine == 6: #Hex1 is all built
            hex1Key = [0,0,0,0,0,0] #Hex1's details lookup key
            i = 0 #used as a counter in the loop below
            for item in self.hex1.lineValues: #populate Hex1's details lookup key
                if item == 6: hex1Key[i] = 8 #revert to unmoving line number
                elif item == 9: hex1Key[i] = 7 #revert to unmoving line number
                else: hex1Key[i] = item #no change
                i = i + 1 #increment counter    
            [self.hex1.number, self.hex1.name] = self.__GetHexDetails(hex1Key) #lookup Hex1 details
            self.hex1.infoSource = 'pyching_int_data.in'+self.hex1.number+'data()'
            if self.hex1.lineValues != hex1Key: #if there are some moving lines in Hex1
                i = 0 #used as a counter in the loop below
                for item in self.hex1.lineValues: #populate Hex2.lineValues
                    if item == 6: self.hex2.lineValues[i] = 7 #move to new line number
                    elif item == 9: self.hex2.lineValues[i] = 8 #move to new line number
                    else: self.hex2.lineValues[i] = item #no change
                    i = i + 1 #increment counter      
                [self.hex2.number, self.hex2.name] = self.__GetHexDetails(self.hex2.lineValues) #lookup Hex2 details
                self.hex2.infoSource = 'pyching_int_data.in'+self.hex2.number+'data()'

    def SetQuestion(self, questionText: str) -> None:
        """
        used to set the Hexagrams.question attribute from outside this module, public method
        """
        self.question = questionText
    
    def __HexStorage(self, file: Path | str, action: str) -> Optional[tuple[str, str]]:
        """
        Store or load a Hexagrams instance to/from disk file using JSON format.
        Falls back to pickle for loading old .psv files and migrates them automatically.

        Args:
            file: Path to the reading file
            action: 'save' or 'load'

        Returns:
            For 'load': saveFileID tuple for verification
            For 'save': None
        """
        file = Path(file)  # Ensure we have a Path object

        try:
            # Failsafe if user deleted ~/.pyching while program running
            if not pyching.savePath.exists():
                pyching.savePath.mkdir(parents=True, exist_ok=True)
        except (RuntimeError, OSError):
            pass  # If we can't determine home, following operations will handle the error

        if action == 'save':
            # Always save as JSON
            reading_data = {
                'file_id': {
                    'type': pyching.saveFileID[0],
                    'version': pyching.saveFileID[1]
                },
                'reading': {
                    'question': self.question,
                    'oracle': self.oracle,
                    'hex1': {
                        'number': self.hex1.number,
                        'name': self.hex1.name,
                        'lineValues': self.hex1.lineValues,
                        'infoSource': self.hex1.infoSource
                    },
                    'hex2': {
                        'number': self.hex2.number,
                        'name': self.hex2.name,
                        'lineValues': self.hex2.lineValues,
                        'infoSource': self.hex2.infoSource
                    },
                    'currentLine': self.currentLine,
                    'currentOracleValues': self.currentOracleValues
                }
            }

            try:
                with open(file, 'w') as f:
                    json.dump(reading_data, f, indent=2)
            except (IOError, OSError) as e:
                raise IOError(f"Unable to save reading to {file}") from e

        elif action == 'load':
            # Try JSON first, fall back to pickle for old files
            loaded_from_pickle = False

            try:
                # Attempt to load as JSON
                with open(file, 'r') as f:
                    reading_data = json.load(f)

                # Extract data from JSON structure
                file_id = (reading_data['file_id']['type'], reading_data['file_id']['version'])
                self.question = reading_data['reading']['question']
                self.oracle = reading_data['reading']['oracle']

                # Restore hex1
                hex1_data = reading_data['reading']['hex1']
                self.hex1.number = hex1_data['number']
                self.hex1.name = hex1_data['name']
                self.hex1.lineValues = hex1_data['lineValues']
                self.hex1.infoSource = hex1_data['infoSource']

                # Restore hex2
                hex2_data = reading_data['reading']['hex2']
                self.hex2.number = hex2_data['number']
                self.hex2.name = hex2_data['name']
                self.hex2.lineValues = hex2_data['lineValues']
                self.hex2.infoSource = hex2_data['infoSource']

                self.currentLine = reading_data['reading']['currentLine']
                self.currentOracleValues = reading_data['reading']['currentOracleValues']

                return file_id

            except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
                # Not valid JSON or wrong structure, try pickle (old format)
                try:
                    with open(file, 'rb') as f:
                        hexData = pickle.load(f)

                    # Extract data from pickle tuple
                    saveFileID, self.question, self.oracle, self.hex1, self.hex2, \
                        self.currentLine, self.currentOracleValues = hexData

                    loaded_from_pickle = True

                    # Auto-migrate: rename old pickle file and save as JSON
                    backup_file = Path(str(file) + '.backup')
                    try:
                        file.rename(backup_file)
                        # Now save as JSON in the original location
                        self.__HexStorage(file, 'save')
                    except (IOError, OSError):
                        # If migration fails, continue anyway - we have the data
                        pass

                    return saveFileID

                except Exception as e:
                    # Both JSON and pickle failed
                    raise IOError(f"Unable to load reading from {file} (tried JSON and pickle)") from e

            except (IOError, OSError) as e:
                # File doesn't exist or can't be read
                raise IOError(f"Unable to read file {file}") from e

    def Save(self, file: Path | str) -> None:
        """
        save instance data to disk file, public method

        this function should be called in a
        try:
        except IOError:
        block, to handle potential disk IO errors
        """
        #fileName = time.strftime('%Y_%m_%d_%H_%M_%S.sav', time.localtime(time.time()))
        try:
            self.__HexStorage(file, 'save')
        except IOError:  # pass the error back up the line
            raise  # re-raise the exception

    def Load(self, file: Path | str) -> Optional[tuple[str, str]]:
        """
        load instance data from disk file, public method, returns savefile version

        this function should be called in a
        try:
        except IOError:
        block, to handle potential disk IO errors
        """
        try:
            version = self.__HexStorage(file, 'load')
        except IOError:  # pass the error back up the line
            raise  # re-raise the exception
        else:
            return version  # to enable savefile version check if required
            
    def ReadingAsText(self) -> str:
        """
        create a multi-line text representation of the reading as a formatted string, public method,
        returns the string
        """
        #textReading = [] 
        
        lineStrings = {6:'---X---',7:'-------',8:'--- ---',9:'---O---',0:''}#the 0 takes care of an empty Hex2 
        linePositions = {1:'bottom',2:'second',3:'third',4:'fourth',5:'fifth',6:'topmost'}
        lineTypes = {6:'(6 moving yin)',7:'(7 yang)',8:'(8 yin)',9:'(9 moving yang)',0:''}#the 0 takes care of an empty Hex2 
        
        textReadingParts = []

        textReadingParts.append( '\n              '+self.hex1.number.ljust(2)+\
                        ' '+self.hex1.name.ljust(30)+\
                        ' '+self.hex2.number.ljust(2)+' '+self.hex2.name+'\n\n' )
        
        for i in range(5,-1,-1):
            if i == 3: 
                if (6 in self.hex1.lineValues) or (9 in self.hex1.lineValues): #if there are moving lines
                    separator = '  becomes  '
                else:
                    separator = '  no moving lines'
            else:
                    separator = '           '
            textReadingParts.append( ' '+linePositions[i +1].rjust(9)+'   '+lineStrings[self.hex1.lineValues[i]]+\
                            ' '+lineTypes[self.hex1.lineValues[i]].ljust(15)+separator+\
                            lineStrings[self.hex2.lineValues[i]]+' '+lineTypes[self.hex2.lineValues[i]]+'\n'  )
        
        textReadingParts.append('\n '+self.question+'\n\n')

        textReading = ''.join(textReadingParts)

        return textReading

#
# utility routines 
######################

def Storage(file: Path | str, data: Any = None) -> Any:
    """
    store or load data to/from file using pickler

    data should be a tuple of data items if storing, or None if loading
    returns an unpickled tuple of data items on successful load

    this function should be called in a
    try:
    except IOError:
    except Exception:
    block, to handle potential disk IO and pickle/unpickle errors
    """
    if data: openType = 'wb'
    else: openType = 'rb'
    try:
        pickleFile = open(file, openType)
    except IOError:
        raise #re-raise the exception to pass it back up the line
    else: #no exception, so proceed
        try:
            try:
                if data: #pickle required data
                    pickle.dump(data, pickleFile)
                else: #unpickle data
                    pickleData = pickle.load(pickleFile)
                    return pickleData
            except Exception as e:
                if data:
                    raise Exception('pychingPickleError') from e
                else:
                    raise Exception('pychingUnpickleError') from e
        finally: pickleFile.close()
