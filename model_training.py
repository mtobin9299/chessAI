import tensorflow as tf
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import network_module

EPOCHS = 3
LEARNING_RATE = 1e-3
TRAINING_DATA_FILE = 'cf_training_data-17-36.npy'
MODEL_NAME = 'basic1'

def train_model(training_data, model=None):
    X = np.array([np.resize(i[0],(len(training_data[0][0]) * len(training_data[0][0][0]), 1)) for i in training_data])
    Y = [i[1] for i in training_data]

    print("Input Length: " + str(len(X[0])))
    print("Output Length: " + str(len(Y[0])))
    if model is None:
        model = network_module.neural_network_model(input_size=len(X[0]), output_size=len(Y[0]), lr=LEARNING_RATE)

    model.fit({'input':X}, {'targets':Y}, n_epoch=EPOCHS, snapshot_step=500, show_metric=True,
               run_id=MODEL_NAME)
    return model

training_data = np.load('training_data\\' + TRAINING_DATA_FILE, allow_pickle=True)
model = train_model(training_data)
model.save(MODEL_NAME)