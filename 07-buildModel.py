import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras

from getDataFromCSV import split_train_test


def make_model(input_shape, n_classes):
    input_layer = keras.layers.Input(input_shape)

    x = keras.layers.Conv1D(filters=32, kernel_size=3, padding="same")(input_layer)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.ReLU()(x)
    x = tf.keras.layers.Dropout(0.1)(x)

    x = keras.layers.Conv1D(filters=64, kernel_size=3, padding="same")(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.ReLU()(x)
    x = tf.keras.layers.Dropout(0.1)(x)

    # x = keras.layers.Conv1D(filters=128, kernel_size=3, padding="same")(x)
    # x = keras.layers.BatchNormalization()(x)
    # x = keras.layers.ReLU()(x)

    x = tf.keras.layers.Flatten()(x)
    # x = keras.layers.BatchNormalization()(x)
    # x = tf.keras.layers.Dense(64, activation=tf.nn.relu)(x)
    # x = tf.keras.layers.Dropout(0.5)(x)
    x = tf.keras.layers.Dense(20, activation=tf.nn.relu)(x)

    output_layer = keras.layers.Dense(n_classes, activation="softmax")(x)
    return keras.models.Model(inputs=input_layer, outputs=output_layer)


def train():

    x_train, y_train, x_test, y_test = split_train_test()

    n_classes = len(np.unique(y_train))

    model = make_model(input_shape=x_train.shape[1:], n_classes=n_classes)
    keras.utils.plot_model(model, show_shapes=True, dpi=320)

    epochs = 200
    batch_size = 128
    # learning_rate = 0.0001

    callbacks = [
        keras.callbacks.ModelCheckpoint("best_model.h5", save_best_only=True, monitor="val_loss"),
        keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.1, patience=10, min_lr=0),
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=30, verbose=1),
    ]
    model.compile(
        optimizer="Adam",
        loss="sparse_categorical_crossentropy",
        metrics=["sparse_categorical_accuracy"],
    )
    history = model.fit(
        x_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        callbacks=callbacks,
        validation_data=(x_test, y_test),
        verbose=1,
    )

    model = keras.models.load_model("best_model.h5")

    test_loss, test_acc = model.evaluate(x_test, y_test)

    print("Test accuracy", test_acc)
    print("Test loss", test_loss)

    metric = "sparse_categorical_accuracy"
    plt.figure()
    plt.plot(history.history[metric])
    plt.plot(history.history["val_" + metric])
    plt.title("model " + metric)
    plt.ylabel(metric, fontsize="large")
    plt.xlabel("epoch", fontsize="large")
    plt.legend(["train", "val"], loc="best")
    plt.show()
    plt.close()


if __name__ == "__main__":
    train()
