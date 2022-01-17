import csv
import datetime
import multiprocessing as mp
import os
import sys

import filter.filterlib as flt
from cyton import OpenBCICyton
from Simulation import EyeMovementSimulation

BASE_DIR = os.path.dirname(os.path.abspath("__file__"))

sys.path.append(BASE_DIR)


def mp_acquisition(state, output_csv, streaming, terminate):
    print(' * acquisition * Current state: %s.' % state.value)
    print(' * acquisition * Acquisition will start soon.')

    # Callback function for OpenBCI class to handle samples.
    def handle_sample(sample):

        smp = sample.channels_data

        # filter sample
        frt = flt.FltRealTime(flt_type='4A')
        smp_flted = frt.filterIIR(smp)

        # Let the inreface know that the data is streaming.
        if board.streaming:
            streaming.set()

        # Quit program, stop and disconnect board.
        if terminate.is_set():
            print(' * acquisition * Disconnect signal sent...')
            streaming.clear()
            board.disconnect()
            sys.exit(0)

        with open(output_csv, 'at', newline="") as f:
            save = csv.writer(f)
            data = list(smp_flted) + [state.value]
            save.writerow(data)

    print(' * acquisition * Modules for OpenBCI real time set...')

    port = 'COM12'
    board = OpenBCICyton(port=port)
    print(' * acquisition * Starting streaming...')
    board.start_stream(handle_sample)
    board.disconnect()


if __name__ == '__main__':
    # 0. Define variables.
    subject_code = 'CHY'
    DATA_PATH = './data'

    # code the time to name file or variable
    csv_filename = os.path.join(DATA_PATH, subject_code + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M") + '.csv')

    # 1. Create stimuli object.
    simulation = EyeMovementSimulation(tralsNum=5, duration=1.5, flags=0)

    state = mp.Value('i', 0)
    #
    # Flag to communicate the interface when to
    # to start stimuli display.
    streaming = mp.Event()
    #
    # The way to stop the data acquisition.
    terminate = mp.Event()

    # Define process.
    recorder = mp.Process(target=mp_acquisition, args=(state, csv_filename, streaming, terminate))
    # Start process.
    recorder.start()
    print(' ! main ! Subprocess for recording started')

    ############################################
    # Stimuli reference
    #
    # State is shared between both objects.
    #

    simulation.start_display(state, streaming, terminate)
