"""
Krishna Panchapagesan, Mark Pock
CSE 163 Final Project

Uses a Sequential Model from keras to predict the coefficients of a
polynomial regression in what we have determined to be a postwar economic
period for significant wars (5 years after a war which has lasted at least a
year). Saves the model to ./model/model.pb. Accomodates using different
degrees of polynomial.
"""


import pandas as pd
from utils import time_series
from polynomials import construct, War
from keras import layers, Sequential
import keras
import numpy as np
from sklearn.model_selection import train_test_split


def vectorise(entry: War):
    """
    Given an entry of type War, returns a Series with two vectors. The first
    vector is an unrolling of the coefficients of the polynomial regressions
    that describe the prewar and wartime global economic health index adjusted
    for inflation. The second vector is the postwar global economic health
    index.
    """
    pre = list(entry.pre().coef)
    pre.extend(list(entry.dur().coef))
    features = pre
    labels = list(entry.post().coef)
    return pd.Series([features, labels])


def main(degree: int):
    final = time_series('final', concat=False)
    wars = pd.Series(final.columns[1:])
    entries = wars.apply(lambda war: construct(war, final, degree)).dropna()

    vectors = entries.apply(vectorise)
    x = vectors[0]
    y = vectors[1]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train,
                                                      test_size=0.25)
    arrays = (np.array(list(x_train)), np.array(list(x_test)),
              np.array(list(x_val)), np.array(list(y_train)),
              np.array(list(y_test)), np.array(list(y_val)))
    x_train, x_test, x_val, y_train, y_test, y_val = arrays

    degree += 1
    model = Sequential([layers.Dense(degree * 3, activation="relu",
                                     input_shape=(2 * degree,)),
                        layers.Dense(degree * 4, activation="relu"),
                        layers.Dense(degree * 3, activation="relu"),
                        layers.Dense(degree * 2, activation="relu"),
                        layers.Dense(degree)])

    model.compile(
        optimizer='adam',
        loss=keras.losses.MeanAbsolutePercentageError(
            reduction="auto", name="mean_absolute_percentage_error"
        ),
        metrics=[keras.losses.MeanAbsolutePercentageError(
                    reduction="auto", name="mean_absolute_percentage_error")]
    )

    print("Fit model on training data")
    hist = model.fit(x_train, y_train, batch_size=64, epochs=500,
                     validation_data=(x_val, y_val))
    print("Evaluation on test data:")
    results = model.evaluate(x_test, y_test, batch_size=128)
    print("test loss, test acc:", results)
    model.save("model")
    print('History', hist.history)


if __name__ == '__main__':
    main(int(input('What degree polynomial will you fit? ')))
