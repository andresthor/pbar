#!/usr/bin/env python
# ==============================================================================
# Title:       Terminal colors
# File:        tcolor.py
# Author:      Andres Saemundsson, andresthor@gmail.com
#
# Description: Contains the basic ANSI escape codes used to change the color of
#              text in the terminal window.
# ==============================================================================


class base_colors:
    def wrap(color):
        CSI = '\x1B['
        BG  = ';49m'

        return CSI + str(color) + BG

    BLACK   = wrap(30)
    RED     = wrap(31)
    GREEN   = wrap(32)
    YELLOW  = wrap(33)
    BLUE    = wrap(34)
    MAGENTA = wrap(35)
    CYAN    = wrap(36)
    WHITE   = wrap(37)
    CLR     = wrap(39)
