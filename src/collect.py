#!/usr/bin/env python
'''
Created on Jul 29, 2015

@author: adrian
'''

import json
import os
import scipy.io as sio
import shutil
import sys


from oct2py import octave
from pprint import pprint
from pylab import *  # @UnusedWildImport


PNGDIR = os.path.abspath('.') + '/png/'
MATDIR = os.path.abspath('.') + '/mat/'

label_on = False

VERMAGIC = datetime.datetime.now().strftime("data_%m%d")
JSON_NAME = 'json/' + VERMAGIC + '.json'


def jsonify_csi(csi_contents, rssi, pkt_index, xpos, ypos):

    csi_contents = csi_contents[0]  # we only have the RX dimension
    csi_node = {}
    csi_node['index'] = pkt_index
    csi_node['csi_a'] = [str(c) for c in csi_contents[0]]
    csi_node['csi_b'] = [str(c) for c in csi_contents[1]]
    csi_node['csi_c'] = [str(c) for c in csi_contents[2]]
    csi_node['rssi_a'] = rssi[0]
    csi_node['rssi_b'] = rssi[1]
    csi_node['rssi_c'] = rssi[2]

    csi_dict[str((xpos, ypos))].append(csi_node)


def plot_csi(csi_contents, pkt_number):
    global label_on, plot_dir

    Ntx, Nrx = csi_contents.shape[:2]
    if Ntx != 1:
        print "We'll stick to a single TX path for now.", pkt_number
        return

    csi_contents = csi_contents[0]  # we only have the RX dimension

    for antenna in range(Nrx):
        # amplitude
        csi_contents[antenna] = [abs(x) for x in csi_contents[antenna]]
        # power
        csi_contents[antenna] = [pow(x, 2) for x in csi_contents[antenna]]
        # dB
        csi_contents[antenna] = 10. * np.log10(csi_contents[antenna])
        # We no longer have complex numbers, so remove +0j
        csi_contents = [abs(x) for x in csi_contents]

    # csi_contents = np.transpose(csi_contents)

    if not label_on:
        plot(csi_contents[0], label='RX Antenna A')
        plot(csi_contents[1], label='RX Antenna B')
        plot(csi_contents[2], label='RX Antenna C')
        label_on = True
    else:
        plot(csi_contents[0])
        plot(csi_contents[1])
        plot(csi_contents[2])

    axis([0, 30, 5, 30])
    xlabel('Subcarrier index')
    ylabel('SNR [dB]')
    legend(loc='lower right')
    savefig(plot_dir + '%04d' % pkt_number + '.png', bbox_inches='tight')
    # close()

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print 'Usage: $ %s <.dat file> <xpos> <ypos>' % sys.argv[0]
        sys.exit(1)

    # online phase
    if (sys.argv[2] == '?' and sys.argv[3] == '?'):
        JSON_NAME = 'json/online.json'
        plot_dir = PNGDIR + VERMAGIC + '_?_?/'
        csi_dict = {}
        xpos, ypos = '?', '?'

    # offline phase
    else:
        xpos, ypos = int(sys.argv[2]), int(sys.argv[3])
        plot_dir = PNGDIR + VERMAGIC + '_' + \
            '%02d' % xpos + '_' + '%02d' % ypos + '/'

        if os.path.exists(JSON_NAME):
            with open(JSON_NAME, 'rt') as infile:
                csi_dict = json.load(infile)
        else:
            csi_dict = {}

    if os.path.exists(plot_dir):
        shutil.rmtree(plot_dir)
    os.mkdir(plot_dir)

    dat_path = os.path.abspath(sys.argv[1])
    octave.addpath('~/csi/linux-80211n-csitool-supplementary/matlab')
    # FAQ #2
    octave.eval("csi_trace = read_bf_file('" + dat_path + "');")
    pkts = octave.eval("rows(csi_trace);")
    print 'Trace has', pkts, 'packets.'

    # overwrite is permitted
    csi_dict[str((xpos, ypos))] = []

    for index in range(1, int(pkts) + 1):  # Octave indexes from 1
        octave.eval("csi_entry = csi_trace{" + str(index) + "};")
        rssi_a, rssi_b, rssi_c = octave.eval("csi_entry.rssi_a;"), \
            octave.eval("csi_entry.rssi_b;"), octave.eval("csi_entry.rssi_c;")

        octave.eval("csi = get_scaled_csi(csi_entry);")
        octave.eval("save -6 " + MATDIR + "temp.mat csi;")

        mat_contents = sio.loadmat(MATDIR + 'temp.mat')['csi']
        jsonify_csi(mat_contents, [rssi_a, rssi_b, rssi_c], index, xpos, ypos)
        plot_csi(mat_contents, index)

    with open(JSON_NAME, 'w+') as outfile:
        json.dump(csi_dict, outfile, sort_keys=True, indent=4)
