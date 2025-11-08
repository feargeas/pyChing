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
import sys, os, random, pickle, time
from functools import reduce

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
    def __init__(self):
        self.number = ''
        self.name = ''
        self.lineValues = [0,0,0,0,0,0]
        self.infoSource = None

#public classes
class PychingAppDetails:
    """
    holds information about a running instance of the pyching application, public class
    """
    def __init__(self,createConfigDir=1):
        self.title = 'pyChing'
        self.version = '1.2.2'
        self.os = sys.platform
        self.osType = os.name
        self.execPath = self.GetProgramDir() + os.sep
        self.configPath=self.GetUserCfgDir('.pyching')
        self.savePath=self.configPath
        self.configFile=os.path.join(self.configPath,'pychingrc')
        self.saveFileExt = '.psv'
        self.internalImageExt = '.#@~'
        self.internalHtmlExt = '.~@#'
        self.saveFileID = ('pyching_save_file',self.version)
        self.emailAddress = 'elguavas@users.sourceforge.net'
        self.webAddress = 'http://pyching.sourceforge.net'

    def GetProgramDir(self):
        """
        return the filesystem directory where this program file resides.
        (ie the applications exec or import directory.)
        """
        if __name__ != '__main__': # we were imported
            appDir=os.path.dirname(__file__)
        else: # we were exec'ed (for testing only)
            appDir=os.path.abspath(sys.path[0])
        return appDir

    def GetUserCfgDir(self,cfgDir):
        """
        Creates (if required) and returns a filesystem directory for storing 
        user config files.
        """
        userDir=os.path.expanduser('~')
        if userDir != '~': #'HOME' exists as a key in os.environ
            if not os.path.exists(userDir):
                warn=('\n Warning: HOME environment variable points to\n '+
                        userDir+'\n but the path does not exist.\n')
                sys.stderr.write(warn)
                userDir='~'
        if userDir=='~': #we still don't have a home directory
            #I guess we must simply default to os.getcwd()
            userDir = os.getcwd() #hack for no real homedir
        userDir=os.path.join(userDir,cfgDir)    
        if not os.path.exists(userDir):
            try: #make the config dir if it doesn't exist yet 
                os.mkdir(userDir)
            except IOError:
                warn=('\n Warning: unable to create user config directory\n '+
                        userDir+'\n')
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
    def __init__(self, oracleType='coin'):
        """
        initialise self by setting oracle type
        defaults to coin, if specified must be a valid oracle type (coin or yarrow)
        """
        #public data attributes - should read but not written to from outside this module
        #any attributes that need to be modified from outside this module have a 'set_xxx'
        #method available below
        self.question = ''#use SetQuestion (below) to set this attribute from outside this module
        self.oracle = oracleType #oracle being used
        self.hex1 = Hexagram() #Hexagram 1 data structure
        self.hex2 = Hexagram() #Hexagram 2 data structure
        self.currentLine = 0 #current line being cast in Hex1
        self.currentOracleValues = [] #list of oracle values for current line

    def __GetHexDetails(self, hexKey):
        """
        lookup hex name and number, private method
        
        hexKey value should be a list of the non-moving line numbers for the 
        Hexagram being enquired upon (Hex?.Key)
        returns a list of Hexagram details in the form [number, name]
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

    def NewLine(self):
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

    def SetQuestion(self, questionText):
        """
        used to set the Hexagrams.question attribute from outside this module, public method
        """
        self.question = questionText
    
    def __HexStorage(self, file, action):
        """
        store or load a Hexagrams instance to/from disk file using the utility routine
        Storage(), private method

        this private method should be called from the public load and save 
        routines below. action should be 'save' or 'load' .
        """
        if os.path.expanduser('~') != '~': #unix-style home directories
            if not os.path.exists(pyching.savePath): #failsafe if user deleted ~/.pyching while program running :-)
                os.mkdir(pyching.savePath)#make the save dir
        try:
            if action == 'save':
                hexData = (pyching.saveFileID, self.question, self.oracle, self.hex1, 
                                self.hex2, self.currentLine, self.currentOracleValues)
                Storage(file, data=hexData)
            elif action == 'load': 
                hexData = Storage(file)
        except IOError: #pass the error back up the line
            raise #re-raise the exception
        else: #no exception, so proceed
            if action == 'load':
                saveFileID, self.question, self.oracle, self.hex1, self.hex2, \
                                self.currentLine, self.currentOracleValues = hexData
                return saveFileID #to enable savefile verification and version checking

    def Save(self, file):
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
        except IOError: #pass the error back up the line
            raise #re-raise the exception

    def Load(self, file):
        """
        load instance data from disk file, public method, returns savefile version

        this function should be called in a 
        try:
        except IOError:
        block, to handle potential disk IO errors
        """
        try:
            version = self.__HexStorage(file, 'load')
        except IOError: #pass the error back up the line
            raise #re-raise the exception
        else:
            return version #to enable savefile version check if required
            
    def ReadingAsText(self):
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

def Storage(file, data=None):
    """
    store or load data to/from file using pickler

    data should be a list of data items if storing, or None if loading
    returns an unpickled list of data items on successful load

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
