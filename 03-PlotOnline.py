import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath("__file__"))

sys.path.append(BASE_DIR)
from cyton import OpenBCICyton
import filter.filterlib as flt
import plot.plotlib as pltlib


def plotData(sample):

    smp = sample.channels_data

    # filter sample
    smp_flted = frt.filterIIR(smp)
    print(smp_flted)
    # online plotting using matplotlib blit
    prt.frame_plot(smp_flted)


if __name__ == '__main__':

    # filtering in real time object creation
    frt = flt.FltRealTime(flt_type='4A')

    # plotting in real time object creation
    prt = pltlib.OnlinePlot(samples_per_frame=4, channels=8)

    port = 'COM12'
    baud = 115200
    board = OpenBCICyton(port=port, baud=baud)
    print('starting streaming...')
    board.start_stream(plotData)
    board.disconnect()
