import numpy as np
np.random.seed(666)  # for reproducibility

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D, Conv1D
from keras.utils import np_utils

import matplotlib.pyplot as plt
import DataLoad

winsize = 10
freq = 360

# We have 48 patients
X_train, Y_train = DataLoad.nload(Patients=(1,10), Winsize=winsize, Fs=freq, Norm=True)

X_test, Y_test = DataLoad.nload(Patients=(11,15), Winsize=winsize, Fs=freq, Norm=True)

X_valid, Y_valid = DataLoad.nload(Patients=(16,20), Winsize=winsize, Fs=freq, Norm=True)
#
#X_train, Y_train, annotation = DataLoad.fload(FileNames='TrainData/*.dat', 
#						  WinSize=winsize, 
#						  Fs=freq,
#						  AllowMistakes=allowmistakes,
#						  Norm=True)
#X_test, Y_test, annotation = DataLoad.fload(FileNames='TestData/*.dat', 
#						  WinSize=winsize, 
#						  Fs=freq,
#						  AllowMistakes=0,
#						  Norm=True)
#
#X_valid, Y_valid, annotation = DataLoad.fload(FileNames='ValidData/*.dat', 
#						  WinSize=winsize, 
#						  Fs=freq,
#						  AllowMistakes=0,
#						  Norm=True)	
								

								
print('\n \t Input data has been completely parsed and loaded!')

#X_train, X_test, Y_train, Y_test = DataLoad.Shuffle(X, Y, Percent=30)
print('X_train.shape: ', X_train.shape)
print('X_test.shape: ', X_test.shape)

print( 	'\n\tOk segments in train data:', Y_train[Y_train==1].shape[0], 
		'from', Y_train.shape[0])
print( 	'\n\tOk segments in test data:', Y_test[Y_test==1].shape[0], 
		'from', Y_test.shape[0], '\n\n')

# Reshape an input data
X_train = X_train.reshape(X_train.shape[0], 1, winsize*freq, 1)
X_valid = X_valid.reshape(X_valid.shape[0], 1, winsize*freq, 1)
X_test = X_test.reshape(X_test.shape[0], 1, winsize*freq, 1)

# Reshape a keys(classes) for training and testing
Y_train = np_utils.to_categorical(Y_train, 2)
Y_valid = np_utils.to_categorical(Y_valid, 2)
Y_test = np_utils.to_categorical(Y_test, 2)

# Declaring a model format
model = Sequential() 
	
model.add(Convolution2D(32, (1, 7), padding="same", activation='sigmoid', input_shape=(1, winsize*freq, 1)))
#print (model.output_shape)

model.add(Convolution2D(32, (1, 7), padding="same", activation='sigmoid'))
model.add(MaxPooling2D(pool_size=(1, 4)))
model.add(Convolution2D(32, (1, 7), padding="same", activation='sigmoid'))
#model.add(Dropout(0.25))
model.add(MaxPooling2D(pool_size=(1, 4)))
model.add(Convolution2D(32, (1, 7), padding="same", activation='sigmoid'))

model.add(MaxPooling2D(pool_size=(1, 4)))
model.add(Convolution2D(32, (1, 7), padding="same", activation='sigmoid'))

model.add(Flatten())
#model.add(Dense(2048, activation='tanh'))
#model.add(Dropout(0.25))
model.add(Dense(1024, activation='tanh'))
#model.add(Dropout(0.25))
model.add(Dense(128, activation='tanh'))
#model.add(Dropout(0.25))
model.add(Dense(2, activation='softmax'))

model.compile(	loss='categorical_crossentropy',
			optimizer='adam',
			metrics=['accuracy'])	           

print(model.summary())

# training
# Here - put a valid set
model.fit(	X_train, Y_train,
		validation_data=(X_valid, Y_valid),
		batch_size=36,
		nb_epoch=10,
		#validation_split=0.3,
		shuffle=True,
		verbose=2)
		
# evluation
score = model.evaluate(X_test, Y_test, batch_size=36)

for i in range(len(score)):
	print('\n', model.metrics_names[i], ': ',score[i])