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
tkinter interface module for pyching
"""

#python library imports
import sys, os, time, copy, htmllib, formatter

#tkinter imports
from tkinter import *
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
import tkinter.colorchooser as tkColorChooser

#pyChing source specific imports
import pyching_engine, pyching_cimages, pyching_idimage_data
import pyching_int_data, pyching_hlhtx_data 

#smg library module imports
from smgDialog import smgDialog
from smgHtmlView import smgHtmlView
from smgAbout import smgAbout

class WidgetColors:
    """
    colours for widgets in the reading display area
    """
    def __init__(self):
        #maybe colour defaults for all platforms
        #and platform defaults if started with a --mono switch (?)
        #if pyching.osType in ('posix','nt'): #non-default values for X & win32 style tk widgets
        #self.BgReading = '#7e7e7e'
        #self.bgReading = '#cd5c5c'
        self.bgReading = '#323c4a'
        self.bgLabelHint = '#FFE4B5'
        self.fgLabelHint = '#000000'
        #self.fgLabelPlaces = '#D3D3D3'
        #self.fgLabelPlaces = '#F08080'
        self.fgLabelPlaces = '#FFA07A'
        self.fgLabelHexTitles = '#FFFFFF'
        self.fgLabelLines = '#FFFFFF'
        self.fgMessageQuestion = '#FFFFFF'
        self.lineBody = '#DAA520'
        self.lineHighlight = '#EEE8AA'
        self.lineShadow = '#B8860B'
        #self.bgHtmlViewer = '#e8e8e8'
        #self.fgHtmlViewer = '#000000'
        #else: #values default to the platform standards
        # self.bgReading = None
        # self.bgLabelHint = None
        # self.fgLabelHint = None
        # self.fgLabelPlaces = None
        # self.fgLabelHexTitles = None
        # self.fgLabelLines = None
        # self.fgMessageQuestion = None
        # self.lineBody = 'Gray'
        # self.lineHighlight = 'LightGray'
        # self.lineShadow = 'DarkGray'

class WidgetFonts:
    """
    fonts for widgets in the main window
    """
    def __init__(self):
        if pyching.osType == 'posix': #non-default values for X style tk widgets
            self.menu = '-*-Helvetica-Normal-R-*--*-120-*-*-*-*-ISO8859-1'
            self.button = '-*-Helvetica-Normal-R-*--*-120-*-*-*-*-ISO8859-1'
            self.label = '-*-Helvetica-Normal-R-*--*-120-*-*-*-*-ISO8859-1'
            self.labelHexTitles = '-*-Helvetica-Bold-R-*--*-140-*-*-*-*-ISO8859-1'
            self.labelLineHint = '-*-Helvetica-Normal-R-*--*-120-*-*-*-*-ISO8859-1'
        elif pyching.osType == 'nt': #values for win32 style tk widgets
            self.menu = None
            self.button = None
            self.label = None
            self.labelHexTitles = '-*-Helvetica-Bold-R-*--*-150-*-*-*-*-ISO8859-1'
            self.labelLineHint = None
        else: #use default values for any other (untested :-) platform
            self.menu = None
            self.button = None
            self.label = None
            self.labelHexTitles = None
            self.labelLineHint = None

class WindowMain:
    """
    main application window
    """
    def __init__(self, master): 
        self.master = master
        self.master.resizable(height=FALSE,width=FALSE)
        #self.master.colormapwindows([self.master])#debug, does this solve the 256 color problem??
        self.images = pyching_cimages.CoinImages()
        try:
            self.master.iconbitmap(bitmap='@'+pyching.execPath+'/icon.xbm')
        except TclError:
            #sys.stderr.write("can't load icon bitmap")
            pass #just ignore this
        self.master.title(pyching.title + '  ' + pyching.version)
        
        #application-wide event bindings
        self.master.bind('<F1>',self.HelpBinding) #help key #bind_all
        self.master.bind('<Alt-c>',self.CastButtonBinding) #cast button
        self.master.bind('<Alt-v>',self.ViewHex1InfoButtonBinding) #view hex 1 info button
        self.master.bind('<Alt-i>',self.ViewHex2InfoButtonBinding) #view hex 2 info button
        
        #application-wide protocol bindings
        self.master.protocol("WM_DELETE_WINDOW", self.Quit)

        #configuration attributes
        self.showPlaces = BooleanVar()
        self.showPlaces.set(TRUE)
        self.showLineHints = BooleanVar()
        self.showLineHints.set(TRUE)
        self.castAll = BooleanVar()
        self.castAll.set(TRUE)
        #instantiate default colour and font values
        self.colors = WidgetColors() 
        self.fonts = WidgetFonts() 

        #load configuration file (if any)
        self.LoadSettings()

        self.MakeMenus(self.master)

        self.MakeStatusBar(self.master)

        #main frame
        frameMainBevel = Frame(self.master,borderwidth=2,relief=SUNKEN,highlightthickness=0)
        frameMainBevel.pack(expand=TRUE,fill=BOTH,padx=4)#used as a bevel for the main frame
        self.frameMain = Frame(frameMainBevel,bg=self.colors.bgReading)#highlightthickness=4,borderwidth=4,relief=SUNKEN)#,borderwidth=1,relief=SOLID
        self.frameMain.pack(expand=TRUE,fill=BOTH)
        
        self.MakeCastDisplay(self.frameMain)
        
        self.MakeQuestionDisplay(self.frameMain)

        self.MakeHexDisplay(self.frameMain)

        self.hexes = None #so we can test if a reading has been performed yet
    
    def Quit(self):
        #print 'bye now'#debug
        self.master.quit()
        
    def __AddMenu(self,parent,title):
        if title == 'Help': menuName = 'help'#name option to right justify help menu under X
        else: menuName = None
        _menu = Menu(parent,name=menuName,tearoff=0,font=self.fonts.menu)#create the menu
        if parent == self.master:#this is the menubar itself
            parent.configure(menu=_menu)#make _menu the menubar
            _menu.configure(borderwidth=0)
        else: #this is a dropdown from the menubar  
            parent.add_cascade(label=title,underline=0,menu=_menu)#add the menu to the menubar
        return _menu

    def MakeMenus(self, parent):
        self.menuMain = self.__AddMenu(parent,'')#create the menubar
        self.menuMainFile = self.__AddMenu(self.menuMain,'File')#create the file menu 
        self.menuMainSettings = self.__AddMenu(self.menuMain,'Settings')#create the settings menu 
        self.menuMainHelp = self.__AddMenu(self.menuMain,'Help')#create the help menu 
        
        def AddMenuItems(menu, items):
            for item in items:
                if item[0] == 's':#add a separator
                    menu.add_separator()
                elif item[0] == 'c':#add a command  
                    menu.add_command(label=item[1],underline=item[2],command=item[3])
                elif item[0] == 'k':#add a checkbutton
                    menu.add_checkbutton(label=item[1],underline=item[2],command=item[3],variable=item[4])  
                elif item[0] == 'r':#add a radiobutton
                    menu.add_radiobutton(label=item[1],underline=item[2],command=item[3],variable=item[4],value=item[5])  
                #elif item[0] == 'm':#add a submenu
                # pass #not implemented 
        
        AddMenuItems(self.menuMainFile,(('c','Load Reading...',0,self.LoadReading),
                                                    ('c','Save Reading...',0,self.SaveReading),('s',),
                                                    ('c','Save Reading As Text...',16,self.SaveReadingAsText),('s',),
                                                    ('c','Exit',1,self.Quit)) )
        AddMenuItems(self.menuMainSettings,(('k','Show Places',5,self.__ToggleLabelsPlaces,self.showPlaces),
            ('k','Show Line Hints',10,None,self.showLineHints),('s',),
            ('r','Cast Each Line Separately',10,None,self.castAll,FALSE),
            ('r','Cast Entire Hexagram Automatically',12,None,self.castAll,TRUE),('s',),
            ('c','Configure Colors...',10,self.SetColors),('s',),
            ('c','Save Settings',0,self.SaveSettings)) )
        AddMenuItems(self.menuMainHelp,(
            ('c','Using '+pyching.title,0,self.ShowHelpUsingPyching),
            ('c','Introduction to the I Ching',0,self.ShowHelpIChingIntro),
            ('c','Browse Hexagram Information',0,self.ShowHelpHexInfo),
            ('s',),
            ('c','About '+pyching.title+'...',0,self.ShowAbout)) )
        #self.ShowText(title='Help - Using '+pyching.title,textFile='help.txt')),
        self.menuMainFile.entryconfigure(1,state=DISABLED)#disable save item by default
        self.menuMainFile.entryconfigure(3,state=DISABLED)#disable save as text item by default
        
    def HelpBinding(self,event):
        #main window binding for the F1 key
        #try:
        self.ShowHelpUsingPyching()
        #except KeyError:
        # pass #this error is raised while pressing F1 over a tk file dialog, ignore it

    def CastButtonBinding(self,event):
        #binding for the Meta-c hotkey on buttonCast
        if self.buttonCast.cget('state') == 'normal': #if the button isn't disabled
            self.buttonCast.invoke()
    
    def ViewHex1InfoButtonBinding(self, event):
        #binding for the Meta-v hotkey on buttonViewHex1Info
        if self.buttonViewHex1Info.cget('state') == 'normal': #if the button isn't disabled
            self.buttonViewHex1Info.invoke()

    def ViewHex2InfoButtonBinding(self, event):
        #binding for the Meta-i hotkey on buttonViewHex1Info
        if self.buttonViewHex2Info.cget('state') == 'normal': #if the button isn't disabled
            self.buttonViewHex2Info.invoke()

    def ShowHelpUsingPyching(self):
        self.ShowHtml(title=pyching.title + ' - Help',
                htmlSource='pyching_hlhtx_data.hlHelpData()',
                index='pyching_hlhtx_data.hlHelpData()')
        
    def ShowHelpIChingIntro(self):
        self.ShowHtml(title=pyching.title + ' - Help',
                htmlSource='pyching_hlhtx_data.hlIntroData()',
                index='pyching_hlhtx_data.hlHelpData()')
            
    def ShowHelpHexInfo(self):
        self.ShowHtml(title=pyching.title + ' - Hexagram Infomation Browser',
                hexBrowser=1)
            
    def ShowText(self,title=None,textFile=None):
        #dialogTxt = DialogShowHtml(self.master,title=title,htmlFile=textFile,
        #    plainText=1)
        dialogTxt = smgHtmlView(self.master,title=title,htmlSource=textFile,
                plainText=1)

    def ShowHtml(self,title=None,htmlSource=None,index=None,hexBrowser=0):
        #dialoghtml = DialogShowHtml(self.master,title=title,htmlFile=textFile,
        #    indexFile=indexFile)
        dialoghtml = smgHtmlView(self.master,title=title,
                htmlSource=htmlSource,
                internalLink=None,index=index,hexBrowser=hexBrowser)
        
    def ShowAbout(self):
        #dialogAbout = DialogAbout(self.master,currentColors=self.colors)
        aboutPicData="""R0lGODlhMgAyAKEAAAICBP4CBAIC/P///yH+Dk1hZGUgd2l0aCBHSU1QACH5BAEKAAMALAAA
AAAyADIAAAL+nI+ZwO0Ko1SOhYvvmzw2YWUi1nTmwAgqMLYic0rp6tYkEC+AStt+AMvNeKyf
L2ga9oxHXEe5ZNqQnh0v2nIwqZQrcXot/pwQqxdUM3+NZAR0nT2Lm90zNqO+pxd2+CiPJtUG
GAbmx3bw5jX31yB1Y0C4+EjpJDlJuRXZh5k5hsIp58l2acc42hhqeoqqUcoZ0nqjGuooq0i7
GJuJmyvHOvbqGwacJjxcKHiMfDgFyuxbjLcJnStNQl1New0UuUzcG2icyDxXKj2IfHqJzhf9
B7un8/4Sn9VGbg3fB4zvRq+hVpYJ4cC9WudvnjZRLxJS+KaKEReCEPk1zIGiIkMfVxgTaVwy
EWNBU5A6lhkJgkUJkxRxVXDIssrLkCYKAAA7"""
        dialogAbout = smgAbout(self.master,title='About '+pyching.title, 
                appTitle=pyching.title,
                version='Version: '+pyching.version,
                copyright='Copyright (c) 1999-2003 Stephen M. Gava',
                licence='Released under the GNU General Public Licence',
                email='email:  '+pyching.emailAddress,
                www='web:  '+pyching.webAddress,
                pictureData=aboutPicData,
                licenceFile=pyching.execPath+'COPYING',
                creditsFile=pyching.execPath+'CREDITS',
                fontAppTitle=self.fonts.labelHexTitles,  
                fontText=self.fonts.label,
                fg=self.colors.fgLabelHexTitles,
                bg=self.colors.bgReading )
    
    def SetColors(self):
        dialogSetColors = DialogSetColors(self.master,currentColors=copy.copy(self.colors))
        if dialogSetColors.result: #user didn't cancel
            self.RepaintColors(dialogSetColors.result)    

    def SaveSettings(self):
        if os.path.expanduser('~') != '~': #unix-style home directories
            if not os.path.exists(pyching.configPath): #failsafe if user deleted ~/.pyching while program running :)
                os.mkdir(pyching.configPath)#make the config dir
        castAllValue = self.castAll.get()
        showPlacesValue = self.showPlaces.get()
        showLineHintsValue = self.showLineHints.get()
        configData = (pyching.version,self.colors,castAllValue,showPlacesValue,showLineHintsValue)
        try:
                pyching_engine.Storage(pyching.configFile, data=configData)
        except IOError:
            #print '\n error: unable to write config file', pyching.configFile
            tkMessageBox.showerror(title='File Error',
                            message='Unable to write configuration file:\n'+pyching.configFile)
        else:
            #print '\n saved file:', fileName
            self.labelStatus.configure(text='saved settings')

    def LoadSettings(self):
        if os.path.exists(pyching.configFile): #if a saved configuration exists
            try:
                    configData= pyching_engine.Storage(pyching.configFile, data=None)
            except IOError: #just silently let this past??
                #print '\n error: unable to read configuration file', pyching.configFile
                sys.stderr.write('\n error (IOError): unable to read configuration file'+pyching.configFile+'\n')
                #tkMessageBox.showerror(title='File Error',
                #       message='Unable to read configuration file:\n'+pyching.configFile)
                pass
            except 'pychingUnpickleError': #just silently let this past??
                #print '\n error: invalid configuration file', pyching.configFile
                sys.stderr.write('\n error (pychingUnpickleError): invalid configuration file'+pyching.configFile+'\n')
                #tkMessageBox.showerror(title='File Error',
                #       message='Invalid configuration file:\n'+pyching.configFile)
                pass
            else:
                #version can be tested against pyching.version for config file compatability
                version,self.colors,castAllValue,showPlacesValue,showLineHintsValue = configData
                self.castAll.set(castAllValue)
                self.showPlaces.set(showPlacesValue)
                self.showLineHints.set(showLineHintsValue)
                #print '\n loaded config file:', pyching.configFile
        
    def __HideLabel(self,label):
        label.configure(fg=label.cget('bg'))#fg=bg to hide label  
        
    def __ToggleLabelsPlaces(self):
        if self.hexes: #if there's been a reading yet
            for label in self.labelsHexPlaces:
                if label.cget('fg') == self.colors.fgLabelPlaces:
                    self.__HideLabel(label)
                else:
                    label.configure(fg=self.colors.fgLabelPlaces)
    
    def ClearReading(self): 
        self.HideInfoButtons()#get rid of any info buttons  
        for coin in self.labelsCoins:#clear coins display
            coin.configure(image=self.images.coinFrames[16])
        #blank both hexagram displays
        for i in range(2):
            for line in self.hexLines[i]:
                line.Draw(linetype=None)
        for label in self.labelsHexPlaces:
            self.__HideLabel(label)
        for key in self.labelsNoMovingLines.keys():
            self.labelsNoMovingLines[key].lower()#hide the 'no moving lines' labels
        self.__HideLabel(self.labelBecomes)     
        self.labelH1Title.configure(text='')
        self.labelH2Title.configure(text='')
        self.messageQuestion.configure(text='')
        #wiped stuff still appears on win32?? - try below
        self.master.update()
    
    def CastHexes(self):
        self.labelLineHint.show = 0 #disable line hints
        #get the question
        questionDialog = DialogGetQuestion(self.master)
        self.master.update()#makes sure the main app window gets redrawn properly (seems only to be a problem on win32)
        if questionDialog.result: #the user didn't cancel
            self.ClearReading()
            for coin in self.labelsCoins:#initialise coins display
                coin.configure(image=self.images.coinFrames[0])
            self.hexes = pyching_engine.Hexagrams('coin')
            self.hexes.question = questionDialog.result
            self.ShowQuestion()
            if self.castAll.get():#cast all lines automatically
                self.CastAllLines()
            else:#cast 1 line at a time
                for menuItem in range(3,5):#disable cast-type changing while casting
                    self.menuMainSettings.entryconfigure(menuItem,state=DISABLED)
                self.buttonCast.configure(text='Cast Line 1 of 6',command=self.CastNextLine)
                self.labelStatus.configure(text='Waiting to cast line 1 of 6 ...')
        else: #the user cancelled
            self.labelLineHint.show = 1 #re-enable line hints
        
    def CastNextLine(self):
        self.buttonCast.configure(state=DISABLED)
        self.CastLine()
        self.buttonCast.configure(state=NORMAL)
        if self.hexes.hex1.lineValues[5] == 0:#if hex1 is'nt fully built yet
            self.buttonCast.configure(text='Cast Line '+str(self.hexes.currentLine+1)+' of 6')
            self.labelStatus.configure(text='Waiting to cast line '+str(self.hexes.currentLine+1)+ ' of 6 ...')
        else:#hex1 is fully built now
            for menuItem in range(3,5):#re-enable cast-type changing
                self.menuMainSettings.entryconfigure(menuItem,state=NORMAL)
            self.buttonCast.configure(text='Create 2nd Hexagram',command=self.BuildHex2)
            self.labelStatus.configure(text='Waiting to create 2nd hexagram ...')
            
    def CastAllLines(self,loadingSaveFile=0):
        self.buttonCast.configure(state=DISABLED)
        if loadingSaveFile: 
            self.hexes.currentLine = 0
            self.ShowQuestion()
        for line in self.hexLines[0]:#build and display hexagram 1
            if loadingSaveFile: #increment the current line
                self.hexes.currentLine = self.hexes.currentLine + 1
            self.CastLine(loadingFromFile=loadingSaveFile)
            self.master.update_idletasks()
            if not loadingSaveFile: time.sleep(1)#pause to let user see the thrown coins
        self.BuildHex2()#show second hexagram
        self.buttonCast.configure(state=NORMAL)
        #self.master.update_idletasks()

    def CastLine(self,loadingFromFile=0):
        if not loadingFromFile:
            self.hexes.NewLine()
            self.labelStatus.configure(text='Casting Line '+str(self.hexes.currentLine)+' of 6 ...')
            #for spins in range(3):
            for spins in range(2):
                    for frameNum in range(14):
                        for coin in self.labelsCoins:
                            coin.configure(image=self.images.coinFrames[frameNum])
                            self.master.update_idletasks()
                        #time.sleep(0.06)
                        #time.sleep(0.04)
                        time.sleep(0.02)

            for i in range(3):
                self.labelsCoins[i].configure(image=self.images.coinFrames[self.hexes.currentOracleValues[i]+12])
                self.master.update_idletasks()

        #self.hexes.hex1.lineValues[self.hexes.currentLine-1] = 8#debug!!
        if self.showPlaces.get():#if places should be shown
            self.labelsHexPlaces[self.hexes.currentLine-1].configure(fg=self.colors.fgLabelPlaces)#show the place name
            #self.__ShowLabel(self.labelsHexPlaces[self.hexes.currentLine-1])#show the place name
        self.hexLines[0][self.hexes.currentLine-1].Draw(self.hexes.hex1.lineValues[self.hexes.currentLine-1])     
        #if loadingFromFile: self.hexLines[0][self.hexes.currentLine-1].update()
        #self.master.update_idletasks()
    
    def BuildHex2(self):
        #if self.hexes.hex1.lineValues[5] != 0:#hex1 is fully built
        self.labelH1Title.configure(text=self.hexes.hex1.number+'.  '+self.hexes.hex1.name)
        if self.hexes.hex2.lineValues[0] != 0:#if there were moving lines
            self.labelBecomes.configure(fg=self.colors.fgLabelLines)#show the 'becomes' label
            #self.__ShowLabel(self.labelBecomes)#show the 'becomes' label
            self.labelH2Title.configure(text=self.hexes.hex2.number+'.  '+self.hexes.hex2.name)
        #self.hexes.hex2.lineValues = [0,0,0,0,0,0]#debug
        i = 0#a counter
        for line in self.hexLines[1]:#display hexagram 2
            if self.hexes.hex2.lineValues[i] == 0:#empty hexagram 2
                #for lines 3,4,5 display 'no, moving, lines' message
                if self.labelsNoMovingLines.has_key(i):
                    self.labelsNoMovingLines[i].tkraise()
                    #self.labelsNoMovingLines[i].update()
                    #print self.labelsNoMovingLines[i].cget('text') #debug
            else:#hexagram2 has lines
                line.Draw(self.hexes.hex2.lineValues[i])
            self.master.update_idletasks()
            i = i+1#increment counter

        self.labelStatus.configure(text='')
        self.labelLineHint.show = 1 #enable line hints

        for coin in self.labelsCoins:#blank coins display
            coin.configure(image=self.images.coinFrames[16])

        if not self.castAll.get():#if we were casting a line at a time
            self.buttonCast.configure(text='Cast New Hexagram',command=self.CastHexes)
        
        self.ShowInfoButtons()#show the info buttons

        self.menuMainFile.entryconfigure(1,state=NORMAL)#enable save menuitem
        self.menuMainFile.entryconfigure(3,state=NORMAL)#enable save as text menuitem

    def MakeCastDisplay(self, parent):
        self.frameCast = Frame(parent,bg=self.colors.bgReading)
        self.frameCast.pack(anchor=NW,side=TOP)#,padx=20,pady=20
        
        self.buttonCast = Button(self.frameCast,text='Cast New Hexagram',underline=0,
                        width=20,bg=None,fg=None,font=self.fonts.button,highlightthickness=0,
                        takefocus=FALSE,command=self.CastHexes)
        #self.buttonCast.focus_set()
        self.buttonCast.grid(column=0,row=0,sticky=NW,padx=20,pady=20)

        self.labelsCoins = []
        for i in range(3):
            self.labelsCoins.append(Label(self.frameCast,image=self.images.coinFrames[16],
                            bg=self.colors.bgReading) )
            self.labelsCoins[i].grid(column=i+1,row=0,padx=10,pady=10)

        #the following widgets are not initially shown or enabled
        self.frameInfoButtons = Frame(self.frameCast,bg=self.colors.bgReading)
        self.buttonViewHex1Info = Button(self.frameInfoButtons,text=None,underline=0,
                        width=30,bg=None,fg=None,font=self.fonts.button,highlightthickness=0,
                        takefocus=FALSE,state=DISABLED,command=self.ViewHex1Info)
        self.buttonViewHex2Info = Button(self.frameInfoButtons,text=None,underline=1,
                        width=30,bg=None,fg=None,font=self.fonts.button,highlightthickness=0,
                        takefocus=FALSE,state=DISABLED,command=self.ViewHex2Info)
                
    def ShowInfoButtons(self):
        #show, setup and enable the required info buttons
        textStub = 'View information on:  '
        if self.hexes.hex2.lineValues[0] != 0:#there is a hex 2
            self.buttonViewHex2Info.configure(text=textStub+self.hexes.hex2.number+
                            '. '+self.hexes.hex2.name,state=NORMAL)
            self.buttonViewHex2Info.grid(column=0,row=1)
            button1Pad = 5
        else:
            self.buttonViewHex2Info.grid_forget()
            button1Pad = 15

        self.buttonViewHex1Info.configure(text=textStub+self.hexes.hex1.number+
                            '. '+self.hexes.hex1.name,state=NORMAL)
        self.buttonViewHex1Info.grid(column=0,row=0,pady=button1Pad)

        self.frameInfoButtons.grid(column=1,row=0,columnspan=3,sticky=NW,pady=5)
        #self.frameInfoButtons.lift()

    def HideInfoButtons(self):
        #hide and disable the info buttons
        self.frameInfoButtons.grid_forget()
        self.buttonViewHex1Info.configure(state=DISABLED)
        self.buttonViewHex2Info.configure(state=DISABLED)

    def ViewHex1Info(self):
        self.ShowHtml(title='Hexagram Information - '+self.hexes.hex1.number+'. '+self.hexes.hex1.name,
                            htmlSource=self.hexes.hex1.infoSource)

    def ViewHex2Info(self):
        self.ShowHtml(title='Hexagram Information - '+self.hexes.hex2.number+'. '+self.hexes.hex2.name,
                            htmlSource=self.hexes.hex2.infoSource)

    def MakeHexDisplay(self, parent):
        self.frameHexes = Frame(parent,bg=self.colors.bgReading)
        self.frameHexes.pack(anchor=NW,side=TOP,padx=20)
                        
        self.frameSpacerC4R1 = Frame(self.frameHexes,height=8,bg=self.colors.bgReading)
        self.frameSpacerC4R1.grid(column=4,row=1)
        
        self.labelsHexPlaces = []
        labelsTexts = ('topmost','fifth','fourth','third','second','bottom')
        for labelNum in range(6):
            self.labelsHexPlaces.append(Label(self.frameHexes,text=labelsTexts[labelNum],
                            bg=self.colors.bgReading,fg=self.colors.bgReading,font=self.fonts.label) )#fg=bg because label starts off hidden
            self.__HideLabel(self.labelsHexPlaces[labelNum])
            self.labelsHexPlaces[labelNum].grid(column=0,row=labelNum+2,sticky=E)
        self.labelsHexPlaces.reverse()#puts the labels in order of appearance

        self.labelH1Title = Label(self.frameHexes,text='',bg=self.colors.bgReading,
                        fg=self.colors.fgLabelHexTitles,font=self.fonts.labelHexTitles)
        self.labelH1Title.grid(column=1,row=0)
        
        self.labelH2Title = Label(self.frameHexes,text='',bg=self.colors.bgReading,
                        fg=self.colors.fgLabelHexTitles,font=self.fonts.labelHexTitles)
        self.labelH2Title.grid(column=3,row=0)

        self.labelBecomes = Label(self.frameHexes,text='becomes',bg=self.colors.bgReading,
                        fg=self.colors.bgReading,font=self.fonts.label)#fg=bg because label starts off hidden
        #self.__HideLabel(self.labelBecomes)
        self.labelBecomes.grid(column=2,row=4)
        
        #lineTexts = ('no','moving','lines')#lineTexts[key-3]
        self.labelsNoMovingLines = {3:'no',4:'moving',5:'lines'}
        for key in self.labelsNoMovingLines.keys():
            self.labelsNoMovingLines[key] = Label(self.frameHexes,
                        text=self.labelsNoMovingLines[key],bg=self.colors.bgReading,
                        fg=self.colors.fgLabelLines,font=self.fonts.label)
            self.labelsNoMovingLines[key].grid(row=key,column=3)
            
        self.hexLines = ([],[])
        
        for hexNum in range(2):
            for lineNum in range(6):
                self.hexLines[hexNum].append(HexLine(self.frameHexes,
                                bindingEnter=self.ShowLineDetails,bindingLeave=self.ClearLineDetails,
                                currentColors=self.colors))
                if hexNum == 0: colNum = 1 
                else: colNum = 3 #set the corect grid column
                self.hexLines[hexNum][lineNum].grid(column=colNum,row=lineNum+2,padx=20,pady=1)
            self.hexLines[hexNum].reverse()#puts the labels in hex filling order
        
        self.frameSpacerC4R7 = Frame(self.frameHexes,width=20,bg=self.colors.bgReading)
        self.frameSpacerC4R7.grid(column=4,row=8)

        self.labelLineHint = Label(self.master,text=None,bg=self.colors.bgLabelHint,
                                            fg=self.colors.fgLabelHint,font=self.fonts.labelLineHint,
                                            borderwidth=1,relief=SOLID,padx=6)
        self.labelLineHint.place_forget() 
        #add an attribute to the hint label to indicate if it can currently be
        #shown or not (eg. hints should not be shown during hex building). 
        #this is independent of the user preference held in self.showLineHints .
        self.labelLineHint.show = 0 
    
    def ShowLineDetails(self,event):
        if  self.labelLineHint.show and event.widget.hint: #if hints can be shown and there is a hint for the line
            self.labelStatus.configure(text=event.widget.hint)#show line details on the status line
            if self.showLineHints.get():#if the user wants to see line details hints, show them
                self.labelLineHint.configure(text=event.widget.hint)
                self.labelLineHint.place(relx=0.1,rely=1.0,x=2,y=2,in_=event.widget)
                #self.labelLineHint.tkraise()
                self.labelLineHint.update()
                
    def ClearLineDetails(self,event):
        if event.widget.hint: #if there's a hint for the line
            self.labelStatus.configure(text='')
            if self.showLineHints.get():
                self.labelLineHint.configure(text=None)
                self.labelLineHint.place_forget() 

    def MakeQuestionDisplay(self,parent):
        #print self.frameMain.winfo_width()#cget('width')#.winfo_width()#cget(key)
        self.frameQuestion=Frame(parent,bg=self.colors.bgReading,borderwidth=2)
        self.frameQuestion.pack(anchor=SW,side=BOTTOM,expand=TRUE,fill=X,padx=10,pady=5)
        self.messageQuestion = Message(self.frameQuestion,width=20,text=None,justify=LEFT,
                                                 bg=self.colors.bgReading,fg=self.colors.fgMessageQuestion,
                                                 font=self.fonts.label)
        self.messageQuestion.pack(anchor=W)

    def ShowQuestion(self):
        #self.frameQuestion.configure(relief=GROOVE)
        self.messageQuestion.configure(width=self.frameQuestion.winfo_width(),
                                                 text=self.hexes.question)
    def HideQuestion(self):
        #self.frameQuestion.configure(relief=FLAT)
        self.messageQuestion.configure(width=20,text=None)

    def MakeStatusBar(self, parent):
        self.frameStatusBar = Frame(parent,borderwidth=2,relief=SUNKEN,highlightthickness=2)
        self.frameStatusBar.pack(anchor=SW,side=BOTTOM,fill=X,padx=2)#,expand=TRUE
        self.labelStatus = Label(self.frameStatusBar,
                        text=pyching.title + '  ' + pyching.version,font=self.fonts.label)
        self.labelStatus.pack()

        #button for debug/testing purposes only
        #self.buttonDebug = Button(self.frameStatusBar,text='DEBUG',command=self.DEBUG)
        #self.buttonDebug.pack(anchor=E)
 
    def DEBUG(self):
        #run any routines in test or debug from here
        print('begin debug\n')
        #
        print(sys.path)
        #
        print('\nend debug')
        
    def RepaintColors(self,newColors):
        oldColors=self.colors #save them for comparison below
        self.colors=newColors
        #these are always repainted
        self.frameMain.configure(bg=self.colors.bgReading)
        self.frameCast.configure(bg=self.colors.bgReading)
        for i in range(3):
            self.labelsCoins[i].configure(bg=self.colors.bgReading)
        self.frameHexes.configure(bg=self.colors.bgReading)
        self.frameInfoButtons.configure(bg=self.colors.bgReading)
        self.frameSpacerC4R1.configure(bg=self.colors.bgReading)
        self.frameSpacerC4R7.configure(bg=self.colors.bgReading)
        self.frameQuestion.configure(bg=self.colors.bgReading)
        self.labelLineHint.configure(bg=self.colors.bgLabelHint,fg=self.colors.fgLabelHint)
        self.messageQuestion.configure(bg=self.colors.bgReading,fg=self.colors.fgMessageQuestion)
        self.labelH1Title.configure(bg=self.colors.bgReading,fg=self.colors.fgLabelHexTitles)
        self.labelH2Title.configure(bg=self.colors.bgReading,fg=self.colors.fgLabelHexTitles)
        for key in self.labelsNoMovingLines.keys():
            self.labelsNoMovingLines[key].configure(bg=self.colors.bgReading,fg=self.colors.fgLabelLines)
        #the backgrounds of these are always repainted
        for hexNum in range(2):
            for lineNum in range(6):
                self.hexLines[hexNum][lineNum].configure(bg=self.colors.bgReading)
                self.hexLines[hexNum][lineNum].colors = self.colors #so they will draw correctly next time
        #self.frameMain.update()
        #the backgrounds of these are always repainted, and fg=bg to hide them as
        #fg will be repainted in the correct color below if required
        for labelNum in range(6):
            self.labelsHexPlaces[labelNum].configure(bg=self.colors.bgReading,fg=self.colors.bgReading)
        self.labelBecomes.configure(bg=self.colors.bgReading,fg=self.colors.bgReading)
        #the foreground of these are only repainted here if a reading has been performed
        #otherwise they will paint in the new colors next time they are shown
        if self.hexes: #a reading has been performed
            if self.showPlaces.get():#if places should be shown
                for labelNum in range(6):
                    self.labelsHexPlaces[labelNum].configure(fg=self.colors.fgLabelPlaces)
            if self.hexes.hex2.lineValues[0] != 0: #if there is a second hexagram
                self.labelBecomes.configure(fg=self.colors.fgLabelLines)
            #only redraw all lines now if their fg colors have changed
            if (oldColors.lineBody != self.colors.lineBody) or \
                            (oldColors.lineHighlight != self.colors.lineHighlight) or \
                            (oldColors.lineShadow != self.colors.lineShadow):
                for hexNum in range(2):
                    for lineNum in range(6):
                        self.hexLines[hexNum][lineNum].Draw(self.hexLines[hexNum][lineNum].value)
            elif oldColors.bgReading != self.colors.bgReading: #but if only the bg color has changed
                for hexNum in range(2): #repaint any 9 lines, to give the correct color in their inner circle
                    for lineNum in range(6):
                        if self.hexLines[hexNum][lineNum].value == 9:
                            self.hexLines[hexNum][lineNum].Draw(self.hexLines[hexNum][lineNum].value)
                
    def SaveReading(self):
        fileName = tkFileDialog.asksaveasfilename(parent=self.master,
                        title='Save Reading',defaultextension=pyching.saveFileExt,
                        filetypes=[(pyching.title+' save files','*'+pyching.saveFileExt)],
                        initialdir=pyching.savePath)
        #print fileName #debug
        if not fileName: return #user cancelled so get out
    
        #if not self.hexes: #we need an instance to work with
        # self.hexes = pyching_engine.Hexagrams()
        try: 
            #pass
            self.hexes.Save(fileName)
        except IOError:
            #print '\n error: unable to write save file', fileName
            tkMessageBox.showerror(title='File Error',
                            message='Unable to write save file:\n'+fileName)
        else:
            #print '\n saved file:', fileName
            self.labelStatus.configure(text='saved reading: '+fileName)
            
    def LoadReading(self):
        self.labelLineHint.show = 0 #disable line hints
        fileName = tkFileDialog.askopenfilename(parent=self.master,
                        title='Load Saved Reading',defaultextension=pyching.saveFileExt,
                        filetypes=[(pyching.title+' save files','*'+pyching.saveFileExt)],
                        initialdir=pyching.savePath)
        #print fileName #debug
        if not fileName: 
            self.labelLineHint.show = 1 #re-enable line hints
            return #user cancelled so get out

        tempHexes = pyching_engine.Hexagrams()
        try: 
            saveFileID = tempHexes.Load(fileName)
        except IOError:
            #print '\n error: unable to read save file', fileName
            tkMessageBox.showerror(title='File Error',
                            message='Unable to load save file:\n'+fileName)
        except 'pychingUnpickleError': #the file couldn't be unpickled, most likely it isn't a pickled file
            #print '\n error: unable to unpickle file', fileName
            tkMessageBox.showerror(title='Not A Save File',
                            message='The file you attempted to load:\n\n'+fileName+\
                                            '\n\nis not a '+pyching.title+' save file.')
        else:
            if not saveFileID[0] == pyching.saveFileID[0]: #this isn't a valid pyching savefile
                #print '\n invalid save file:', fileName
                tkMessageBox.showerror(title='Not A Save File',
                                message='The file you attempted to load:\n\n'+fileName+\
                                                '\n\nis not a '+pyching.title+' save file.')
            #elif not saveFileID[1] == pyching.saveFileID[1]: #savefile fails version check
            # pass #handle any savefile version issues here
            else:     
                self.hexes = tempHexes
                self.ClearReading()
                self.CastAllLines(loadingSaveFile=1)
                self.labelStatus.configure(text='loaded reading: '+fileName)
        
        self.labelLineHint.show = 1 #re-enable line hints

    def SaveReadingAsText(self):
        fileName = tkFileDialog.asksaveasfilename(parent=self.master,
                        title='Save Reading As Text',defaultextension='.txt',
                        filetypes=[('text files','*.txt')],
                        initialdir=pyching.savePath)
        if not fileName: return #user cancelled so get out
        
        textData = self.hexes.ReadingAsText()
        #print textData #debug
        try:
            textFile = open(fileName, 'w')
        except IOError: 
            #print '\n error: unable to create text file', fileName
            tkMessageBox.showerror(title='File Error',
                            message='Unable to create text file:\n'+fileName)
        else: #no exception, so proceed
            try:
                try:
                    textFile.write(textData)
                except IOError:
                    #print '\n error: unable to write text file', fileName
                    tkMessageBox.showerror(title='File Error',
                                    message='Unable to write text file:\n'+fileName)
            finally:
                textFile.close()

class HexLine(Canvas):
    """
    creates a hexagram line object
    """
    def __init__(self,parent,bindingEnter=None,bindingLeave=None,currentColors=None):
        self.value=None
        self.hint=None
        if currentColors: self.colors = currentColors
        else: self.colors = WidgetColors()
        Canvas.__init__(self,parent,height=25,width=145,bg=self.colors.bgReading,
                        takefocus=FALSE,highlightthickness=0)
        #self.tag_bind('all','<Enter>',bindingEnter)#when the mouse enters the drawing
        self.bind('<Enter>',bindingEnter)#when the mouse enters the canvas
        self.bind('<Leave>',bindingLeave)#when the mouse leaves the canvas

    def Draw(self,linetype=None):
        #draw the required linetype and set the relevant value and hint
        hints = {6: 'line value = 6 (moving yin)',7: 'line value = 7 (yang)',
                        8: 'line value = 8 (yin)',9: 'line value = 9 (moving yang)'}
        self.configure(bg=self.colors.bgReading)
        self.update()
        if linetype == 6:
            self.value=linetype
            self.hint=hints[linetype]
            self.DrawBevelRectangle(origin=(1,6),height=13,width=60)
            self.DrawBevelRectangle(origin=(84,6),height=13,width=60)
            self.DrawBevelX(origin=(62,2),height=20,width=20)
        elif linetype == 7:
            self.value=linetype
            self.hint=hints[linetype]
            self.DrawBevelRectangle(origin=(2,6),height=13,width=141)
        elif linetype == 8:
            self.value=linetype
            self.hint=hints[linetype]
            self.DrawBevelRectangle(origin=(2,6),height=13,width=60)
            self.DrawBevelRectangle(origin=(83,6),height=13,width=60)
        elif linetype == 9:
            self.value=linetype
            self.hint=hints[linetype]
            self.DrawBevelRectangle(origin=(2,6),height=13,width=60)
            self.DrawBevelRectangle(origin=(83,6),height=13,width=60)
            self.DrawBevelO(origin=(62,2),height=20,width=20)
        else: #blank the canvas (clear any existing drawing)  
            self.value=None
            self.hint=None
            self.delete('all')
    
    def DrawBevelRectangle(self,origin=(0,0),height=13,width=0,bevel=2):
        
        color=self.colors.lineBody
        highlightcolor=self.colors.lineHighlight,
        shadowcolor=self.colors.lineShadow
                
        #fill with fg colour
        self.create_rectangle( ((origin[0],origin[1]),
                        (origin[0]+width-1,origin[1]+height-1)),width=0,
                        outline=color,fill=color,tags='BODY')

        #draw bevels
        for i in range(bevel):
            #draw highlight bevel
            if pyching.osType == 'nt': #allow for differences in tk canvas on win32
                self.create_line( ((origin[0]+i,origin[1]+height-i-1),
                                (origin[0]+i,origin[1]+i),
                                (origin[0]+width-i,origin[1]+i)),width=1,fill=highlightcolor,tags='HIGHLIGHT')
            else: #just draw without above modifications
                self.create_line( ((origin[0]+i,origin[1]+height-i),
                                (origin[0]+i,origin[1]+i),
                                (origin[0]+width-i,origin[1]+i)),width=1,fill=highlightcolor,tags='HIGHLIGHT')
            
            #draw shadow bevel
            if pyching.osType == 'nt': #allow for differences in tk canvas on win32
                self.create_line(  ( (origin[0]+i+1,origin[1]+((height-i)-1)),
                                                            (origin[0]+(width-i),origin[1]+((height-i)-1)) ),
                                                            width=1,fill=shadowcolor,tags='SHADOW')
                self.create_line(  ( (origin[0]+(width-i)-1,origin[1]+((height-i)-1)),
                                                            (origin[0]+(width-i)-1,origin[1]+i) ),
                                                            width=1,fill=shadowcolor,tags='SHADOW')
            else: #just draw without above modifications
                self.create_line(  ( (origin[0]+i+1,origin[1]+((height-i)-1)),
                                                            (origin[0]+(width-i),origin[1]+((height-i)-1)) ),
                                                            width=1,fill=shadowcolor,tags='SHADOW')
                self.create_line(  ( (origin[0]+(width-i)-1,origin[1]+((height-i)-1)),
                                                            (origin[0]+(width-i)-1,origin[1]+i+1) ),
                                                            width=1,fill=shadowcolor,tags='SHADOW')

    def DrawBevelX(self,origin=(0,0),height=0,width=0,thickness=4):
        
        color=self.colors.lineBody
        highlightcolor=self.colors.lineHighlight,
        shadowcolor=self.colors.lineShadow
                
        #filled cross with shadowcolor outline
        centre = ( origin[0]+width/2 , origin[1]+height/2 )
        iCO = thickness/2+2 #insideCornerOffset
        self.create_polygon(( ( origin[0]+thickness , origin[1] ),
                                                        ( centre[0] , centre[1]-iCO ),
                                                        ( origin[0]+width-thickness , origin[1] ),
                                                        ( origin[0]+width , origin[1]+thickness ),
                                                        ( centre[0]+iCO , centre[1] ),
                                                        ( origin[0]+width , origin[1]+height-thickness ),
                                                        ( origin[0]+width-thickness , origin[1]+height ),
                                                        ( centre[0] , centre[1]+iCO ),
                                                        ( origin[0]+thickness , origin[1]+height ),
                                                        ( origin[0] , origin[1]+height-thickness ),
                                                        ( centre[0]-iCO , centre[1] ),
                                                        ( origin[0] , origin[1]+thickness ) ),
                                                        outline=shadowcolor,width=1,fill=color,tags='BODY')     
        #pad the shadow to bevel width
        self.create_line( ( ( origin[0] +2, origin[1]+thickness +1),
                                                    ( centre[0]-iCO +1, centre[1] ) ),
                                                    width=1,fill=shadowcolor,tags='SHADOW')
        self.create_line( ( ( centre[0]+iCO , centre[1] -1),
                                                    ( origin[0]+width -1, origin[1]+thickness) ),
                                                    width=1,fill=shadowcolor,tags='SHADOW')
        self.create_line( ( ( origin[0] +2, origin[1]+height-thickness +1),
                                                    ( origin[0]+thickness , origin[1]+height -1),
                                                    ( centre[0] , centre[1]+iCO -1),
                                                    ( origin[0]+width-thickness , origin[1]+height -1),
                                                    ( origin[0]+width -1, origin[1]+height-thickness) ),
                                                    width=1,fill=shadowcolor,tags='SHADOW')
        #add the highlight
        self.create_line( ( ( origin[0] , origin[1]+height-thickness ),
                                                    ( centre[0]-iCO +1  , centre[1] -1 ) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')
        self.create_line( ( ( origin[0] +1, origin[1]+height-thickness ),
                                                    ( centre[0]-iCO +1  +1, centre[1] -1 ) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')
        self.create_line( ( ( centre[0]+iCO , centre[1] ),
                                                    ( origin[0]+width +1 , origin[1]+height-thickness +1 ) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')
        self.create_line( ( ( centre[0]+iCO -1, centre[1] ),
                                                    ( origin[0]+width, origin[1]+height-thickness +1) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')
        self.create_line( ( ( origin[0] , origin[1]+thickness ),
                                                    ( origin[0]+thickness , origin[1] ),
                                                    ( centre[0] , centre[1]-iCO ),
                                                    ( origin[0]+width-thickness , origin[1] ),
                                                    ( origin[0]+width +1 , origin[1]+thickness +1 ) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')
        self.create_line( ( ( origin[0] +1 , origin[1]+thickness ),
                                                    ( origin[0]+thickness , origin[1] +1),
                                                    ( centre[0] , centre[1]-iCO +1),
                                                    ( origin[0]+width-thickness , origin[1] +1),
                                                    ( origin[0]+width , origin[1]+thickness +1 ) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')

    def DrawBevelO(self,origin=(0,0),height=0,width=0,thickness=4):
        color=self.colors.lineBody
        highlightcolor=self.colors.lineHighlight,
        shadowcolor=self.colors.lineShadow
                
        #draw filled O with shadowcolor border
        self.create_oval( ( ( origin[0] , origin[1] ), 
                                                    ( origin[0]+width , origin[1]+height ) ), 
                                                    outline=shadowcolor,width=1,fill=shadowcolor)
        self.create_oval( ( ( origin[0]+1 , origin[1]+1 ), 
                                                    ( origin[0]+width-1 , origin[1]+height-1 ) ), 
                                                    outline=shadowcolor,width=1,fill=color,tags='BODY')#,fill=color
        #draw central O with shadowcolor border
        self.create_oval( ( ( origin[0]+thickness+1 , origin[1]+thickness+1 ), 
                                                    ( origin[0]+width-thickness-1 , origin[1]+height-thickness-1) ), 
                                                    outline=shadowcolor,width=1,fill=shadowcolor)
        self.create_oval( ( ( origin[0]+thickness+2 , origin[1]+thickness+2 ), 
                                                    ( origin[0]+width-thickness-2 , origin[1]+height-thickness-2) ), 
                                                    outline=shadowcolor,width=1,fill=self.cget('bg'),tags='SHADOW')#,fill='DarkGray'
        #add highlights
        #top
        self.create_arc(  ( ( origin[0] , origin[1] ), 
                                                    ( origin[0]+width , origin[1]+height ) ),
                                                    start=40,extent=180,
                                                    style='arc',width=1,outline=highlightcolor,tags='HIGHLIGHT')#'red' 
        self.create_arc(  ( ( origin[0]+1 , origin[1]+1 ), 
                                                    ( origin[0]+width-1 , origin[1]+height-1 ) ),
                                                    start=35,extent=180,
                                                    style='arc',width=1,outline=highlightcolor,tags='HIGHLIGHT')#'black' highlightcolor

        #lower inside
        self.create_arc(  ( ( origin[0]+thickness+1 , origin[1]+thickness+1 ), 
                                                    ( origin[0]+width-thickness-1 , origin[1]+height-thickness-1) ),
                                                    start=220,extent=180,
                                                    style='arc',width=1,outline=highlightcolor,tags='HIGHLIGHT')#'red'
        self.create_arc(  ( ( origin[0]+thickness+2 , origin[1]+thickness+2 ), 
                                                    ( origin[0]+width-thickness-2 , origin[1]+height-thickness-2) ),
                                                    start=215,extent=180,
                                                    style='arc',width=1,outline=highlightcolor,tags='HIGHLIGHT')#'black'
        #patch the highlight drawing to compensate for 
        #differences(!) in behaviour of tk canvas on win32
        if pyching.osType == 'nt':
            self.create_line( ( (origin[0]+1 , origin[1]+13),
                                                        (origin[0]+1 , origin[1]+6), 
                                                        (origin[0]+6 , origin[1]+1),
                                                        (origin[0]+8 , origin[1]+1),
                                                        (origin[0]+14 , origin[1]+1),
                                                        (origin[0]+16 , origin[1]+3) ),
                                                        width=1,fill=highlightcolor,tags='HIGHLIGHT')
            self.create_line( ( (origin[0]+7 , origin[1]+13),
                                                        (origin[0]+8 , origin[1]+14), 
                                                        (origin[0]+12 , origin[1]+14),
                                                        (origin[0]+15 , origin[1]+11) ),
                                                        width=1,fill=highlightcolor,tags='HIGHLIGHT')

class DialogSetColors(smgDialog):
    """
    display a colour configuration dialog
    """
    def __init__(self,parent,currentColors=None):
        if currentColors: self.colors=currentColors
        else: self.colors=WidgetColors()
        self.fonts=WidgetFonts()
        smgDialog.__init__(self,parent,title='Configure Colors',
                    buttons=[{'name':'buttonOk','title':'Ok','binding':'Ok','underline':None,'hotKey':'<Return>'},
                                {'name':'buttonCancel','title':'Cancel','binding':'Cancel','underline':None,'hotKey':'<Escape>'}],
                    buttonsDef=-1, buttonsWidth=0,buttonsPad=5, 
                    resizeable=0, transient=1, wait=1)#buttonsPos='BOTTOM',

    def Body(self,master):
        master.configure(borderwidth=2,relief=SUNKEN,highlightthickness=4)
        
        self.frameDemo = Frame(master,bg=self.colors.bgReading,borderwidth=2,relief=FLAT)
        self.frameDemo.grid(row=1,column=0,padx=0,pady=10)
        self.frameDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.labelTitleDemo = Label(self.frameDemo,text='Hexagram Title',
                        font=self.fonts.labelHexTitles,borderwidth=0,
                        fg=self.colors.fgLabelHexTitles,bg=self.colors.bgReading)
        self.labelTitleDemo.grid(row=0,column=0,pady=5)
        self.labelTitleDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)
        
        self.lineDemos = []
        for i in range(4):
            self.lineDemos.append(HexLine(self.frameDemo,currentColors=self.colors))
            #self.lineDemos[i].colors = self.colors
            self.lineDemos[i].Draw(linetype=i +6)  
            self.lineDemos[i].grid(row=i+1,column=0,padx=10)  
            self.lineDemos[i].bind('<ButtonPress-1>',self.SetColorExampleDetails)
            #self.tag_bind('BODY','<ButtonPress-1>',self.SetColorExampleDetails)
            #self.tag_bind('HIGHLIGHT','<ButtonPress-1>',self.SetColorExampleDetails)
            #self.tag_bind('SHADOW','<ButtonPress-1>',self.SetColorExampleDetails)
        
        self.labelQuestionDemo = Label(self.frameDemo,text='Reading Question',
                        font=self.fonts.label,borderwidth=0,
                        fg=self.colors.fgMessageQuestion,bg=self.colors.bgReading)
        self.labelQuestionDemo.grid(row=5,column=0,pady=5)
        self.labelQuestionDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.labelPlaceDemo = Label(self.frameDemo,text='place name',
                        font=self.fonts.label,borderwidth=0,
                        fg=self.colors.fgLabelPlaces,bg=self.colors.bgReading)
        self.labelPlaceDemo.grid(row=1,column=1,padx=5)
        self.labelPlaceDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.labelBecomesDemo = Label(self.frameDemo,text='becomes',
                        font=self.fonts.label,borderwidth=0,
                        fg=self.colors.fgLabelLines,bg=self.colors.bgReading)
        self.labelBecomesDemo.grid(row=2,column=1,padx=5)
        self.labelBecomesDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.labelNoMovingDemo = Label(self.frameDemo,text='no moving lines',
                        font=self.fonts.label,borderwidth=0,
                        fg=self.colors.fgLabelLines,bg=self.colors.bgReading)
        self.labelNoMovingDemo.grid(row=3,column=1,padx=5)
        self.labelNoMovingDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.frameHintBgDemo = Label(self.frameDemo,text='line hint',
                        font=self.fonts.labelLineHint,relief=SOLID,borderwidth=1,
                        bg=self.colors.bgLabelHint)
        self.frameHintBgDemo.grid(row=4,column=1,sticky=(N,S,E,W),padx=5)#padx=5
        self.frameHintBgDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.labelHintDemo = Label(self.frameHintBgDemo,text='line hint',
                        font=self.fonts.labelLineHint,borderwidth=0,
                        fg=self.colors.fgLabelHint,bg=self.colors.bgLabelHint)
        self.labelHintDemo.grid(row=0,column=0)
        self.labelHintDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)
        
        self.SetColorButtonDetails()

        self.colorExampleDetails = { 'name': self.colorButtonDetails[0][0],
                                                    'color': self.colorButtonDetails[0][1] }

        self.frameColorSelect = Frame(master,bg=self.colorExampleDetails['color'],
                        relief=SOLID,borderwidth=1)
        self.frameColorSelect.grid(row=0,column=0,padx=10,pady=10,ipadx=10,ipady=10)
        
        self.buttonGetColor =  Button(self.frameColorSelect,text='Set Color of:',
                        underline=0,highlightthickness=0,font=self.fonts.button,
                        takefocus=FALSE,command=self.GetColor)
        self.buttonGetColor.grid(row=0,column=0,padx=2)

        self.menubuttonOptions = Menubutton(self.frameColorSelect,width=32,
                        text=self.colorButtonDetails[0][0],font=self.fonts.menu,indicatoron=TRUE,
                        underline=string.find(self.colorButtonDetails[0][0],'e'),
                        relief=RAISED,highlightthickness=0)
        self.menubuttonOptions.grid(row=0,column=1,padx=2,sticky=(N,S))#sticky=(N,S) makes the menubutton the smae height as buttonGetCOlor
        self.menuOptions = Menu(self.menubuttonOptions,tearoff=0,font=self.fonts.menu)
        self.menubuttonOptions.configure(menu=self.menuOptions)
        for item in self.colorButtonDetails: #build the menu
            self.menuOptions.add_command(label=item[0],command=self.SetColorExample)
        #self.menuOptions.bind('<<MenuSelect>>',self.SetColorExampleDetails)

        self.buttonDefaults = Button(master,
                        text='Reset All Colors To '+pyching.title+' Defaults',
                        underline=0,highlightthickness=0,font=self.fonts.button,
                        takefocus=FALSE,command=self.SetDefaultColors)
        self.buttonDefaults.grid(row=2,column=0,padx=10,pady=10,sticky=(W,E))

        #return self.menubuttonOptions #control for initial focus

        #hot key bindings for this dialog
        self.bind('<Alt-s>',self.SetColorButtonBinding) #set color button
        self.bind('<Alt-e>',self.ScreenElementButtonBinding) #screen element selection button
        self.bind('<Alt-r>',self.ResetColorsButtonBinding) #reset default colors button

    def SetColorButtonBinding(self,event):
        self.buttonGetColor.invoke()

    def ScreenElementButtonBinding(self,event):
        #self.menubuttonOptions.invoke()
        #print self.menubuttonOptions.winfo_rootx(),self.menubuttonOptions.winfo_rooty(),\
        #   self.menubuttonOptions.winfo_height() #debug
        self.menuOptions.post(self.menubuttonOptions.winfo_rootx(),
                self.menubuttonOptions.winfo_rooty()+self.menubuttonOptions.winfo_height())
        #self.menuOptions.tk_mbPost()

    def ResetColorsButtonBinding(self,event):
        self.buttonDefaults.invoke()

    def SetColorButtonDetails(self):
        self.colorButtonDetails=( 
                ('Reading Background',self.colors.bgReading),
                ('Hexagram Titles',self.colors.fgLabelHexTitles),
                ('Reading Question',self.colors.fgMessageQuestion),
                ('Place Names',self.colors.fgLabelPlaces),
                ("'becomes' & 'no moving lines'",self.colors.fgLabelLines),
                ('Line Hint Background',self.colors.bgLabelHint),
                ('Line Hint Text',self.colors.fgLabelHint),
                ('Hexagram Line Body',self.colors.lineBody),
                ('Hexagram Line Highlight',self.colors.lineHighlight),
                ('Hexagram Line Shadow',self.colors.lineShadow) )

    def SetColorExampleDetails(self,event):
        if event.widget == self.frameDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[0][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[0][1]
        elif event.widget == self.labelTitleDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[1][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[1][1]
        elif event.widget == self.labelQuestionDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[2][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[2][1]
        elif event.widget == self.labelPlaceDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[3][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[3][1]
        elif event.widget == self.labelBecomesDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[4][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[4][1]
        elif event.widget == self.labelNoMovingDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[4][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[4][1]
        elif event.widget == self.frameHintBgDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[5][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[5][1]
        elif event.widget == self.labelHintDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[6][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[6][1]
        elif event.widget in self.lineDemos:
            tags = string.split(event.widget.itemcget('current','tags'))
            #print tags
            if 'SHADOW' in tags:
                self.colorExampleDetails['name']=self.colorButtonDetails[9][0]
                self.colorExampleDetails['color']=self.colorButtonDetails[9][1]
            elif 'HIGHLIGHT' in tags:
                self.colorExampleDetails['name']=self.colorButtonDetails[8][0]
                self.colorExampleDetails['color']=self.colorButtonDetails[8][1]
            elif 'BODY' in tags:
                self.colorExampleDetails['name']=self.colorButtonDetails[7][0]
                self.colorExampleDetails['color']=self.colorButtonDetails[7][1]
            else: #background clicked
                self.colorExampleDetails['name']=self.colorButtonDetails[0][0]
                self.colorExampleDetails['color']=self.colorButtonDetails[0][1]

        self.SetColorExample()
    
    def SetColorExample(self):
        #print 'active menuitem is:',self.menuOptions.index('active') #debug
        if self.menuOptions.index('active') != None: #if this routine was called by self.menuOptions
            self.colorExampleDetails['name']=self.colorButtonDetails[self.menuOptions.index('active')][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[self.menuOptions.index('active')][1]
        
        self.menubuttonOptions.configure(text=self.colorExampleDetails['name'],
                underline=string.find(self.colorExampleDetails['name'],'e'))
        self.frameColorSelect.configure(bg=self.colorExampleDetails['color'])
        
    def GetColor(self):
        rgbTuplet, colorString = tkColorChooser.askcolor(parent=self,
                        title='Pick a new colour for: '+self.colorExampleDetails['name'],
                        initialcolor=self.colorExampleDetails['color'])#._root()
        if colorString: #user didn't cancel
            self.frameDemo.update() #redraw after dialog
            #print 'GetColor colorString =',colorString
            self.colorExampleDetails['color']=colorString
            self.frameColorSelect.configure(bg=colorString)
            self.UpdateColors()
            self.RepaintColors()
            #self.frameDemo.update() #redraw new colors
    
    def UpdateColors(self):
        if self.colorExampleDetails['name'] == self.colorButtonDetails[0][0]: 
            self.colors.bgReading = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[1][0]: 
            self.colors.fgLabelHexTitles = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[2][0]: 
            self.colors.fgMessageQuestion = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[3][0]: 
            self.colors.fgLabelPlaces = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[4][0]: 
            self.colors.fgLabelLines = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[5][0]: 
            self.colors.bgLabelHint = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[6][0]: 
            self.colors.fgLabelHint = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[7][0]: 
            self.colors.lineBody = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[8][0]: 
            self.colors.lineHighlight = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[9][0]: 
            self.colors.lineShadow = self.colorExampleDetails['color']
    
    def RepaintColors(self):
        #print 'ConfigureWidgetCustomColors frameDemo bg was =',self.frameDemo.cget('bg') 
        self.frameDemo.configure(bg=self.colors.bgReading)
        #print 'ConfigureWidgetCustomColors frameDemo bg is =',self.frameDemo.cget('bg') 
        self.labelTitleDemo.configure(fg=self.colors.fgLabelHexTitles,bg=self.colors.bgReading)
        self.labelQuestionDemo.configure(fg=self.colors.fgMessageQuestion,bg=self.colors.bgReading)
        self.labelPlaceDemo.configure(fg=self.colors.fgLabelPlaces,bg=self.colors.bgReading)
        self.labelBecomesDemo.configure(fg=self.colors.fgLabelLines,bg=self.colors.bgReading)
        self.labelNoMovingDemo.configure(fg=self.colors.fgLabelLines,bg=self.colors.bgReading)
        self.frameHintBgDemo.configure(bg=self.colors.bgLabelHint)
        self.labelHintDemo.configure(fg=self.colors.fgLabelHint,bg=self.colors.bgLabelHint)
        self.frameDemo.update()
        for item in self.lineDemos: 
            #item.configure(bg=self.colors.bgReading)
            item.colors = self.colors
            item.Draw(linetype=item.value)  

        self.SetColorButtonDetails()

    def SetDefaultColors(self):
        self.colors=WidgetColors()
        self.RepaintColors()
        self.colorExampleDetails['name']=self.colorButtonDetails[0][0]
        self.colorExampleDetails['color']=self.colorButtonDetails[0][1]
        self.SetColorExample()

    def Apply(self):
        self.result = self.colors

class DialogGetQuestion(smgDialog):
    """
    gets the question for a reading
    """ 
    def __init__(self,parent):
        smgDialog.__init__(self,parent,title='Enter Question',
                    buttons=[{'name':'buttonOk','title':'Ok','binding':'Ok','underline':None,'hotKey':'<Return>'},
                                {'name':'buttonCancel','title':'Cancel','binding':'Cancel','underline':None,'hotKey':'<Escape>'}],
                    buttonsDef=-1,buttonsWidth=0,buttonsPad=5, 
                    resizeable=0, transient=1, wait=1) # buttonsPos='BOTTOM',

    def Body(self,master):
        labelPrompt = Label(master,text='Enter a question to ask the I Ching (maximum 70 characters):',
                        ).grid(column=0,row=0,sticky=W,padx=5,pady=5)
        self.questionText = StringVar()
        self.questionText.set('Tell me about my current circumstances.')
        self.entryQuestion = Entry(master,textvariable=self.questionText,width=70)
        self.entryQuestion.grid(column=0,row=1,sticky=W,padx=5)
        return self.entryQuestion
    
    def Apply(self):
        self.result = self.questionText.get()
         
    def Validate(self):
        if len(self.questionText.get()) > 70:#question too long
            tkMessageBox.showerror(title='Question Too Long',
                                                message='The question you have entered is longer than 70 characters.')
            return 0
        elif len(string.strip(self.questionText.get())) == 0:#null question
            tkMessageBox.showerror(title='No Question Entered',
                                                message='You have entered a blank question.')
            return 0
        else:
            return 1
        
#create an instance of the app details for use throughout this module
pyching = pyching_engine.PychingAppDetails()

windowRoot = Tk()
windowMain = WindowMain(windowRoot)
windowRoot.mainloop()
