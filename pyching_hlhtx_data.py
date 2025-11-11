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
hypertext data return routines for pyching
each of these functions returns the html information data
for one help page back to pyching_interface_tkinter for
display
"""

def hlHelpData():
 return """
<html><body><p>
<h2>Using pyChing - Help Index</h2>
<p>
pyChing is a program that enables you to perform an I Ching reading using the coin oracle. By casting three coins, you generate 'lines' which are used to build up one or two figures of six lines each, known as hexagrams. These hexagrams are then used as keys to consult the text of an ancient Chinese book of wisdom called the I Ching, or Book of Changes.
<br>Click on the links below to view help on these topics:
<p>
<a href="pyching_hlhtx_data.hlIntroData()">Inroduction to the I Ching</a><br>
A brief introduction to the I Ching itself, including a description of the
coin method used by pyChing.
<p>
<a href="pyching_hlhtx_data.hlReadingData()">Performing a reading</a><br>
A general description of how to use pyChing to perform an I Ching reading.
<p>
<a href="pyching_hlhtx_data.hlMenuData()">Menu commands</a><br>
What all the menu choices in pyChing do.
<p>
<a href="pyching_hlhtx_data.hlButtonData()">Command Buttons in the Reading Area</a><br>
What the command buttons in the reading area do.
<p>
<a href="pyching_hlhtx_data.hlDialogData()">Dialog Boxes</a><br>
How to operate the various dialog boxes that you will see while using pyChing.
<p></body></html>
"""

def hlIntroData():
 return """
<html><body><p>
<h2>Introduction to the I Ching</h2>
<p>
Following is an extremely brief introduction to what the I Ching actually is, after which is a quick explanation of the coin method used by pyChing to perform its readings, a quick note on wording, and pointers to a couple of books where you would be able to obtain more useful information on the I Ching and the related philosophy of Taoism.
<p>
The I Ching, or Book Of Changes, is an ancient Chinese book (its origins date back perhaps 5,000 years) that has been used since time immemorial as a source of wisdom or advice in dealing with life's complexities. 
<p>
The book can simply be read or browsed to glean insight or inspiration,  but it is also commonly consulted as an oracle, by formulating a question  and using some means of harnessing chance (or more interestingly,  synchronicity, as described by Carl Jung in his foreword to the Wilhelm  translation [see below]) to build one or two 'hexgrams' (figures  constructed from six lines), which are meant to be keys to the heart of  the underlying issues surrounding the question asked. 
<p>
Two of the more time honoured methods of consulting the oracle (or,  'casting' a hexgram) are by the manipulation of yarrow stalks, or the use  of three coins. The coin method is the one used by pyChing. Once the  hexgrams have been built their corresponding passages in the I Ching may  be looked up to give some extra information or insight into the issues  surrounding the question, or to provide a different perspective on the  situation described in the question. 
<p>
The I Ching is treated very seriously by those who use it as a source of  wisdom and self development. The book, and its underlying philosopy of  change being a key aspect of life and existence, are closely associated  with the philosophy of Taoism. Some would say that the use of the I Ching  as an oracle at all trivialises its underlying importance, while others  would say that using the book in this way is simply another way to access the wisdom it contains. In any case it is generally accepted by users of  the I Ching that the spirit it is consulted in is the important thing, and that any results you get from consulting it will be in accordance with  your sincerity in approaching the I Ching.
<p>
The coin oracle, the method used by pyChing to perform I Ching readings, is briefly outlined below, followed by a note on wording and a couple of  pointers to further reading. Please bear in mind that the information on  the hexagrams presented within pyChing is very brief. If you are (or you  become) at all interested in the I Ching I strongly recommend that you  obtain one of the many translations or in-depth books available on the  subject.
<p>
<h3>The Coin Oracle</h3>
<p>
This method of casting I Ching hexagrams involes the use of three coins, which are tossed simultaneously six times, with each toss of the coins rendering one of the hexagram's six lines. Afficianados of this method often prefer to employ old Chinese coins with a square hole in the middle and an inscription on one side. With this type of coin the inscribed side generally represents Yin (passive, fecund, shadow energy) with a value of 2, while the other side represents Yang (creative, active, light energy) with a value of 3. If you happen to use any other kind of coins to perform a reading just decide in advance which side represents Yin and which represents Yang (tails for Yin and heads for Yang might be a good choice).
<p>
The values of the three thrown coins are added together to give the value for that line. Each of the four possible line values (6,7,8 or 9)  indicates a particular type of line to be drawn in building the first  hexagram, as follows:
<p>
<b>6</b>,  represents a moving (old) Yin line, which is drawn as: 
            <pre>   ---- X ----</pre>   
     (a line with a gap that has a cross in it)<p>
     
<b>7</b>,  represents a static (young) Yang line, which is drawn as: 
            <pre>   -----------</pre>
     (a line with no gap)<p>     

<b>8</b>,  represents a static (young) Yin line, which is drawn as: 
            <pre>   ----   ----</pre>
     (a line with a gap in the middle)<p>     

<b>9</b>,  represents a moving (old) Yang line, which is drawn as: 
            <pre>   -----O-----</pre>
     (a line with no gap with a circle in the middle)<p>

The hexagram is built from the bottom upwards. 
<p>
Any moving lines (6's or 9's) are counted as changing into the opposite  kind of (non-moving) line, therefore a 6 (moving Yin) line becomes a 7  (Yang) line and a 9 (moving Yang) line becomes an 8 (Yin) line. If there are any of these moving lines in the first hexagram, a second hexagram is constructed by changing the moving lines to into their new types, while  any non-moving lines remain the same. If there are no moving lines in the  first hexagram then the reading consists of only one hexgram.
<p>
The casting of the hexagram(s) is now complete, and you can look up the sections in the I Ching that correspond to these hexgrams and try to relate what you read there back to your question in any way you can. The positions (places) of any moving lines in the first hexagram are particularly significant. 
<p>
<h3>A quick note on the wording used in pyChing</h3>
<p>
<b>Hexagram Names</b>
<p>
Firstly I should note here that the names of the hexgrams as presented in pyChing may vary from any books on the subject you consult (although of  course the hexagram numbers are always the same). There are several systems for  attempting to render Chinese words into pronounceable english (and in fact, if you read more than one translation of the I Ching you will find the names spelt in many different ways, but they should always sound pretty much the same when you say them), apart from the one I have followed here.
<p>
<b>Hexagram Information</b>
<p>
The information on (interpretation of) the hexagrams presented in pyChing is couched in the usual flowery language that results from attempts to translate extremely terse and ancient Chinese into western languages. (If you read any of the full translations available you will find that the various translators have found lots of scope for variation on the theme of the undelying phrases also, although the bones always remain the same.) This can lead to some problems in dealing with some of the recurring motifs in the text.
<p>
If you find all the 'he' and 'the superior man' stuff you might read in  some translations a tad sexist, remember that these gender specific  pronouns are inserted by the translators in order to make sentences which  scan better in western-style languages. The original language is said to  be formed of such extremely terse and compact imagery that it barely contains any pronoun-like elements at all. So if these constructs bother you feel free to substitute 'she' or 'the superior woman' to your heart's content.
<p>
On the subject of phrases like 'the sage', 'the superior man', or 'the  superior person', it may be useful to think of them as indicatiing someone who has attained some degree of wisdom, ie, the position you may  be aspiring to. 
<p>
Lastly, let me just say that if all the talk about 'heaven' bothers you,  you can think of the idea the translators have tried to convey with that  word as representing 'the cosmic oneness' or 'the essence of the universe' or 'the underlying way of things' or whatever else makes sense in your personal mythology.
<p>
The main point is, read the imagery, and go with whatever ideas related to your question you find arising in your mind, trust the angle that makes  sense to you or feels right to you!
<p>
<h3>Further Reading</h3>
<p>
There have been many translations of the I Ching, and many books written on the subject and on the related subject of Taoism, a philosophy that embraces the underlying principle of change expressed in the I Ching and the notion of accepting change and becoming attuned to 'the way things are really going'.
<p>
Many libraries and bookstores will have titles on these subjects in their philosophy or religion or 'new age' sections. So if you're interested why not seek something out yourself from one of these sources?
<p>
Below are the details of one of the books on each of these subjects that I have personally found interesting, your mileage may vary.
<p>
<b>The I Ching</b>
<p>
Just about the most famous translation of the I Ching into a western language is the one made by Richard Wilhelm (rendered from his german into english by Cary F. Barnes). This edition is widely available and has been in print since the 1950's up until the present day. It is titled simply 'I Ching or Book Of Changes' and contains an excellent foreword by the famous psychologist and philosopher C.G. Jung, where he attempts to explain the use of the I Ching in terms of his psychological theories.
<p>
<b>Taoism</b>
<p>
On the subject of Taoism, one of the most interesting books I have read is 'The Tao of Zen' by Ray Grigg. Which attempts to trace the historical development of Taosim in relation to the author's theory that Zen developed out of Taoism. I found the book to also have lots of interesting general information about what Taoism actually is, in case you are  wondering.
<p></body></html>
"""

def hlReadingData():
 return """
<html><body><p>
<h2>Performing a Reading</h2>
<p>
Click on the button 'Cast New Hexagram'. pyChing will then prompt you to enter the question you wish to ask when you consult the I Ching. Your question can be as specific or general as you wish. If you wish to perform a general reading about your current circumstances you can just accept the default question. Concentrate on your question and click on 'Ok' to enter it.
<p>
If you have 'Cast Entire Hexagram Automatically' on the 'Settings' menu checked (the default setting), pyChing will then cast the three coins six times to build up the first hexagram. If you have 'Cast Each Line Separately' checked instead (the two choices are mutually exclusive), then pyChing will wait for you to click the 'Cast line x of 6' button yourself, to cast each of the six lines. This is more like the process of conducting a reading using real coins, where you throw the coins by hand separately  for each line. In either case, keep your question in mind while the lines are cast.
<p>
After the first hexagram is completed a second hexagram will be created if the first hexagram contains any 'moving' (changing) lines. If there are no moving lines the reading results in only one hexagram. If you are casting each line separately pyChing will wait for you to click on 'Create 2nd Hexagram' before building the second hexagram. If there is no second hexagram then 'no moving lines' is displayed.
<p>
Two buttons will now appear, in place of the coins, which allow you to  view the information (interpretation) of each of the hexagrams you have cast. (Only one button appears if there were no moving lines).
<p>
If you move the mouse pointer above any line in either hexagram, a description of that line will appear in the status bar. If 'Show Line Hints' on the 'Settings' menu is checked, the line description will also appear in a pop-up 'hint' below the line, for as long as the mouse pointer is over the line.
<p>
Take note of which 'place' (the place names appear to the left of the first hexagram, provided 'Show Places' is checked on the 'Settings' menu) any 'moving' line appears in (the moving lines have a value of 6 or 9 and have a cross or circle in the middle, respectively). The places the sixes and nines appear in in the first hexagram (there won't be any if there were no moving lines) are used to look up special sections at the end of the hexagram information. Any moving lines are considered to be especially significant as they indicate the points of change which result in the first hexagram 'becoming' (changing into) the second hexagram, which represents the development or unfolding of the issues raised in your question.
<p></body></html>
"""

def hlMenuData():
 return """
<html><body><p>
<h2>Menu Commands</h2>
<p>
Here follows a brief description of the actions performed by each menu choice in pyChing.
<p>
<h3>File Menu</h3>
<p>
<b>Load Reading</b> - Allows any previously saved pyChing readings to be loaded. This is for readings previously saved with the normal 'Save Reading'  command, readings that were saved as text are for use outside of  pyChing (see below). The Load Saved Reading dialog box is described in the 'Dialog Boxes' help topic.
<p>
<b>Save Reading</b> - Saves the current pyChing reading to disk, so that it can later be loaded back into pyChing with the 'Load Reading' command (see above). The Save Reading dialog box is described in the 'Dialog Boxes' help topic.
<p>
<b>Save Reading As Text</b> - Saves a representation of the current reading as a plain text file. This text file may then be loaded into your favourite text editor for printing or any other purpose.   The Save Reading As Text dialog box  is described in the 'Dialog Boxes' help topic.
<p>                       
<b>Exit</b>  -  Quits pyChing
<p>
<h3>Settings Menu</h3>
<p>
<b>Show Places</b> -  Toggle. If checked, the names of the line places will be displayed to the left of the first hexagram.
<p>
<b>Show Line Hints</b> -  Toggle. If checked, line descriptions will be shown as pop-up hints when the mouse pointer is over a line, as well as on the status line.
<p>
<b>Cast Each Line Separately</b> -  If checked, each line is cast separately under user control. This option is mutually exclusive with the option below, checking one un-checks the other.
<p>
<b>Cast Entire hexagram Automatically</b> -  If checked, the entire hexagram casting process is carried out automatically by pyChing. This option is mutually exclusive with the option above, checking one un-checks the other.
<p>
<b>Configure Colors</b> -  Allows configuration of the colours in the reading area. The Color  Configuration dialog is described in the 'Dialog Boxes' help topic.
<p>
<b>Save Settings</b> -  Saves the current pyChing settings to disk so that they will be remembered in future pyChing sessions.
<p>
<h3>Help Menu</h3>
<p>
<b>Using pyChing</b> -  Shows the help you are reading right now.
<p>
<b>Introduction to the I Ching</b> -  Displays a brief introduction to the I Ching itself.
<p>
<b>Browse Hexagram Information</b> -  Allows you to browse the available information on each hexagram.
<p>
<b>About pyChing</b> -  Shows pyChing's About box. License details and program credits can also be viewed from the About box.
<p></body></html>
"""

def hlButtonData():
 return """
<html><body><p>
<h2>Command Buttons in the Reading Area</h2>
<p>
<h3>Cast New Hexagram</h3> Causes pyChing to do its thing; performing an I Ching reading by casting I Ching hexagrams using the coin oracle. If 'Cast Each Line Separately' is checked on the 'Settings' menu, this button also performs the following two functions:
<p>    
<b>Cast Line x of 6</b> - Manually cast the next line in sequence. (x steps from 1 to 6)
<p>      
<b>Create 2nd Hexagram</b> - Causes the second hexagram to be built. Appears after the first      one has been manually completed.
<p>        
<h3>View information on: xx nnnn</h3> Shows information on (interpretation of) a hexagram in the current reading, where xx is the I Ching hexagram number and nnnn is the I Ching hexagram name.
<p></body></html>
"""

def hlDialogData():
 return """
<html><body><p>
<h2>Dialog Boxes</h2>
<p>
<h3>Enter Question</h3>
<p>
The Enter Question dialog is displayed as the first step in performing a new reading. Click on 'Ok' to accept the default question or select it (by dragging over it with the mouse) and overtype your own question, which may be up to 70 characters in length. Keep your question short and to the point. Click on 'Cancel' to  cancel the new reading.
<p>
<h3>Load Saved Reading, Save Reading, Save Reading As Text</h3>
<p>
The exact details of how these dialogs operate depend on the platform you are running pyChing on (pyChing _should_ run on any platform where the correct versions of Python and Tk are available, including Unix/Linux/X11, Windows95/98/NT and MacOs), but the general principles are the same. In all cases you will see a file listing of the relevant types of files  (pyChing save files, or text files). For loading you select the file you  want to load and click 'Open' or 'Ok' or whatever the case may be meaning  'go ahead and do it'. For saving you type in the name of the file you want to save (pyChing will add the file extension for you) and click 'Save' or 'OK' or whatever means 'do it' (you can also select an existing save file to replace). 
<p>
On some platforms you are able to do things like like delete or rename or move existing save or text files right from within these  dialog boxes. Where you can't do that, go ahead and use your favourite file manager for this purpose instead. 
<p>
<h3>Configure Colors</h3>
<p>
This dialog allows you to configure some the colours in pyChing to your personal tastes. It contains the following command buttons and controls:
<p>
<b>Set Color of: [ display element ]</b>  -  This button is just to the left of another button that shows the name of the display element whose color you are currently  dealing with. These two buttons are surrounded by a rectangular  area that shows a sample of the color in question. Clicking on 'Set Color of:' will show a (platform specific) color selection dialog that lets you choose a new colour for the current display element if you wish. Clicking on the button that shows the name of the current display element shows a list of choices from which you  can select a different display element to deal with.
<p>        
<b>Color Example Area</b>  -  This area in the middle of the dialog shows a sample of how your  new color scheme will appear. You can also click on the different  display element samples here as an alternative way of selecting  them as the current display element.
<p>        
<b>Reset All Colors To pyChing Defaults</b>  -  Clicking on this button will revert to pyChing's default built-in color scheme.
 When you have chosen new colors you are happy with click on 'OK' to accept them or 'Cancel' to cancel the changes. Don't forget to click on 'Save Settings' in the 'Settings' menu if you want pyChing to remember your changes between sessions.                
<p>
<h3>About pyChing</h3>
<p>
Displays some information about the version of pyChing you are running. This dialog also has the following command buttons:
<p>
<b>View License</b>  -  Click this to view the full details of the GNU General Public License, under which pyChing has been released.
<p>  
<b>View Credits</b>  -  Click this to view a list of credits relating to pyChing.
<p> 
<b>Ok</b>  -  Click this when you're finished with the About box.
<p>
The pyChing version number will have 'beta' added to it if it is a possibly unstable version that has not yet been fully tested. Other (stable) versions should hopefully have less show stopping bugs and less incomplete features, because they've been tested a little more on some platforms. Most testing of pyChing takes place on Linux, so if you run it on some other platform I'd particularly  like to know how it goes, or get any detailed bug reports. Contact details  are shown in the About box.  
<h3>Help and Information Viewer</h3>
<p>
If you are viewing one of pyChing's help files, there will be an 'Index' button at the bottom of the dialog (which will be disabled if you are actually viewing the help index). Click on the 'Index' button to return to the 'Using pyChing - Help Index' page. In any of these help or information viewer windows, just click on 'Ok' when you've seen enough... (I seriously doubt I needed to tell you that.  ;-)
<h3>Hexagram Information Browsing</h3>
<p>
The hexagram information browser lets you browse the available information for any hexagram you wish. Click on the 'Prev' or 'Next' buttons (if active) to browse info on the next or previous hexagram (in numbered sequence). To view information on a particular hexagram, click on 'Go To Number' and enter the number (from 1 to 64) of the hexagram you wish to view. The 'Quit' button, of course, quits the browser.
<p></body></html>
"""

#end of module
