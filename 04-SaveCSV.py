import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath("__file__"))

sys.path.append(BASE_DIR)
from cyton import OpenBCICyton
import filter.filterlib as flt

import csv
import datetime

DATA_PATH = "./data"
if os.path.exists(DATA_PATH) is False:
    os.makedirs(DATA_PATH)

###############################################################################
#
#   OPENBCI DATA AQUIRING PROCESS (BACKGROUND PROCESS)
#
###############################################################################


def saveData(sample):

    smp = sample.channels_data

    # filter sample
    smp_flted = frt.filterIIR(smp)
    print(smp_flted)

    with open(csv_filename, 'at', newline='') as f:
        save = csv.writer(f)
        # 保存滤波后的数据
        save.writerow(smp_flted)


if __name__ == '__main__':
    subject_code = 'CHY'

    # code the time to name file or variable
    csv_filename = os.path.join(DATA_PATH, subject_code + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M") + '.csv')
    # filtering in real time object creation
    frt = flt.FltRealTime(flt_type='4A')

    port = 'COM12'
    baud = 115200
    board = OpenBCICyton(port=port, baud=baud)
    print('starting streaming...')
    board.start_stream(saveData)
    board.disconnect()