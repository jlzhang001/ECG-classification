import numpy as np
np.random.seed(666)  # for reproducibility

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D, Conv1D
from keras.utils import np_utils

import matplotlib.pyplot as plt
import DataLoad
#import Features

X, Y, annotation = DataLoad.fload(FileNames='RowData/*.dat', 
						  WinSize=10, 
						  fs=360,
						  AllowMistakes=0)
print('Input data has been completely parsed and loaded!')

#print('X_train.shape: ', X_train.shape)
#print('X_test.shape: ', X_test.shape)
#print('Ok segments:', Y[Y==1].shape[0], 'from', Y.shape[0])

X_train, X_test, Y_train, Y_test = DataLoad.Shuffle(X, Y, Percent=30)

# Reshape an input data
X_train = X_train.reshape(X_train.shape[0], 1, 3600, 1)
X_test = X_test.reshape(X_test.shape[0], 1, 3600, 1)

# Reshape a keys(classes) for training and testing
Y_train = np_utils.to_categorical(Y_train, 2)
Y_test = np_utils.to_categorical(Y_test, 2)

# Declaring a model format
model = Sequential() 
	
model.add(Convolution2D(32, 1, 3, activation='relu', input_shape=(1, 3600, 1)))
#print (model.output_shape)

model.add(Convolution2D(32, 1, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(1,100)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

model.compile(	loss='categorical_crossentropy',
			optimizer='adam',
			metrics=['mse', 'accuracy'])	           
			#metrics=['accuracy'])
# train
model.fit(	X_train, Y_train,
		batch_size=64,
		nb_epoch=10,
		validation_split=0.3,
		shuffle=True,
		verbose=2)
# evluate 
score = model.evaluate(X_test, Y_test, batch_size=64)
print(model.metrics_names)
print(score)