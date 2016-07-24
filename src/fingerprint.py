#!/usr/bin/env python

from __future__ import division
from copy import deepcopy
from pprint import pprint
from pylab import *  # @UnusedWildImport

import json
import numpy as np
import sys


averaged = {}


def average_rssi(pos, data):
    rssi_a, rssi_b, rssi_c = 0, 0, 0
    for msr in data:
        rssi_a += msr['rssi_a']
        rssi_b += msr['rssi_b']
        rssi_c += msr['rssi_c']

    averaged[pos]['rssi_a'] = rssi_a / len(data)
    averaged[pos]['rssi_b'] = rssi_b / len(data)
    averaged[pos]['rssi_c'] = rssi_c / len(data)
    averaged[pos]['rssi'] = (rssi_a + rssi_b + rssi_c) / 3 / len(data)


def average_csi(pos, data):

    for node in data:
        for antenna in ['csi_a', 'csi_b', 'csi_c']:
            # amplitude
            node[antenna] = [abs(complex(x)) for x in node[antenna]]
            # power
            node[antenna] = [pow(x, 2) for x in node[antenna]]
            # dB
            node[antenna] = 10. * np.log10(node[antenna])

    avg_csi_a, avg_csi_b, avg_csi_c = 30 * [0], 30 * [0], 30 * [0]

    for node in data:
        avg_csi_a = np.add(avg_csi_a, node['csi_a'])
        avg_csi_b = np.add(avg_csi_b, node['csi_b'])
        avg_csi_c = np.add(avg_csi_c, node['csi_c'])

    averaged[pos]['csi_a'] = np.divide(avg_csi_a, len(data))
    averaged[pos]['csi_b'] = np.divide(avg_csi_b, len(data))
    averaged[pos]['csi_c'] = np.divide(avg_csi_c, len(data))


if __name__ == '__main__':
    with open(sys.argv[1], 'rt') as infile:
        csi_dict = json.load(infile)

    for pos, data in csi_dict.iteritems():
        averaged[pos] = {}
        average_rssi(pos, data)
        average_csi(pos, data)

    pprint(averaged)
