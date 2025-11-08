##---------------------------------------------------------------------------##
##
## Python/Tkinter base module/classes for a html viewer dialog 
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
tkinter html viewer dialog module
"""

#python library imports
import os, htmllib, formatter

#tkinter imports
from tkinter import *
import tkinter.messagebox as tkMessageBox
import tkinter.simpledialog as tkSimpleDialog

#smg library module imports
from smgDialog import smgDialog

class smgHtmlView(smgDialog):
    """
    display a html file (or a plain text file if plainText=1), or html data 
    from a string (which may be a repr of a function name). optionally show 
    an 'index' button, which jumps straight to indexFile (which can also be a 
    disk file or a string as above) if specified. only a small subset of html 
    tags are rendered. ony links to files, specified without any urltype, or 
    internal html and image data returned by functions are supported.
    """
    def __init__(self,parent,title=None,htmlSource=None,sourceIsStr=1,
                internalLink=None,index=None,plainText=0,modal=1,hexBrowser=0,
                imageModule=None,bg='#e8e8e8',fg='#000000'):
        """
        title - string, dialog title
        htmlSource - either a filename or a string containing html data
        sourceIsStr - bool - true if htmlSource is an html string, or a string
                      repr of a function name that will return an html string,
                      false if htmSource is a filename
        internalLink - an url to jump to within the source (not yet implemented)
        index - either a filename or a function that returns html data for the index
        plainText - boolean, true if source is plain text rather than html
        modal - boolean, true if viewer dialog should be modal
        imageModule - string, name of internal image data module
        bg, fg - background and foreground colours of html display area
        """
        self.colorViewerFg = fg
        self.colorViewerBg = bg
        self.index = index
        self.plainText = plainText
        self.hexNum=0
        if hexBrowser:
            htmlSource=self.MakeBrowseSource(1) #start browser at hexagram 1
        self.htmlSource = htmlSource
        self.hexBrowser=hexBrowser
        self.sourceIsStr=sourceIsStr
        self.internalLink = internalLink
        self.internalImageExt = '.#@~' #hack to indicate internal image data
        
        #if imageModule: #import image data module, if any
        #  eval('import ' + imageModule)
        
        #if self.htmlFile: #open disk file 
        #  self.displayFile = self.openDataFile(htmlFile)
        #else: #import html data module
        #  import self.displayFile
        #  #if any image data import it
        #  if self.imageData: import self.imageData 
        
        #configure buttons
        if not hexBrowser: #regular buttons
            btns=[{'name':'buttonOk','title':'Ok','binding':'Ok',
                        'underline':None,
                        'hotKey':'<Return>'}]
            if self.index: #we want an index button
                btns.append({'name':'buttonIndex','title':'Index',
                            'binding':'Index','underline':0,
                            'hotKey':'<Alt-i>'})
        else: #special hexagram info browser buttons
            btns=[  {'name':'buttonPrev','title':'< Prev',
                            'binding':'Prev','underline':2,
                            'hotKey':'<Alt-p>'},
                    {'name':'buttonNext','title':'Next >',
                            'binding':'Next','underline':0,
                            'hotKey':'<Alt-n>'},   
                    {'name':'buttonGoTo','title':'Go To Number',
                            'binding':'GoTo','underline':0,
                            'hotKey':'<Alt-g>'},
                    {'name':'buttonQuit','title':'Quit',
                            'binding':'Cancel','underline':0,
                            'hotKey':'<Alt-q>'}  ]

        smgDialog.__init__(self,parent,title=title, buttons=btns,
                    buttonsDef=-1, buttonsWidth=0, buttonsPad=5, 
                    resizeable=1, transient=1, wait=1) #buttonsPos='BOTTOM'
 
    #def ImportDataModules(self, dataModules=[]):
    #  """
    #  dataModules - a list of strings containing the names of the
    #                modules to be imported
    #  """
    #  for module in dataModules:
    #    exec 'import ' + module
    
    def Index(self, event=None):
        #this may be called by a key binding, thus the 'event=None' and the 
        #enabled check
        if self.buttonIndex.cget('state') in ('normal','active'): #if index button enabled
            #print self.buttonIndex.cget('state')
            self.showHtml(self.index)

    def Prev(self, event=None):
        #this may be called by a key binding, thus the 'event=None' and the 
        #enabled check
        if self.buttonPrev.cget('state') in ('normal','active'): #if index button enabled
            #print self.buttonIndex.cget('state')
            self.showHtml(self.MakeBrowseSource(self.hexNum-1))

    def Next(self, event=None):
        #this may be called by a key binding, thus the 'event=None' and the 
        #enabled check
        if self.buttonNext.cget('state') in ('normal','active'): #if index button enabled
            #print self.buttonIndex.cget('state')
            self.showHtml(self.MakeBrowseSource(self.hexNum+1))

    def GoTo(self, event=None):
        #this may be called by a key binding, thus the 'event=None' and the 
        #enabled check
        if self.buttonGoTo.cget('state') in ('normal','active'): #if index button enabled
            #print self.buttonIndex.cget('state')
            hexNum=tkSimpleDialog.askinteger('Go To Hexagram Number', 
                    'Enter hexagram number.',
                    parent=self,initialvalue=self.hexNum,
                    minvalue=1,maxvalue=64)
            self.showHtml(self.MakeBrowseSource(hexNum))

    def MakeBrowseSource(self,hexNum):
        self.hexNum=hexNum
        return 'pyching_int_data.in%sdata()'%(hexNum)
    
    def openDataFile(self, fileName):
        displayFile = None
        try:
            displayFile = open(fileName, 'r')
        except IOError:
            tkMessageBox.showerror(title='File Load Error',
                    message='Unable to load data file '+repr(fileName)+' .')
        #else:
        return displayFile #will be = None if there was an error
    
    def Body(self,master):
        self.configure(borderwidth=4)
        # create the text widget for html display
        baseFont = ("Times", 12)
        if os.name == "nt": baseFont = ("Times New Roman", 12)
        self.textDisplay = Text(master,height=20,width=74,wrap=WORD,
                insertofftime=0,font=baseFont,highlightthickness=0,
                padx=4,pady=8,fg=self.colorViewerFg,bg=self.colorViewerBg)
        scrollbarY=Scrollbar(master,orient=VERTICAL,width=13,
                highlightthickness=0,command=self.textDisplay.yview)
        #scrollbarX=Scrollbar(master,orient=HORIZONTAL,width=15,highlightthickness=0,
        #        command=textDisplay.xview)
        #textDisplay.configure(yscrollcommand=scrollbarY.set,
        #               xscrollcommand=scrollbarX.set)
        self.textDisplay.configure(yscrollcommand=scrollbarY.set)
        #scrollbarX.grid(row=1,column=0,sticky=(E,W))
        scrollbarY.grid(row=0,column=1,sticky=(N,S))
        
        self.textDisplay.grid(row=0,column=0,sticky=(N,S,E,W))
        master.grid_location(0,0)
        master.columnconfigure(0,weight=1)
        master.rowconfigure(0,weight=1)
        self.showHtml(source=self.htmlSource,iLink=self.internalLink,
                    plainText=self.plainText)
        
        return self.textDisplay

    def showImage(self,source,alt,align):
        #print source,source[-4:],source[:-4],alt,align
        imageType = source[-4:] #image type indicator
        if imageType[-2:] == '()': #internal image data
            try:
                exec ( 'import ' + source.split('.',1)[0] )
                self.images.append(Image('photo', data=eval(source) ) )
            except (NameError,AttributeError): #no such image data
                self.textDisplay.insert("insert", ' [image error] ')
                print("no such image data:", source)
                return #get out
        else: #image file stored on disk
            if imageType in ('.gif','.xbm'): #supported disk file image formats
                try:
                    if imageType == '.gif': #a gif file
                        self.images.append(Image('photo',file=source) )
                    elif imageCheck == '.xbm': #an x bitmap file
                        self.images.append(Image('bitmap',file=source) )
                except TclError: #most likely no such image file
                    self.textDisplay.insert("insert", ' [image error] ')
                    print("image display error:", source)
                    return #get out
            else: #can't handle this image type
                self.textDisplay.insert("insert", ' [unknown image type] ') #:'+source+'
                print("can't display image type:", source)
                return #skip the image creation
        #if we got here then insert the new image in the document
        self.textDisplay.image_create(index='insert',
                    image=self.images[(len(self.images)-1)],padx=10,pady=10)
    
    def showHtml(self,source=None,iLink=None,plainText=0):
        self.images = [] #holds image references for this document 
                         #(used above in showImages)
        htmlData='[html data error]'
        if self.sourceIsStr:
            #if source ends in '()' it is a string representing a function name
            #that will return the html data string
            #print source #debug
            sourceIsData = ( source[-2:] == '()' )
            if sourceIsData:
                try:
                    #module =
                    exec ( 'import ' + source.split('.',1)[0] )
                    exec ( 'htmlData = ' + source )
                except (ImportError,NameError,AttributeError): #no such html data
                    self.textDisplay.insert("insert", ' [hypertext data error] ')
                    print("html data module or function error:", source)
#                 return #get out
            else: #the source is a plain string holding html data
               htmlData=source
        else:
            displayFile = None
            displayFile = self.openDataFile(source) #open disk file
            htmlData = displayFile.read()
        if self.sourceIsStr or displayFile:
            self.oldCursor = self.cget("cursor")
            self.textDisplay.config(cursor="watch")
            self.textDisplay.update_idletasks()
            self.config(cursor="watch")
            self.update_idletasks()
            self.textDisplay.config(state=NORMAL)
            self.textDisplay.delete("1.0", "end")
            if self.sourceIsStr or (not plainText): #render html
                htmlWriter = HtmlWriter(self.textDisplay, self)
                htmlFormatter = formatter.AbstractFormatter(htmlWriter)
                htmlParser = HtmlParser(htmlFormatter)
                #print source #debug
                htmlParser.feed(htmlData)
                htmlParser.close()
            else: #show plain text
                self.textDisplay.insert(1.0,htmlData)  
            self.textDisplay.configure(state=DISABLED)
            self.textDisplay.config(cursor=self.oldCursor)
            self.config(cursor=self.oldCursor)
        else: #no html data
            self.textDisplay.insert("insert", ' [hypertext data error] ')
            print("no html data available:", source)
            return #get out

        if self.index: #we have an index button
            if source == self.index: #disable index button, this _is_ the index
                self.buttonIndex.configure(state=DISABLED)
            else: #enable index button
                self.buttonIndex.configure(state=NORMAL)
        
        if self.hexBrowser: #hex broser buttons        
            if self.hexNum == 1: #at 1st page
                self.buttonPrev.configure(state=DISABLED)
            else: #enable index button
                self.buttonPrev.configure(state=NORMAL)
            if self.hexNum == 64: #at last page
                self.buttonNext.configure(state=DISABLED)
            else: #enable index button
                self.buttonNext.configure(state=NORMAL)
        

class HtmlWriter(formatter.DumbWriter):
    def __init__(self, textWidget, htmlViewer):
        formatter.DumbWriter.__init__(self, self, maxcol=9999)
        self.textWidget = textWidget
        self.htmlViewer = htmlViewer
        font, size = "Times", 12
        fixed = "Courier"
        self.fontmap = {
                "h1"      : (font, size + 12, "bold"),
                "h2"      : (font, size +  7, "bold"),
                "h3"      : (font, size +  4, "bold"),
                "h4"      : (font, size +  2, "bold"),
                "h5"      : (font, size +  2, "bold"),
                "h6"      : (font, size +  1, "bold"),
                "bold"    : (font, size, "bold"),
                "italic"  : (font, size, "italic"),
                "pre"     : (fixed, size),
        }
        for f in self.fontmap.keys():
                self.textWidget.tag_config(f, font=self.fontmap[f])
        self.anchor = None
        self.anchor_mark = None
        self.font = None
        self.font_mark = None
        self.indent = ""

    def handleImage(self, source, alt, align):
        self.htmlViewer.showImage(source, alt, align)
    
    def createCallback(self, href):
        class Functor:
            def __init__(self, htmlViewer, arg):
                self.viewer = htmlViewer
                self.arg = arg
            def __call__(self, *args):
                #self.viewer.updateHistoryXYView()
                return self.viewer.showHtml(self.arg)
        return Functor(self.htmlViewer, href)

    def write(self, data):
        self.textWidget.insert("insert", data)

    def __write(self, data):
        self.textWidget.insert("insert", data)

    def anchor_bgn(self, href, name, type):
        if href:
            #self.text.update_idletasks()   # update display during parsing
            self.anchor = (href, name, type)
            self.anchor_mark = self.textWidget.index("insert")

    def anchor_end(self):
        if self.anchor:
            url = self.anchor[0]
            tag = "href_" + url
            self.textWidget.tag_add(tag, self.anchor_mark, "insert")
            self.textWidget.tag_bind(tag, "<ButtonPress>", self.createCallback(url))
            self.textWidget.tag_bind(tag, "<Enter>", self.anchor_enter)
            self.textWidget.tag_bind(tag, "<Leave>", self.anchor_leave)
            self.textWidget.tag_config(tag, foreground="blue", underline=1)
            self.anchor = None

    def anchor_enter(self, *args):
        self.textWidget.config(cursor = "hand2")

    def anchor_leave(self, *args):
        self.textWidget.config(cursor = self.htmlViewer.oldCursor)

    def new_font(self, font):
        # end the current font
        if self.font:
                self.textWidget.tag_add(self.font, self.font_mark, "insert")
                self.font = None
        # start the new font
        if font:
                self.font_mark = self.textWidget.index("insert")
                if self.fontmap.has_key(font[0]):
                        self.font = font[0]
                elif font[3]:
                        self.font = "pre"
                elif font[2]:
                        self.font = "bold"
                elif font[1]:
                        self.font = "italic"
                else:
                        self.font = None

    def new_margin(self, margin, level):
        self.indent = "    " * level
        #print 'new_margin called'

    def send_label_data(self, data):
        self.__write(self.indent + data + " ")
        #print 'send_label_data called:', data

    def send_paragraph(self, blankline):
        if self.col > 0:
                self.__write("\n")
        if blankline > 0:
                self.__write("\n" * blankline)
        self.col = 0
        self.atbreak = 0
        #print 'send_paragraph called'

    def send_hor_rule(self, *args):
        width = int(int(self.textWidget["width"]) * 0.9)
        self.__write("_" * width)
        self.__write("\n")
        self.col = 0
        self.atbreak = 0
        #print 'send_hor_rule called'

class HtmlParser(htmllib.HTMLParser):
    def anchor_bgn(self, href, name, type):
        htmllib.HTMLParser.anchor_bgn(self, href, name, type)
        self.formatter.writer.anchor_bgn(href, name, type)

    def anchor_end(self):
        if self.anchor: self.anchor = None
        self.formatter.writer.anchor_end()

    def do_dt(self, attrs):
        self.formatter.end_paragraph(1)
        self.ddpop()
    
    def handle_image(self, source, alt, ismap, align, width, height):
        self.formatter.writer.handleImage(source, alt, align)
