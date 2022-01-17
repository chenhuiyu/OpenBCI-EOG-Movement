import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import tensorflow.keras as keras
import pyautogui

BASE_DIR = os.path.dirname(os.path.abspath("__file__"))

sys.path.append(BASE_DIR)
from cyton import OpenBCICyton
import filter.filterlib as flt
from getDataFromCSV import standardization

import time

DATA = []

label = ["向前平视", "向右看", "向左看", "向上看", "向下看"]
model = keras.models.load_model("best_model.h5")


def moveMouse(flag):
    # 不动
    if flag == 0:
        pass
    # 右移
    elif flag == 1:
        currentMouseX, currentMouseY = pyautogui.position()
        for i in range(30):
            pyautogui.moveTo(currentMouseX + i, currentMouseY, duration=0)
    # 左移
    elif flag == 2:
        currentMouseX, currentMouseY = pyautogui.position()
        for i in range(30):
            pyautogui.moveTo(currentMouseX - i, currentMouseY, duration=0)
    # 上移
    elif flag == 3:
        currentMouseX, currentMouseY = pyautogui.position()
        for i in range(30):
            pyautogui.moveTo(currentMouseX, currentMouseY - i, duration=0)
    # 下移
    elif flag == 4:
        currentMouseX, currentMouseY = pyautogui.position()
        for i in range(30):
            pyautogui.moveTo(currentMouseX, currentMouseY + i, duration=0)


def receiveData(sample):
    global DATA
    global model

    smp = sample.channels_data
    frt = flt.FltRealTime(flt_type='4A')
    smp_flted = frt.filterIIR(smp)

    DATA.append([smp_flted[0], smp_flted[1]])

    # 每50个数据预测一次(0.2秒)
    start = time.time()
    if len(DATA) == 500:
        del DATA[:50]
        online_data = np.array(DATA).transpose()
        online_data = online_data[np.newaxis, :, :]
        online_data = standardization(online_data)
        prediction = model.predict(online_data).argmax()
        print("概率：", model.predict(online_data).max(), label[prediction])
        moveMouse(prediction)
        print("用时：", time.time() - start, "秒")
        DATA = []


if __name__ == '__main__':
    port = 'COM12'
    baud = 115200
    board = OpenBCICyton(port=port, baud=baud)
    print('starting streaming...')
    board.start_stream(receiveData)
    board.disconnect()
