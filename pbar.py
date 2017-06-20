#!/usr/bin/env python
# ==============================================================================
# Title: Progress bar
# File:  pbar.py
# Author: Andres Saemundsson, andresthor@gmail.com
#
# Description: Create a simple progress bar that displays on the terminal. The
#              appearance of the progress bar is fully configurable. There is an
#              option to change the color of the text and include a message.
#
#              Example output:
#              Updating...               [#############################-]  95.5%
# ==============================================================================

import os
import sys
import time

from tcolor import base_colors as bc


class appearance:
    def __init__(self, length=0):
        self.fg     = '#'
        self.bg     = '-'
        self.left   = '['
        self.right  = ']'

        self.color  = bc.CLR
        self.length = length


class pbar(object):
    def __init__(self, length=40):
        '''Create a pbar (progress bar) object, with default settings'''
        self.app   = appearance(length=length)
        self.align = 0
        self.msg   = ''
        self.set_alignment('right')

    def update(self, value, total=100):
        '''Writes the pbar to the terminal screen with current settings.

            @param: value   How far the bar has progressed towards the total
                    total   The final value that the pbar progresses towards
        '''

        warning = ('value is {:.2f} but should not surpass the total, {:.2f}'
                   .format(value, total))
        assert value <= total, warning

        prog = int(round(self.app.length * value / float(total)))
        perc = round(100.0 * value / float(total), 1)
        bar  = self.app.fg * prog + self.app.bg * (self.app.length - prog)

        space = self._perc_space(perc)

        make_string = self._left_adj if self.align == 0 else self._right_adj
        out = make_string(bar, space, perc)

        sys.stdout.write(self.app.color + out + bc.CLR)
        if value == total:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def _perc_space(self, perc):
        '''Returns 1, 2 or 3 spaces to fill out the percentage string'''
        space = ' '
        if perc < 10:
            space = 3 * space
        elif perc < 100:
            space = 2 * space

        return space

    def _right_adj(self, bar, space, perc):
        '''Returns the progress bar string, right adjusted'''
        return ('{}{}{}{}{}{}{}{}\r'
                .format(self.msg,
                        (self.align - len(self.msg)) * ' ',
                        self.app.left, bar, self.app.right,
                        space, perc, '%'))

    def _left_adj(self, bar, space, perc):
        '''Returns the progress bar string, left adjusted'''
        return ('{}{}{}{}{}{}{}{}\r'
                .format(self.app.left, bar, self.app.right,
                        space, perc, '%',
                        (self._calc_margin() - len(self.msg)) * ' ',
                        self.msg))

    def _calc_margin(self):
        '''Returns the number of columns available after writing out the pbar
           without any message'''
        cols = self._get_width()
        # 7 = space + percentage
        return (int(cols) - self.app.length -
                len(self.app.left) - len(self.app.right) - 7)

    def _get_width(self):
        '''Returns the total width of the terminal, in characters'''
        _, cols = os.popen('stty size', 'r').read().split()
        return cols

    def set_message(self, msg):
        '''Sets a message that is displayed next to the pbar'''
        assert len(msg) < self._calc_margin(), 'message does not fit in margin'

        self.msg = msg

    def set_alignment(self, align='right'):
        '''The pbar can appear left or right adjusted. Any value other than
           "right" will make the bar left adjusted'''
        if align == 'right':
            margin = self._calc_margin()
            self.align = margin
        else:
            self.align = 0

    def set_fg(self, fg='#'):
        '''Set the foreground symbol for the bar. I.e. the completed part'''
        self.app.fg = fg

    def set_bg(self, bg='-'):
        '''Set the background symbol for the bar. I.e. the not completed part'''
        self.app.bg = bg

    def set_left(self, left='['):
        '''Set the symbol that closes the bar on the left'''
        self.app.left = left

    def set_right(self, right=']'):
        '''Set the symbol that closes the bar on the right'''
        self.app.right = right

    def set_appearance(self, fg=None, bg=None, left=None, right=None,
                       color=None, length=None):
        '''Set any or multiple appearance variables at the same time'''
        if fg is not None:
            self.set_fg(fg)
        if bg is not None:
            self.set_bg(bg)
        if left is not None:
            self.set_left(left)
        if right is not None:
            self.set_right(right)
        if color is not None:
            self.set_color(color)
        if length is not None:
            self.set_length(length)

    def set_length(self, length=40):
        '''Set the length of the bar'''
        self.app.length = length
        if self.align == 0:
            self.set_alignment('left')
        else:
            self.set_alignment('right')

    def set_color(self, color='default'):
        '''Set the color of the text. The base terminal colors are available.'''
        self.app.color = {
            'default':  bc.CLR,
            'red':      bc.RED,
            'blue':     bc.BLUE,
            'green':    bc.GREEN,
            'yellow':   bc.YELLOW,
            'black':    bc.BLACK,
            'white':    bc.WHITE,
            'magenta':  bc.MAGENTA,
            'cyan':     bc.CYAN
        }.get(color, bc.CLR)


class timed_pbar(pbar):
    '''A progress bar that runs for a specified time'''

    def __init__(self, length=40, time=10, interval=100):
        '''Create tbar with default values. Set the total time and how often the
           progress should be updated'''
        pbar.__init__(self, length=length)
        self.time = time
        self.interval = interval

    def start(self):
        '''Run the tbar with the current settings. Runs until completed.'''
        for i in range(1, self.interval + 1):
            factor = i * 1.0 / self.interval
            self.set_message('{:.1f}s'.format(factor * self.time))
            self.update(i, self.interval)
            time.sleep(self.time * 1.0 / self.interval)

    def set_time(self, time=10):
        self.time = time
