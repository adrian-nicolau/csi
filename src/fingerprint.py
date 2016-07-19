#!/usr/bin/env python

import json
import sys

from pprint import pprint


def average(csi_node):
    pass

if __name__ == '__main__':
    # with open(sys.argv[1], 'rt') as infile:
    #     csi_dict = json.load(infile)
    #
    # for k, v in csi_dict.iteritems():
    #     print k
    #     print average(v)

    for top in range(0, 10000000, 10):
        counter = 0
        l = range(1, top + 1)
        strList = ''.join(str(x) for x in l)
        for c in strList:
            if c == '1':
                counter += 1
        print 'for', top, 'counter is', counter

        if top == counter and top != 0:
            print 'hooooooooorayy!!!!!!'
