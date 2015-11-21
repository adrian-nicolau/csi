#!/usr/bin/env python
'''
Created on Jul 29, 2015

@author: adrian
'''

from oct2py import octave
from pylab import *  # @UnusedWildImport

import os
import scipy.io as sio


PNGDIR = '/home/adrian/workspace/csi/png/'
MATDIR = '/home/adrian/workspace/csi/mat/'

label_on = False


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

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Usage: $ %s <.dat file>' % sys.argv[0]
        sys.exit(1)

    dat_path = os.path.abspath(sys.argv[1])
    dat_filename = os.path.splitext(os.path.basename(dat_path))[0]
    plot_dir = PNGDIR + dat_filename + '_' + \
        datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '/'
    os.mkdir(plot_dir)

    octave.addpath('~/csi/linux-80211n-csitool-supplementary/matlab')
    # FAQ #2
    octave.eval("csi_trace = read_bf_file('" + dat_path + "');")
    pkts = octave.eval("rows(csi_trace);")
    print 'Trace has', pkts, 'packets.'

    for pkt in range(1, int(pkts) + 1):  # Octave indexes from 1
        octave.eval("csi_entry = csi_trace{" + str(pkt) + "};")
        # if octave.eval("csi_entry.Nrx;") != 3:
        #    continue

        octave.eval("csi = get_scaled_csi(csi_entry);")
        octave.eval("save -6 " + MATDIR + "temp.mat csi;")

        mat_contents = sio.loadmat(MATDIR + 'temp.mat')['csi']
        plot_csi(mat_contents, pkt)
