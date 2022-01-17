'''
name:
acquire_and_print.py

type:
script
'''
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
sys.path.append(BASE_DIR)

import filter.filterlib as flt
from cyton import OpenBCICyton


def printData(sample):

    # get sample form the all channel
    smp = sample.channels_data

    # filter sample
    smp_flted = frt.filterIIR(smp)
    print(smp_flted)


if __name__ == '__main__':
    # filtering in real time object creation
    frt = flt.FltRealTime(flt_type='4A')

    port = 'COM12'
    baud = 115200
    board = OpenBCICyton(port=port, baud=baud)
    print('starting streaming...')
    board.start_stream(printData)
    board.disconnect()
