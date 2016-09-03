#!/usr/bin/env python

from __future__ import division

import matplotlib
#matplotlib.use('Agg')

from copy import deepcopy
from pprint import pprint
from pylab import *  # @UnusedWildImport

import json
import numpy as np
import re
import sys


ONLINE_POINTS = [
    '(0, 0)',
    '(0, 2)',
    '(0, 4)',
    '(1, 2)',
    '(2, 0)',
    '(2, 1)',
    '(2, 3)',
    '(2, 4)',
    '(3, 2)',
    '(4, 0)',
    '(4, 2)',
    '(4, 4)'
]

OFFLINE_POINTS = [
    '(0, 1)',
    '(0, 3)',
    '(1, 0)',
    '(1, 1)',
    '(1, 3)',
    '(1, 4)',
    '(2, 2)',
    '(3, 0)',
    '(3, 1)',
    '(3, 3)',
    '(3, 4)',
    '(4, 1)',
    '(4, 3)'
]

PLOT_3D_DATA_X = [eval(p)[0] for p in ONLINE_POINTS]
PLOT_3D_DATA_Y = [eval(p)[1] for p in ONLINE_POINTS]
PLOT_3D_DATA_Z = []

total_error = 0

def where_am_i(online_point):
    global total_error

    euclid_diag1 = euclidean_distance(
        online_point=online_point,
        avg_dict=csi_avg_dict_diag1
    )
    euclid_med = euclidean_distance(
        online_point=online_point,
        avg_dict=csi_avg_dict_med
    )
    euclid_diag2 = euclidean_distance(
        online_point=online_point,
        avg_dict=csi_avg_dict_diag2
    )

    p1 = find_pos(online_point, euclid_diag1)
    p2 = find_pos(online_point, euclid_med)
    p3 = find_pos(online_point, euclid_diag2)

    final = ((p1[0] + p2[0] + p3[0]) / 3, (p1[1] + p2[1] + p3[1]) / 3)
    error = np.linalg.norm(np.array(final) - np.array(eval(online_point)))
    print online_point, 'detected at', final, 'with error', error

    total_error += error

    return error


def find_pos(online_point, euclideans, k=3, csi_factor=1, rssi_factor=0):
    costs = []
    costs_per_pos = {}

    for pos in euclideans:
        cost = (euclideans[pos]['dist_csi_a'] +
                euclideans[pos]['dist_csi_b'] +
                euclideans[pos]['dist_csi_c']) * csi_factor
        cost += euclideans[pos]['dist_rssi'] * rssi_factor

        #print pos, cost
        costs.append(cost)
        costs_per_pos[pos] = cost

    best_k_costs = sorted(costs)[:k]
    if len(best_k_costs) < k:
        k = len(best_k_costs)

    x_total, y_total = 0, 0

    for cost in best_k_costs:
        for pos, value in costs_per_pos.iteritems():
            if cost == value:
                pos = re.sub('[(,)]', '', pos)
                x_total += float(pos.split(' ')[0])
                y_total += float(pos.split(' ')[1])

    return (x_total / k, y_total / k)


def euclidean_distance(online_point, avg_dict):

    euclideans = {}

    if online_point not in ONLINE_POINTS:
        sys.exit('Wrong online point!')

    ondata = avg_dict[online_point]

    for pos in avg_dict:

        if pos not in OFFLINE_POINTS:
            continue

        euclideans[pos] = {}
        offdata = avg_dict[pos]

        euclideans[pos]['dist_csi_a'] = np.linalg.norm(
            offdata['csi_a'] - ondata['csi_a'])
        euclideans[pos]['dist_csi_b'] = np.linalg.norm(
            offdata['csi_b'] - ondata['csi_b'])
        euclideans[pos]['dist_csi_c'] = np.linalg.norm(
            offdata['csi_c'] - ondata['csi_c'])

        euclideans[pos]['dist_rssi_a'] = abs(
            offdata['rssi_a'] - ondata['rssi_a'])
        euclideans[pos]['dist_rssi_b'] = abs(
            offdata['rssi_b'] - ondata['rssi_b'])
        euclideans[pos]['dist_rssi_c'] = abs(
            offdata['rssi_c'] - ondata['rssi_c'])
        euclideans[pos]['dist_rssi'] = abs(offdata['rssi'] - ondata['rssi'])

    return euclideans


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
            # get rid of RuntimeWarning: divide by zero encountered in log10
            node[antenna] = [0.1 if x == 0.0 else x for x in node[antenna]]
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


def average_dict(full_dict):
    avg_dict = {}

    for pos, data in full_dict.iteritems():
        avg_dict[pos] = {}
        average_rssi(pos, data, avg_dict)
        average_csi(pos, data, avg_dict)

    return avg_dict


def interpolate_data():
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.interpolate
    from operator import itemgetter

    x = np.array(PLOT_3D_DATA_X)
    y = np.array(PLOT_3D_DATA_Y)
    z = np.array(PLOT_3D_DATA_Z)

    # Set up a regular grid of interpolation points
    xi, yi = np.linspace(x.min(), x.max()), np.linspace(y.min(), y.max())
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate
    rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
    zi = rbf(xi, yi)

    plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
                extent=[x.min(), x.max(), y.min(), y.max()])
    plt.scatter(x, y, c=z, marker='o', s=50)
    plt.colorbar()
    plt.xlabel('X axis')
    plt.ylabel('Y axis')

    plt.show()


if __name__ == '__main__':

    # Open all three databases
    with open('../collected/exp25/diag1/data_0810.json', 'rt') as offline_file:
        csi_full_dict_diag1 = json.load(offline_file)

    with open('../collected/exp25/med/data_0810.json', 'rt') as offline_file:
        csi_full_dict_med = json.load(offline_file)

    with open('../collected/exp25/diag2/data_0810.json', 'rt') as offline_file:
        csi_full_dict_diag2 = json.load(offline_file)

    csi_avg_dict_diag1 = average_dict(csi_full_dict_diag1)
    csi_avg_dict_med = average_dict(csi_full_dict_med)
    csi_avg_dict_diag2 = average_dict(csi_full_dict_diag2)

    for online_point in ONLINE_POINTS:
        error = where_am_i(online_point)
        PLOT_3D_DATA_Z.append(error)
    print total_error
    print 'mean', total_error / len(ONLINE_POINTS)
    print 'median', np.median(PLOT_3D_DATA_Z)

    interpolate_data()

    # from mpl_toolkits.mplot3d import Axes3D
    # import matplotlib.pyplot as plt

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # zpos = [0 for _ in range(len(PLOT_3D_DATA_Z))]
    # dx = np.ones(len(PLOT_3D_DATA_X))
    # dy = np.ones(len(PLOT_3D_DATA_Y))

    # ax.bar3d(PLOT_3D_DATA_X, PLOT_3D_DATA_Y, zpos, dx, dy, PLOT_3D_DATA_Z, color='#ff0000')

    # ax.set_xlabel('Ox')
    # ax.set_ylabel('Oy')
    # ax.set_zlabel('Error')

    # plt.show()
