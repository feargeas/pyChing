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
tkinter generic dialog base module
"""

from tkinter import *
from typing import Any, Optional

class smgDialog(Toplevel):
    """
    tkinter generic dialog, base class
    """
    def __init__(self, parent: Any, title: Optional[str] = None,
                buttons: list[dict[str, Any]] = [{'name':'buttonOk','title':'Ok',
                'binding':'Ok','underline':None,'hotKey':'<Return>'}],
                buttonsDef: int = -1, buttonsWidth: int = 0, buttonsPad: int = 5,
                resizeable: int = 0, transient: int = 1, wait: int = 1) -> None:  # buttonsPos='BOTTOM',
        """
        buttons - a list of button dictionaries, in placement order
                            keys -  'name'      button name, required
                                            'title'     button title, required
                                            'binding'   button binding, or None
                                            'underline' title character to underline, or None
                                            'hotKey'    tkinter key identifier, or None
        buttonsDef - position in buttons of default button, or -1 for no default
        buttonsWidth - width for all buttons, or 0 for all buttons equal to widest
        buttonsPad - pading between buttons, default = 5
        resizable, transient, wait - booleans
        """
        #buttonsPos - position of button box, 'BOTTOM', 'TOP', 'LEFT' or 'RIGHT'

        Toplevel.__init__(self, parent)
        self.withdraw()#hide the window until it is fully built
        #place the window
        self.geometry("+%d+%d" % (parent.winfo_rootx()+10,
                                                            parent.winfo_rooty()+10))
        #transient window or not
        if transient: self.transient(parent)
        if resizeable:
            self.resizable(height=True, width=True)
        else:
            self.resizable(height=False, width=False)
        if title:
            self.title(title)
        self.parent = parent
        
        self.result = None

        self.frameMain = Frame(self)

        #buttons should be created before body in case they are referred to in 
        #self.Body of a derived class
        self.buildButtonBox(buttons, buttonsDef,buttonsWidth, buttonsPad)# buttonsPos, 
        
        self.initial_focus = self.Body(self.frameMain)
        




        #self.frameMain.pack(expand=True,fill='both')

        self.frameMain.grid(row=0, column=0, sticky='nsew')
        
        
        self.grid_location(0,0)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        
        
        
        #do this after body is packed because it looks better on windoze
        self.showButtonBox() #buttonsPos
        
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.Cancel)
        self.initial_focus.focus_set()
        self.update()
        self.deiconify() #unhide the window becuase it's built now
        #wait for window to close (modal) or not (non modal)
        if wait: self.wait_window(self)

    def buildButtonBox(self, buttons, bDef, bWidth, bPad): # bPos, 
    # add button box
        self.frameButtonBox = Frame(self)
        bGreatestWidth = 0
        bRow = 0
        bCol = 0
        Num = 0
            
        for button in buttons:
            #create button
            exec ('self.'+ button['name'] + ' = Button(self.frameButtonBox, text="' +
                        button['title'] + '",command=self.' + button['binding'] + ')' )
            #place button
            exec ('self.'+ button['name'] + '.grid(row=' + str(bRow) +
                        ', column=' + str(bCol) + ', padx=' + str(bPad) + ', pady=' + str(bPad) + ')' )
            #configure optional button hot key
            if button['hotKey']:
                exec ('self.bind("' + button['hotKey'] + '", self.' + button['binding'] + ')' )
                if button['underline']:
                    exec ('self.'+ button['name'] +
                            '.configure(underline=' + str(button['underline']) + ')' )
            #get largest button width so far
            wdth = len(button['title']) + 2 
            if wdth > bGreatestWidth: bGreatestWidth = wdth
            
            # increment row/col
            #if bPos in ('bottom','top'): #horizontal buttons
            #    bCol = bCol + 1
            #else: #vertical buttons
            #    bRow = bRow +1
            bCol = bCol + 1
    
        #set button widths
        if bWidth < bGreatestWidth: bWidth = bGreatestWidth
        for button in buttons:
            exec ('self.'+ button['name'] +
                        '.configure(width=' + str(bWidth) + ')' )

    def showButtonBox(self): #, bPos
        #show the button box
        #eval('self.frameButtonBox.pack(side=' + bPos + ')' )
        
        
        self.frameButtonBox.grid(row=1, column=0, sticky='nsew')
    
    
    
    #
    # override this routine in derived classes to define the dialog body
    #
    def Body(self, master):
    # create dialog body and return widget that should have
    # initial focus.  this method should be overridden
        #return initial_focus_widget
        pass # override

    #
    # override these routines in derived classes for Ok button handling
    #
    def Validate(self):
        return 1 # override

    def Apply(self):
        pass # override
    
    #
    # standard button bindings for Ok and Cancel
    #
    def Ok(self, event=None):
        #standard Ok binding
        #validate and conditionally close dialog
        if not self.Validate(): #if Ok fails validation
            self.initial_focus.focus_set() # put focus back
        else: #proceed with Ok
            self.Apply()
            self.Cancel()

    def Cancel(self, event=None):
        #standard Cancel binding
        #close and destroy the dialog
        self.update_idletasks()
        self.withdraw()
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
