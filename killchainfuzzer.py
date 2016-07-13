#!/usr/bin/env python
#
# Copyright (c) 2016 SafeBreach
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import itertools
import argparse
import csv


####################
# Global Variables #
####################

__version__ = "1.0"
__author__ = "Itzik Kotler"
__copyright__ = "Copyright 2016, SafeBreach"


#############
# Functions #
#############

def main(argv):
    parser = argparse.ArgumentParser(description='Kill Chain Fuzzer')
    parser.add_argument('steps', metavar='STEP #', type=int, nargs='*', default=[7], help='a mandatory STEP NUMBER to include in the result')
    parser.add_argument('-o', '--output-file', nargs='?', type=argparse.FileType('w+'), default=sys.stdout)
    config = parser.parse_args(argv[1:])

    writer = csv.writer(config.output_file)
    writer.writerow(['Reconnaissance', 'Weaponization', 'Delivery', 'Exploitation', 'Installation', 'Command and control', 'Action on objectives'])

    for x in itertools.product(['V', 'X'], repeat=7):
        if len(filter(lambda x: x == 'V', [x[i-1] for i in config.steps])) == len(config.steps):
            writer.writerow(x)


#########
# Entry #
#########

if __name__ == "__main__":
    sys.exit(main(sys.argv))
