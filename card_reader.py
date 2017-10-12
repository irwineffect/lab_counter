#!/usr/bin/python
import termios
from copy import deepcopy

class card_reader():
    def __init__(self):
        self.prev_termattr = termios.tcgetattr(0)
        self.new_termattr = deepcopy(self.prev_termattr)
        self.new_termattr[3] = self.new_termattr[3] & ~termios.ECHO

    def read(self):
        self._setup_term()
        while True:
            line = raw_input()
            if self._verify_line(line) != 0: #card not recognized
                print "card not recognized, please swipe again"
                continue
            #else, card recognized
            self._restore_term()
            return self._extract_id(line)

    def _verify_line(self,line):
        #confirm line length
        if len(line) != 95:
            return 1

        #variety of markers that appear to be present on wsu id cards
        if line[0] != '%':
            return 1
        if line[11] != '^':
            return 1
        if line[14] != '?':
            return 1
        if line[15] != ';':
            return 1
        if line[32] != '=':
            return 1
        if line[40] != '=':
            return 1
        if line[53] != '?':
            return 1
        if line[54] != '+':
            return 1
        if line[71] != '=':
            return 1
        if line[81] != '=':
            return 1

        #if we get to this point, the swipe was probably good
        return 0

    def _extract_id(self, line):
        return line[23:31]

    def _setup_term(self):
        termios.tcsetattr(0, termios.TCSANOW, self.new_termattr)

    def _restore_term(self):
        termios.tcsetattr(0, termios.TCSANOW, self.prev_termattr)

    def __del__(self):
        self._restore_term()


if __name__ == "__main__":
    reader = card_reader()
