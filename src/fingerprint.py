#!/usr/bin/env python

from copy import deepcopy
import json
import numpy as np
import sys

from pprint import pprint
from pylab import *  # @UnusedWildImport


averaged = {}

def average_rssi(pos, data):
    rssi = 0
    for msr in data:
        rssi += msr['rssi_a']
        rssi += msr['rssi_b']
        rssi += msr['rssi_c']

    averaged[pos]['rssi'] = rssi / 3 / len(data)


def average_csi(pos, data):

    for i in range(len(data)):
        for antenna in ['csi_a', 'csi_b', 'csi_c']:
            # amplitude
            data[i][antenna] = [abs(complex(x)) for x in data[i][antenna]]
            # power
            data[i][antenna] = [pow(x, 2) for x in data[i][antenna]]
            # dB
            data[i][antenna] = 10. * np.log10(data[i][antenna])

    avg_csi_a, avg_csi_b, avg_csi_c = 30 * [0], 30 * [0], 30 * [0]
    for node in data:
        avg_csi_a = np.add(avg_csi_a, node['csi_a'])
        avg_csi_b = np.add(avg_csi_b, node['csi_b'])
        avg_csi_c = np.add(avg_csi_c, node['csi_c'])

    averaged[pos]['csi_a'] = np.divide(avg_csi_a, 10)
    averaged[pos]['csi_b'] = np.divide(avg_csi_b, 10)
    averaged[pos]['csi_c'] = np.divide(avg_csi_c, 10)


if __name__ == '__main__':
    with open(sys.argv[1], 'rt') as infile:
        csi_dict = json.load(infile)

    for pos, data in csi_dict.iteritems():
        averaged[pos] = {}
        average_rssi(pos, data)
        average_csi(pos, data)

    pprint(averaged)
