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
from cyton import OpenBCICyton


def print_raw(sample):
    print(sample.channels_data)


if __name__ == '__main__':
    port = 'COM12'
    baud = 115200
    board = OpenBCICyton(port=port, baud=baud)
    print('starting streaming...')
    board.start_stream(print_raw)
    board.disconnect()
