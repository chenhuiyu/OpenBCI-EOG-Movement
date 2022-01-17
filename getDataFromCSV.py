import csv
import numpy as np
import os


def csv_process(data, filepath):
    with open(filepath, mode='r', encoding='utf-8', newline='') as f:
        # 此处读取到的数据是将每行数据当做列表返回的
        reader = csv.reader(f)
        for row in reader:
            data.append([float(row[0]), float(row[1]), int(row[-1])])
    return data


def standardization(data):
    mu = np.mean(data, axis=-1)
    mu = mu[:, :, np.newaxis]
    sigma = np.std(data, axis=-1)
    sigma = sigma[:, :, np.newaxis]
    return (data - mu) / sigma


def process_data():
    raw_data = []
    data_path = 'data'
    for csv_file in os.listdir(data_path):
        raw_data = csv_process(raw_data, os.path.join(data_path, csv_file))
    raw_data = np.array(raw_data)

    start = 0
    end = 0
    data = []
    label = []
    for i in range(1, len(raw_data)):
        end += 1
        if raw_data[i][-1] != raw_data[i - 1][-1]:
            data.append(raw_data[start + 10:start + 460, :-1].transpose())
            label.append(raw_data[start:end, -1])
            start = i
            end = i

    # 处理标签
    for i in range(len(label)):
        assert (np.all(label[i] == label[i][0]))
        label[i] = label[i][0]

    # 归一化
    data = standardization(data)
    label = np.array(label)
    return data, label


def split_train_test():
    data, label = process_data()
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * 0.2)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    x_train = data[train_indices]
    y_train = label[train_indices]
    x_test = data[test_indices]
    y_test = label[test_indices]

    return x_train, y_train, x_test, y_test
