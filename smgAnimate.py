##---------------------------------------------------------------------------##
##
## Python/Tkinter base module/class for an animated canvas
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
tkinter generic canvas based animation
"""

from sys import version
from time import sleep
from string import split
from Tkinter import Canvas
from Tkinter import Label

class smgAnimate(Canvas):
    """
    tkinter generic canvas based animation, base class
    """ 
    def __init__(self,parent,width=0,height=0,frames=None,framesCentre=None,
                framePersist=0,plays=1,bg=None,triggerFunc=None,triggerPlays=0):
        """
        width, height - canvas dimensions, if 0 default to width and/or height of 
                                        frame[0]
        frames - list of animation frame images
        framesCentre - tuple of coordinates of centre of frame images,
                                     defaults to centre of canvas if not specified
        framePersist -  the frame to be displayed when the animation is not running,
                                        if -1 the canvas is blank when not playing
        plays - number of cycles of the animation that is displayed
        bg - background colour of the canvas
        triggerFunc - function that is called every triggerPlays plays
        triggerPlays -  how many plays for each call of triggerFunc
        """
        if not width: width = frames[0].width()
        if not height: height = frames[0].height() 
        if not framesCentre:
            framesCentre = (width/2 , height/2)
        Canvas.__init__(self,parent,width=width,height=height,bg=bg,
                    takefocus='false',highlightthickness=0)
        self.parent=parent
        self.frames=frames
        self.framesCentre=framesCentre
        self.framePersist=framePersist
        self.plays=plays
        self.bg=bg 
        self.triggerFunc=triggerFunc
        self.triggerPlays=triggerPlays 
        self.pyVer = split(version)[0]  
        if frames: self.LoadFrames(frames)
    
    def LoadFrames(self,frames):
        """
        load a set of frame images
        """
        self.frameIDs=[]
        if self.pyVer >= '1.6': #'state' available
            for frame in frames:
                self.frameIDs.append(self.create_image(self.framesCentre[0],
                            self.framesCentre[1],image=frame,state='hidden'))
            if self.framePersist > -1:
                self.itemconfigure(self.frameIDs[self.framePersist],state='normal')
        else: #'state' unavailable
            for frame in frames:
                self.frameIDs.append(self.create_image(self.framesCentre[0],
                            self.framesCentre[1],image=frame))
            self.blankID = self.create_rectangle(0,0,self.cget('width'),self.cget('height'),
                        fill=self.bg,outline=self.bg)
            if self.framePersist > -1:
                self.tkraise(self.frameIDs[self.framePersist])
    
    def SetBg(self,bg):
        """
        set the background colour to a new value
        """
        self.configure(bg=bg)
        self.itemconfigure(self.blankID,outline=bg,fill=bg)
        self.update()
    
    def Play(self,delay=0.02):
        """
        play the animation
        """
        maxFrameID = len(self.frameIDs)-1
        func = (self.triggerFunc and self.triggerPlays) 
        if self.pyVer >= '1.6': #animate by manipulating 'state'
            for plays in range(0,self.plays):
                for frameID in self.frameIDs:
                    self.itemconfigure(frameID,state='normal')
                    self.master.update_idletasks()
                    if frameID ==  self.frameIDs[0]:
                        self.itemconfigure(self.frameIDs[maxFrameID],state='hidden')
                    else:
                        self.itemconfigure(frameID - 1,state='hidden')
                    self.parent.update_idletasks()
                    sleep(delay)
                    self.parent.update_idletasks()
                if func and not (plays % self.triggerPlays): self.triggerFunc()

            if self.framePersist > -1:
                self.itemconfigure(self.frameIDs[self.framePersist],state='normal')
            self.itemconfigure(self.frameIDs[maxFrameID],state='hidden')
            self.parent.update_idletasks()
        else: #'state' unavailable, animate by manipulating stacking order
            for plays in range(0,self.plays):
                for frameID in self.frameIDs:
                    self.tkraise(frameID)
                    #self.master.update_idletasks()
                    if frameID ==  self.frameIDs[0]:
                        self.lower(self.frameIDs[maxFrameID])
                    else:
                        self.lower(frameID - 1)
                    self.parent.update_idletasks()
                    sleep(delay)
                    self.parent.update_idletasks()
                if func and not (plays % self.triggerPlays): self.triggerFunc()

            if self.framePersist > -1:
                self.tkraise(self.frameIDs[self.framePersist])
            self.lower(self.frameIDs[maxFrameID])
            self.parent.update_idletasks()
        
