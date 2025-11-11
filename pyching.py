#!/usr/bin/env python3
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
start-up module for pyching
"""

import sys

#handle command line switches
def CommandLineSwitches() -> None:
    if ('-h' in sys.argv) or ('/h' in sys.argv) or('--help' in sys.argv):
        print(' pyChing - command line switches\n')
        print(' -h, --help                   display this help message')
        print(' -v, --version                display pyching version')
        print(' -d, --disable-version-check  disable Python and Tk version check')
        print(' -c, --console                run the console version of pyChing')
        sys.exit(0)
    elif ('-v' in sys.argv) or ('/v' in sys.argv) or('--version' in sys.argv):
        from pyching_engine import PychingAppDetails
        pyching = PychingAppDetails(createConfigDir=0)
        print('pyChing version:', pyching.version)
        sys.exit(0)

    if ('-d' in sys.argv) or ('/d' in sys.argv) or('--disable-version-check' in sys.argv):
        sys.stderr.write("warning - Python and Tk version checking disabled!\n")
    else: #do version checking
        from tkinter import TkVersion
        if sys.version_info < (3, 10): #python version check
            sys.stderr.write("Sorry, pyChing requires at least Python 3.10\n")
            sys.exit(1)
        if TkVersion < 8.0: #tk version check
            sys.stderr.write("Sorry, pyChing requires at least Tk 8.0\n")
            sys.exit(1)

def main() -> None:
    """Main entry point for pyChing"""
    CommandLineSwitches()

    #run pyching

    if ('-c' in sys.argv) or ('/c' in sys.argv) or('--console' in sys.argv):
        #run the console version of pyChing
        import pyching_interface_console
        pyching_interface_console.main()
    else:
        #run pyching Tkinter GUI
        import pyching_interface_tkinter

    #if we got to here exit cleanly
    sys.exit(0)


if __name__ == '__main__':
    main()
