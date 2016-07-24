#!/usr/bin/env python

from __future__ import division
from copy import deepcopy
from pprint import pprint
from pylab import *  # @UnusedWildImport

import json
import numpy as np
import sys


offline_avg = {}
online_avg = {}
euclideans = {}


def find_my_pos(k=1):
    score = sys.maxint

    for pos in euclideans:
        curr_score = (euclideans[pos]['dist_csi_a'] +
                      euclideans[pos]['dist_csi_b'] +
                      euclideans[pos]['dist_csi_c']) * 0.75
        curr_score += euclideans[pos]['dist_rssi'] * 1.25

        print pos, curr_score

        if curr_score < score:
            score = curr_score
            rpos = pos

    return rpos


def euclidean_distance(data1, data2, pos):
    euclideans[pos] = {}

    euclideans[pos]['dist_csi_a'] = np.linalg.norm(
        data1['csi_a'] - data2['csi_a'])
    euclideans[pos]['dist_csi_b'] = np.linalg.norm(
        data1['csi_b'] - data2['csi_b'])
    euclideans[pos]['dist_csi_c'] = np.linalg.norm(
        data1['csi_c'] - data2['csi_c'])

    euclideans[pos]['dist_rssi_a'] = abs(data1['rssi_a'] - data2['rssi_a'])
    euclideans[pos]['dist_rssi_b'] = abs(data1['rssi_b'] - data2['rssi_b'])
    euclideans[pos]['dist_rssi_c'] = abs(data1['rssi_c'] - data2['rssi_c'])
    euclideans[pos]['dist_rssi'] = abs(data1['rssi'] - data2['rssi'])


def test_plot(pos, indict):
    plot(indict[pos]['csi_a'], label='RX Antenna A')
    plot(indict[pos]['csi_b'], label='RX Antenna B')
    plot(indict[pos]['csi_c'], label='RX Antenna C')

    axis([0, 30, 5, 30])
    xlabel('Subcarrier index')
    ylabel('SNR [dB]')
    legend(loc='lower right')
    show()


def average_rssi(pos, data, outdict):
    rssi_a, rssi_b, rssi_c = 0, 0, 0
    for msr in data:
        rssi_a += msr['rssi_a']
        rssi_b += msr['rssi_b']
        rssi_c += msr['rssi_c']

    outdict[pos]['rssi_a'] = rssi_a / len(data)
    outdict[pos]['rssi_b'] = rssi_b / len(data)
    outdict[pos]['rssi_c'] = rssi_c / len(data)
    outdict[pos]['rssi'] = (rssi_a + rssi_b + rssi_c) / 3 / len(data)


def average_csi(pos, data, outdict):

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

    outdict[pos]['csi_a'] = np.divide(avg_csi_a, len(data))
    outdict[pos]['csi_b'] = np.divide(avg_csi_b, len(data))
    outdict[pos]['csi_c'] = np.divide(avg_csi_c, len(data))


if __name__ == '__main__':
    with open(sys.argv[1], 'rt') as offline_file:
        csi_dict = json.load(offline_file)

    with open(sys.argv[2], 'rt') as online_file:
        online_dict = json.load(online_file)

    for pos, data in csi_dict.iteritems():
        offline_avg[pos] = {}
        average_rssi(pos, data, offline_avg)
        average_csi(pos, data, offline_avg)

    for pos, data in online_dict.iteritems():
        online_avg[pos] = {}
        average_rssi(pos, data, online_avg)
        average_csi(pos, data, online_avg)

        # test_plot(pos, online_avg)

    for pos in csi_dict:
        euclidean_distance(offline_avg[pos], online_avg["('?', '?')"], pos)

    # pprint(offline_avg)
    pprint(online_avg)
    pprint(euclideans)
    rpos = find_my_pos()
    print 'You are probably located at', rpos
