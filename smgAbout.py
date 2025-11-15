##---------------------------------------------------------------------------##
##
## Python/Tkinter base module/class for a generic dialog 
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
## http://pyching.sourgeforge.net/elguavas-soft.html
##
##---------------------------------------------------------------------------##
"""
tkinter about dialog base module
"""

#python library imports
import sys
from typing import Any, Optional

#tkinter imports
from tkinter import *

#smg library module imports
from smgDialog import smgDialog
from smgHtmlView import smgHtmlView

class smgAbout(smgDialog):
    """
    display an 'about' box
    """
    def __init__(self, parent: Any, title: str = '', appTitle: str = '', version: str = '',
                copyright: str = '', licence: str = '', email: str = '', www: str = '',
                pictureData: str = '', licenceFile: str = '', creditsFile: str = '',
                showToolVersions: int = 1,
                fontAppTitle: Optional[str] = None, fontText: Optional[str] = None,
                fg: Optional[str] = None, bg: Optional[str] = None) -> None:
        self.appTitle=appTitle
        self.version=version
        self.copyright=copyright
        self.licence=licence
        self.email=email
        self.www=www
        self.pictureData=pictureData
        self.licenceFile=licenceFile
        self.creditsFile=creditsFile
        self.showToolVersions = showToolVersions
        self.fontAppTitle=fontAppTitle 
        self.fontText=fontText
        self.fg=fg
        self.bg=bg
        smgDialog.__init__(self, parent, title='About '+ appTitle,
                    buttons=[{'name':'buttonOk','title':'Ok','binding':'Ok','underline':None,'hotKey':'<Return>'}],
                    buttonsDef=-1, buttonsWidth=0, buttonsPad=5,
                    resizeable=0, transient=1, wait=1) # buttonsPos='bottom'
        
    def ShowLicense(self):
        smgHtmlView(self,title='About - License',
                    htmlSource=self.licenceFile,plainText=1,sourceIsStr=0)

    def ShowCredits(self):
        smgHtmlView(self,title='About - Credits',
                    htmlSource=self.creditsFile,plainText=1,sourceIsStr=0)

    def Body(self, master):
        self.picture = Image('photo', data=self.pictureData)
        master.configure(borderwidth=2, relief='sunken', highlightthickness=4)
        frameBg = Frame(master, bg=self.bg)
        frameBg.pack(expand=True, fill='both')
        labelTitle = Label(frameBg, text=self.appTitle, font=self.fontAppTitle, fg=self.fg, bg=self.bg)
        labelTitle.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        labelPicture = Label(frameBg, image=self.picture, bg=self.bg)
        labelPicture.grid(row=0, column=1, sticky='w', rowspan=2, padx=0, pady=3)
        labelVersion = Label(frameBg, text=self.version, font=self.fontText, fg=self.fg, bg=self.bg)
        labelVersion.grid(row=1, column=0, sticky='w', padx=10, pady=5)
        labelCopyright = Label(frameBg, text=self.copyright, font=self.fontText, fg=self.fg, bg=self.bg)
        labelCopyright.grid(row=2, column=0, sticky='w', columnspan=3, padx=10, pady=5)
        labelLicense = Label(frameBg, text=self.licence, font=self.fontText, fg=self.fg, bg=self.bg)
        labelLicense.grid(row=3, column=0, sticky='w', columnspan=3, padx=10, pady=5)
        framePad = Frame(frameBg, bg=self.bg, height=5).grid(row=4, column=0)
        labelEmail = Label(frameBg, text=self.email, font=self.fontText, fg=self.fg, bg=self.bg)
        labelEmail.grid(row=5, column=0, columnspan=2, sticky='w', padx=10, pady=0)
        labelWWW = Label(frameBg, text=self.www, font=self.fontText, fg=self.fg, bg=self.bg)
        labelWWW.grid(row=6, column=0, columnspan=2, sticky='w', padx=10, pady=0)
        frameDivider = Frame(frameBg, borderwidth=1, relief='sunken', bg=self.bg,
                        height=2).grid(row=7, column=0, sticky='ew', columnspan=3, padx=5, pady=5)
        if self.showToolVersions:
            labelPythonVer = Label(frameBg, text='Python version: '+sys.version.split()[0],
                            font=self.fontText, fg=self.fg, bg=self.bg)
            labelPythonVer.grid(row=8, column=0, sticky='w', padx=10, pady=0)
            #handle wierd tk version num in windoze python >= 1.6 (?!?)
            tkVer = str(TkVersion).split('.')
            tkVer[len(tkVer)-1] = str('%.3g' % (float('.'+tkVer[len(tkVer)-1])))[2:]
            if tkVer[len(tkVer)-1] == '':
                tkVer[len(tkVer)-1] = '0'
            tkVer = '.'.join(tkVer)
            labelTkVer = Label(frameBg, text='Tk version: '+tkVer,
                            font=self.fontText, fg=self.fg, bg=self.bg)
            labelTkVer.grid(row=8, column=1, sticky='w', padx=2, pady=0)
            #labelOs = Label(frameBg,text='python os name: '+pyching.os,
            #       font=self.fontText,fg=self.fg,bg=self.bg)
            #labelOs.grid(row=6,column=0,sticky='w',padx=10,pady=0)
            #labelOsType = Label(frameBg,text='python os type: '+pyching.osType,
            #       font=self.fontText,fg=self.fg,bg=self.bg)
            #labelOsType.grid(row=6,column=1,sticky='w',padx=5,pady=0)
            #framePad = Frame(frameBg,bg=self.bg,height=5).grid(row=7,column=0)

        self.buttonLicense = Button(frameBg, text='View License', underline=5,
                        width=14, font=self.fontText, highlightthickness=0,
                        takefocus=False, command=self.ShowLicense)
        self.buttonLicense.grid(row=9, column=0, sticky='w', padx=10, pady=10)
        self.buttonCredits = Button(frameBg, text='View Credits', underline=5,
                        width=14, font=self.fontText, highlightthickness=0,
                        takefocus=False, command=self.ShowCredits)
        self.buttonCredits.grid(row=9, column=1, columnspan=2, sticky='e', padx=10, pady=10)

        #hot key bindings for this dialog
        self.bind('<Alt-c>',self.CreditsButtonBinding) #credits button
        self.bind('<Alt-l>',self.LicenseButtonBinding) #license button

    def CreditsButtonBinding(self,event):
        self.buttonCredits.invoke()

    def LicenseButtonBinding(self,event):
        self.buttonLicense.invoke()
