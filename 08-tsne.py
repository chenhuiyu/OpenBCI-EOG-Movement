import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from keras.utils import np_utils
from pylab import mpl
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from getDataFromCSV import split_train_test

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

x_train, y_train, x_test, y_test = split_train_test()
model = keras.models.load_model("best_model.h5")


# -------------------------------获取模型最后一层的数据--------------------------------
# 获取x = tf.keras.layers.Flatten()(x)数据
# Reference:https://becominghuman.ai/visualizing-representations-bd9b62447e38
def create_truncated_model(trained_model, input_shape):
    input_layer = keras.layers.Input(input_shape)

    x = keras.layers.Conv1D(filters=32, kernel_size=3, padding="same")(input_layer)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.ReLU()(x)

    x = keras.layers.Conv1D(filters=64, kernel_size=3, padding="same")(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.ReLU()(x)

    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(20, activation=tf.nn.relu)(x)

    for i, layer in enumerate(model.layers):
        layer.set_weights(trained_model.layers[i].get_weights())
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


truncated_model = create_truncated_model(model, x_train.shape[1:])
hidden_features = truncated_model.predict(np.concatenate((x_train, x_test), axis=0))

# -------------------------------PCA,tSNE降维分析--------------------------------
pca = PCA(n_components=5)  # 总的类别
pca_result = pca.fit_transform(hidden_features)
print('Variance PCA: {}'.format(np.sum(pca.explained_variance_ratio_)))

# Run T-SNE on the PCA features.
tsne = TSNE(n_components=2, verbose=1, method="exact")
tsne_results = tsne.fit_transform(hidden_features)

# -------------------------------可视化--------------------------------

y_test_cat = np_utils.to_categorical(np.concatenate((y_train, y_test), axis=0), num_classes=5)  # 总的类别
color_map = np.argmax(y_test_cat, axis=1)
plt.figure()
for cl in range(5):  # 总的类别
    indices = np.where(color_map == cl)
    indices = indices[0]
    plt.scatter(tsne_results[indices, 0], tsne_results[indices, 1], label=cl)
plt.legend(["向前平视", "向右看", "向左看", "向上看", "向下看"])
plt.show()
