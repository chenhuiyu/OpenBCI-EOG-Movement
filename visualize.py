import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl

from getDataFromCSV import process_data

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

data, label = process_data()

classes = np.unique(label)

plt.figure()
# for c in classes:
for c in classes:
    for i in range(10):
        c_x_train = data[label == c]
        plt.plot(c_x_train[i][0], label="channel 0, class " + str(c))
        plt.plot(c_x_train[i][1], label="channel 1, class " + str(c))
        plt.legend(loc="best")
        # plt.show()
        # plt.close()
        plt.savefig('class' + str(c) + "_" + str(i))
        plt.close()
